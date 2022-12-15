from time import sleep
import os
from invoke import task
from fabric import Connection
from textwrap import dedent


@task
def write_env(c, prerender, ssr, csr, dest):
    env = dedent(
        f"""\
    VITE_PRERENDER = {prerender}
    VITE_SSR = {ssr}
    VITE_CSR = {csr}
    """
    )
    with open("/tmp/.env", "w") as w:
        w.write(env)
    c.put("/tmp/.env", dest)


@task
def build(c, env=os.environ):
    github_token = os.environ["GITHUB_TOKEN"]
    c.run("rm -rf ~/build_node ~/build_static")
    c.run("rm -rf btcnewstoday")
    if c.run("test -d btcnewstoday", warn=True).failed:
        c.run(
            f"git clone https://{github_token}@github.com/lightningorb/btcnewstoday.git"
        )
    with c.cd("btcnewstoday"):
        c.run("git checkout permalinks_og_tags")
        copy_stuff(c)
        c.run("pip3 install virtualenv")
        c.run(
            f"""echo 'export const API_FQDN = "https://{c.host}";' > src/svelte_site/src/lib/constants.js"""
        )
        c.run("rm -rf src/api/venv")
        c.run(
            "cd src/api && python3 -m virtualenv venv && . venv/bin/activate && pip3 install -r requirements.txt && pip3 install -r requirements-dev.txt"
        )
        c.run("sudo supervisorctl reload")
        sleep(10)
        c.run(
            "cp src/svelte_site/svelte.config.node.js src/svelte_site/svelte.config.js"
        )
        write_env(
            c,
            prerender="false",
            ssr="true",
            csr="true",
            dest="btcnewstoday/src/svelte_site/.env",
        )
        c.run(". ~/.nvm/nvm.sh && cd src/svelte_site && npm install")
        c.run(
            """sed -i '2i "type": "module",' src/svelte_site/node_modules/@popperjs/core/package.json"""
        )
        c.run(". ~/.nvm/nvm.sh && cd src/svelte_site && npm run build")
        # c.run("mv src/svelte_site/build ~/build_node")
        # build_static(c)


@task
def build_static(c):
    github_token = os.environ["GITHUB_TOKEN"]
    c.run("rm -rf ~/build_node ~/build_static")
    c.run("rm -rf btcnewstoday_static")
    if c.run("test -d btcnewstoday_static", warn=True).failed:
        c.run(
            f"git clone https://{github_token}@github.com/lightningorb/btcnewstoday.git btcnewstoday_static"
        )
    with c.cd("btcnewstoday_static"):
        c.run("git checkout permalinks_og_tags")
        c.run(
            f"""echo 'export const API_FQDN = "https://{c.host}";' > src/svelte_site/src/lib/constants.js"""
        )
        c.run("pip3 install virtualenv")
        c.run("rm -rf src/api/venv")
        c.run(
            "cd src/api && python3 -m virtualenv venv && . venv/bin/activate && pip3 install -r requirements.txt && pip3 install -r requirements-dev.txt"
        )
        c.run(". ~/.nvm/nvm.sh && cd src/svelte_site && npm install")
        c.run(
            """sed -i '2i "type": "module",' src/svelte_site/node_modules/@popperjs/core/package.json"""
        )
        c.run(
            "cp src/svelte_site/svelte.config.static.js src/svelte_site/svelte.config.js"
        )
        write_env(
            c,
            prerender="true",
            ssr="true",
            csr="true",
            dest="btcnewstoday_static/src/svelte_site/.env",
        )
        c.run(". ~/.nvm/nvm.sh && cd src/svelte_site && npm run build")


@task
def supervisord_conf(c):
    for conf in ["btcnewstoday_api.conf", "btcnewstoday.conf"]:
        c.put(f"src/build_system/conf/{conf}", "/tmp/")
        c.sudo(f"cp /tmp/{conf} /etc/supervisor/conf.d/")
        c.sudo(f"cp /tmp/{conf} /etc/supervisor/conf.d/")
    c.sudo("supervisorctl reload")


@task
def nginx_conf(c):
    with open("src/build_system/conf/btcnewstoday_ssl.nginx") as f:
        content = f.read()
        content = content.replace("{HOSTNAME}", c.host)
        with open("/tmp/btcnewstoday.nginx", "w") as w:
            w.write(content)
    c.put("/tmp/btcnewstoday.nginx", "/tmp/")
    c.sudo(f"cp /tmp/btcnewstoday.nginx /etc/nginx/sites-available/")
    c.sudo(
        f"ln -fs /etc/nginx/sites-available/btcnewstoday.nginx /etc/nginx/sites-enabled/"
    )
    c.sudo(f"rm -f /etc/nginx/sites-enabled/default")
    c.sudo("nginx -s reload")


@task
def copy_stuff(c):
    c.put("src/api/bn_secrets.py", "btcnewstoday/src/api/")
    home = c.run("echo $HOME").stdout.strip()
    path = f"{home}/database.db"
    c.put("src/api/database.db", f"{home}/database.db")


def cron_cmd(c, job):
    c.run(
        f""" (crontab -l ; echo "{job}") 2>&1 | grep -v "no crontab" | sort | uniq | crontab - """
    )


@task
def cron(c, env=os.environ):
    cron_cmd(c, "0 * * * *     curl -X POST http://localhost:8000/api/ingest/articles/")
    cron_cmd(c, "0 * * * *     curl -X POST http://localhost:8000/api/ingest/podcasts/")
    cron_cmd(c, "0 */4 * * *   curl -X POST http://localhost:8000/api/snapshot/")
    cmd = "0 */12 * * *   bndev_bucket=btcnewstoday cd ~/btcnewstoday_static && . src/api/venv/bin/activate && timeout 43200 fab snapshot.snapshot-past"
    cron_cmd(cmd)
    cron_cmd(
        c,
        f"*/5 * * * *   bndev_bucket={env['bndev_bucket']} cd ~/btcnewstoday_static && . src/api/venv/bin/activate && fab snapshot.snapshot",
    )


@task
def migrate_db(c):
    with c.cd("btcnewstoday/src/api"):
        c.run(". venv/bin/activate && alembic upgrade head")

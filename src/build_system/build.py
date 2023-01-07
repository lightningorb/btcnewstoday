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
    branch = c.local("git rev-parse --abbrev-ref HEAD").stdout.strip()
    with c.cd("btcnewstoday"):
        c.run(f"git checkout {branch}")
        c.run("pip3 install virtualenv")
        c.run(
            f"""echo 'export const API_FQDN = "https://{c.host}";' > src/svelte_site/src/lib/constants.js"""
        )
        c.run("rm -rf src/api/venv")
        c.run(
            "cd src/api && python3 -m virtualenv venv && . venv/bin/activate && pip3 install -r requirements.txt && pip3 install -r requirements-dev.txt"
        )
        migrate_db(c)
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
    c.run("sudo supervisorctl reload")


@task
def build_static(c):
    github_token = os.environ["GITHUB_TOKEN"]
    c.run("rm -rf ~/build_node ~/build_static")
    c.run("rm -rf btcnewstoday_static")
    if c.run("test -d btcnewstoday_static", warn=True).failed:
        c.run(
            f"git clone https://{github_token}@github.com/lightningorb/btcnewstoday.git btcnewstoday_static"
        )
    branch = c.local("git rev-parse --abbrev-ref HEAD").stdout.strip()
    with c.cd("btcnewstoday_static"):
        c.run(f"git checkout {branch}")
        c.run(
            f"""echo 'export const API_FQDN = "https://{c.host}";' > src/svelte_site/src/lib/constants.js"""
        )
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
        c.run("rm -rf src/svelte_site/src/routes/jsapi")
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


def cron_cmd(c, job):
    c.run(
        f""" (crontab -l ; echo "{job}") 2>&1 | grep -v "no crontab" | sort | uniq | crontab - """
    )


@task
def cron(c, env=os.environ):
    cron_cmd(c, "0 * * * *     curl -X POST http://localhost:8000/api/ingest/articles/")
    cron_cmd(c, "0 * * * *     curl -X POST http://localhost:8000/api/ingest/podcasts/")
    cron_cmd(c, "0 * * * *     curl -X GET http://localhost:8000/api/images/")
    cron_cmd(c, "0 * * * *     curl -X GET http://localhost:8000/api/meta/")
    cron_cmd(c, "5 * * * *     curl -X GET http://localhost:8000/api/meta/index/")
    cron_cmd(
        c,
        "0 * * * *     sudo su postgres -c 'cd /home/postgres && pg_dump -d postgres -Fc > postgres.sql' && sudo cp /home/postgres/postgres.sql .",
    )
    cron_cmd(
        c,
        f"*/10 * * * *  cd ~/btcnewstoday_static && . src/api/venv/bin/activate && env bndev_bucket={env['bndev_bucket']} timeout 600 fab snapshot.snapshot",
    )
    cron_cmd(
        c,
        "5 * * * *     /usr/local/bin/aws s3 cp postgres.sql s3://btcnews-db-backups/bndev-us-west-1/`date +%Y-%m-%d`/",
    )


@task
def import_db(c):
    c.run(
        "aws s3 cp s3://btcnews-db-backups/bndev-us-west-2/`date +%Y-%m-%d`/postgres.sql ."
    )
    # c.run(
    # "PGPASSWORD=abc_abc_123_abc_abc_123-abc_abc_123 psql -h localhost -p 5432 -w -v --create --dbname btcnewstoday < db.sql"
    # )
    c.run("pg_restore -v -d postgres < postgres.sql")


@task
def migrate_db(c):
    c.run("cd src/api && . venv/bin/activate && alembic upgrade head")
    c.run("cd src/api && . venv/bin/activate && python3 migrate.py")

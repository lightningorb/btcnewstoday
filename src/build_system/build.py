import os
from invoke import task
from fabric import Connection


@task
def build(c, env=os.environ):
    github_token = os.environ["GITHUB_TOKEN"]
    c.run("rm -rf btcnewstoday")
    c.run(f"git clone https://{github_token}@github.com/lightningorb/btcnewstoday.git")
    with c.cd("btcnewstoday"):
        # c.run(f"git checkout permalink")
        c.run("pip3 install virtualenv")
        c.run(
            f"""echo 'export const API_FQDN = "https://{c.host}";' > src/svelte_site/src/lib/constants.js"""
        )
        c.run(". ~/.nvm/nvm.sh && cd src/svelte_site && npm install && npm run build")
        c.run("rm -rf src/api/venv")
        c.run(
            "cd src/api && python3 -m virtualenv venv && . venv/bin/activate && pip3 install -r requirements.txt"
        )
        c.run("sudo supervisorctl reload")


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
    c.put("src/api/database.db", "btcnewstoday/src/api/database.db")


def cron_cmd(c, job):
    c.run(
        f""" (crontab -l ; echo "{job}") 2>&1 | grep -v "no crontab" | sort | uniq | crontab - """
    )


@task
def cron(c):
    cron_cmd(c, "0 * * * *     curl -X POST http://localhost:8000/api/ingest/articles/")
    cron_cmd(c, "0 * * * *     curl -X POST http://localhost:8000/api/ingest/podcasts/")
    cron_cmd(c, "0 */4 * * *   curl -X POST http://localhost:8000/api/snapshot/")
    c.run("curl -X POST http://localhost:8000/api/snapshot/")


@task
def migrate_db(c):
    with c.cd("btcnewstoday/src/api"):
        c.run(". venv/bin/activate && alembic upgrade head")

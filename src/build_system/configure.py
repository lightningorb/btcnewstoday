from textwrap import dedent
import os
from invoke import task
from fabric import Connection


@task
def setup(c):
    c.sudo("""adduser --home /home/postgres --disabled-password --gecos "" postgres""")
    c.sudo("adduser postgres sudo")
    c.sudo("apt-get update")
    c.sudo(
        "apt-get install postgresql postgresql-contrib mosh nginx git make zip python3-pip supervisor certbot python3-certbot-nginx unzip -y"
    )
    c.sudo("systemctl start nginx")
    cmd = "curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash"
    c.run(cmd)
    c.run(". .nvm/nvm.sh && nvm install v16.14.2")
    c.sudo(f"hostname {c.host}")
    c.sudo("mkdir -p ../postgres/.ssh/")
    c.sudo("cp .ssh/authorized_keys ../postgres/.ssh/")
    c.sudo("chown postgres -R ../postgres")


@task
def setup_postgres(c):
    """
    TODO: fix me
    """
    c.sudo(
        """echo "listen_addresses = '*'" >> /etc/postgresql/14/main/postgresql.conf"""
    )

    c.sudo(
        """echo "host  all  all 0.0.0.0/0 md5" >> /etc/postgresql/14/main/pg_hba.conf"""
    )
    c.run(
        dedent(
            """\
            psql -U postgres postgres <<OMG
            CREATE USER btcnewstoday password 'abc_abc_123_abc_abc_123-abc_abc_123';
            CREATE DATABASE btcnewstoday;
            GRANT ALL PRIVILEGES ON DATABASE btcnewstoday TO btcnewstoday;
            OMG
           """
        )
    )
    c.sudo("systemctl restart postgresql")


@task
def aws_cli(c, env=os.environ):
    with c.cd("/tmp"):
        c.run(
            'curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"'
        )
        c.run("unzip awscliv2.zip")
        c.run("sudo ./aws/install")
    aws_access_key_id = os.environ["aws_access_key_id"]
    aws_secret_access_key = os.environ["aws_secret_access_key"]
    c.run("mkdir -p .aws")
    c.run("echo '[default]' > .aws/credentials")
    c.run(f"echo 'aws_access_key_id = {aws_access_key_id}' >> .aws/credentials")
    c.run(f"echo 'aws_secret_access_key = {aws_secret_access_key}' >> .aws/credentials")


@task
def generate_cert(c):
    c.sudo(f"certbot -n --agree-tos --email btcnewstoday@proton.me --nginx -d {c.host}")


@task
def copy_certs_to_s3(c):
    c.sudo(f"cp -r /etc/letsencrypt /tmp/")
    with c.cd("/tmp"):
        c.run("sudo tar -zcvf letsencrypt.tar.gz letsencrypt")
        dst = f"s3://btcnews-db-backups/certs/{c.host}/"
        c.run(f"aws s3 cp /tmp/letsencrypt.tar.gz {dst}")


@task
def get_certs_from_s3(c):
    # c.sudo("ls /etc/letsencrypt/live/*")
    c.sudo("rm -rf /tmp/tmp /tmp/letsencrypt.tar.gz /etc/letsencrypt")
    dst = f"/tmp/"
    src = f"s3://btcnews-db-backups/certs/{c.host}/letsencrypt.tar.gz"
    c.run(f"aws s3 cp {src} {dst}")
    with c.cd("/tmp"):
        c.run("sudo tar xvf letsencrypt.tar.gz")
    c.sudo(
        f"mv /tmp/letsencrypt/live/{c.host}-0002 /tmp/letsencrypt/live/{c.host}",
        warn=True,
    )
    c.sudo(f"mv /tmp/letsencrypt /etc/")


@task
def main(c):
    setup(c)
    aws_cli(c)

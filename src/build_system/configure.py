from textwrap import dedent
import os
from invoke import task
from fabric import Connection


@task
def setup_amqp(c):
    c.sudo("apt-get install curl gnupg apt-transport-https -y")
    c.sudo(
        'curl -1sLf "https://keys.openpgp.org/vks/v1/by-fingerprint/0A9AF2115F4687BD29803A206B73A36E6026DFCA" | sudo gpg --dearmor | sudo tee /usr/share/keyrings/com.rabbitmq.team.gpg > /dev/null'
    )
    c.sudo(
        'curl -1sLf "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0xf77f1eda57ebb1cc" | sudo gpg --dearmor | sudo tee /usr/share/keyrings/net.launchpad.ppa.rabbitmq.erlang.gpg > /dev/null'
    )
    c.sudo(
        'curl -1sLf "https://packagecloud.io/rabbitmq/rabbitmq-server/gpgkey" | sudo gpg --dearmor | sudo tee /usr/share/keyrings/io.packagecloud.rabbitmq.gpg > /dev/null'
    )
    c.sudo("chmod a+w -R /etc/apt/sources.list.d/")
    c.sudo(
        "echo 'deb [signed-by=/usr/share/keyrings/net.launchpad.ppa.rabbitmq.erlang.gpg] http://ppa.launchpad.net/rabbitmq/rabbitmq-erlang/ubuntu jammy main' >> /etc/apt/sources.list.d/rabbitmq.list"
    )
    c.sudo(
        "echo 'deb-src [signed-by=/usr/share/keyrings/net.launchpad.ppa.rabbitmq.erlang.gpg] http://ppa.launchpad.net/rabbitmq/rabbitmq-erlang/ubuntu jammy main' >> /etc/apt/sources.list.d/rabbitmq.list"
    )
    c.sudo(
        "echo 'deb [signed-by=/usr/share/keyrings/io.packagecloud.rabbitmq.gpg] https://packagecloud.io/rabbitmq/rabbitmq-server/ubuntu/ jammy main' >> /etc/apt/sources.list.d/rabbitmq.list"
    )
    c.sudo(
        "echo 'deb-src [signed-by=/usr/share/keyrings/io.packagecloud.rabbitmq.gpg] https://packagecloud.io/rabbitmq/rabbitmq-server/ubuntu/ jammy main' >> /etc/apt/sources.list.d/rabbitmq.list"
    )
    c.sudo("apt-get update -y")
    c.sudo(
        "apt-get install -y erlang-base erlang-asn1 erlang-crypto erlang-eldap erlang-ftp erlang-inets erlang-mnesia erlang-os-mon erlang-parsetools erlang-public-key erlang-runtime-tools erlang-snmp erlang-ssl erlang-syntax-tools erlang-tftp erlang-tools erlang-xmerl"
    )
    c.sudo("apt-get install rabbitmq-server -y --fix-missing")
    c.sudo("rabbitmq-plugins enable rabbitmq_management")
    c.sudo("rabbitmqctl add_user btcnewstoday abc_abc_123_abc_abc_123-abc_abc_123")
    c.sudo("rabbitmqctl set_user_tags btcnewstoday administrator")
    c.sudo("rabbitmqctl delete_user guest")
    c.sudo("rabbitmqctl set_permissions -p / btcnewstoday '.*' '.*' '.*'")


@task
def setup(c):
    c.sudo("""adduser --home /home/postgres --disabled-password --gecos "" postgres""")
    c.sudo("adduser postgres sudo")

    c.sudo("apt-get update -y")
    c.sudo("apt-get update -y")
    c.sudo("apt-get update -y")
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
    c.sudo("chmod a+w /etc/postgresql/14/main/postgresql.conf")
    c.sudo(
        """echo "listen_addresses = '*'" >> /etc/postgresql/14/main/postgresql.conf"""
    )
    c.sudo("chmod a+w /etc/postgresql/14/main/pg_hba.conf")
    c.sudo(
        """echo "host  all  all 0.0.0.0/0 md5" >> /etc/postgresql/14/main/pg_hba.conf"""
    )
    c.run(
        "echo 'localhost:5432:btcnewstoday:btcnewstoday:abc_abc_123_abc_abc_123-abc_abc_123' >> ~/.pgpass"
    )
    c.run(
        "echo 'localhost:5432:btcnewstoday:postgres:abc_abc_123_abc_abc_123-abc_abc_123' >> ~/.pgpass"
    )
    c.run("chmod 600 ~/.pgpass")
    c.sudo("service postgresql restart")


@task
def setup_postgres(c, env=os.environ):
    c.run(
        dedent(
            """\
            psql -U postgres postgres <<OMG
            CREATE USER btcnewstoday password 'abc_abc_123_abc_abc_123-abc_abc_123';
            CREATE DATABASE btcnewstoday;
            GRANT ALL PRIVILEGES ON DATABASE btcnewstoday TO btcnewstoday;
            GRANT ALL ON SCHEMA public TO btcnewstoday;
            OMG
           """
        ),
        env=env,
    )
    # c.sudo("systemctl restart postgresql")
    c.run(
        "echo 'localhost:5432:btcnewstoday:btcnewstoday:abc_abc_123_abc_abc_123-abc_abc_123' >> ~/.pgpass"
    )
    c.run(
        "echo 'localhost:5432:btcnewstoday:postgres:abc_abc_123_abc_abc_123-abc_abc_123' >> ~/.pgpass"
    )
    c.run("chmod 600 ~/.pgpass")


@task
def aws_cli(c, env=os.environ):
    with c.cd("/tmp"):
        c.run(
            'curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"'
        )
        c.run("unzip awscliv2.zip")
        c.run("sudo ./aws/install")


@task
def aws_cli_credentials(c, env=os.environ):
    aws_access_key_id = os.environ["AWS_ACCESS_KEY_ID"]
    aws_secret_access_key = os.environ["AWS_SECRET_ACCESS_KEY"]
    c.run("mkdir -p .aws")
    c.run("echo '[default]' > .aws/credentials")
    c.run(f"echo 'aws_access_key_id = {aws_access_key_id}' >> .aws/credentials")
    c.run(f"echo 'aws_secret_access_key = {aws_secret_access_key}' >> .aws/credentials")
    c.run("ls .aws")


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

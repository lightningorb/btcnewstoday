import os
import arrow
from invoke import task
import requests
import boto3
from textwrap import dedent


@task
def write_env(c, prerender, ssr, csr, snapshot, aid, dest):
    env = dedent(
        f"""\
    VITE_SNAPSHOT = {snapshot}
    VITE_AID = {aid}
    VITE_PRERENDER = {prerender}
    VITE_SSR = {ssr}
    VITE_CSR = {csr}
    """
    )
    print(env)
    print(dest)
    with c.cd(dest):
        with open(dest, "w") as w:
            w.write(env)


@task
def write_plain_env(c, prerender, ssr, csr, dest):
    env = dedent(
        f"""\
    VITE_PRERENDER = {prerender}
    VITE_SSR = {ssr}
    VITE_CSR = {csr}
    """
    )
    print(env)
    print(dest)
    with c.cd(dest):
        with open(dest, "w") as w:
            w.write(env)


class BuildSettings:
    def __init__(self, base, destination):
        self.base = base
        self.destination = destination


@task()
def snapshot(c, env=os.environ):
    with c.cd("src/svelte_site"):
        assert env["bndev_bucket"]
        today = arrow.utcnow().format("YYYY-MM-DD")
        short = requests.get(f"http://localhost:8000/api/articles?date={today}").json()
        long = requests.get(
            f"http://localhost:8000/api/articles?longform=true&date={today}"
        ).json()
        articles = [x["id"] for x in short + long]
        main_page_settings = BuildSettings(base="", destination="")

        nvm = ". ~/.bash_profile && nvm use 16.14"
        # nvm = ". ~/.nvm/nvm.sh && nvm use 16.14"

        write_plain_env(
            c,
            prerender="true",
            ssr="true",
            csr="true",
            dest="/home/ubuntu/btcnewstoday_static/src/svelte_site/.env",
        )

        print(main_page_settings.base)
        c.run(
            ". ~/.nvm/nvm.sh && nvm use 16.14 && npm run build",
            warn=True,
            env=dict(BN_SVELTE_BASE=main_page_settings.base),
        )
        c.run(
            f"aws s3 cp build/ s3://{env['bndev_bucket']}/ --recursive",
        )

        for aid in articles:
            settings = BuildSettings(
                base=f"/{today}/{aid}",
                destination=f"{today}/{aid}",
            )
            write_env(
                c,
                prerender="true",
                ssr="true",
                csr="true",
                snapshot=today,
                aid=aid,
                dest="/home/ubuntu/btcnewstoday_static/src/svelte_site/.env",
            )
            c.run("rm -rf build")
            print(settings.base)
            c.run(
                ". ~/.nvm/nvm.sh && nvm use 16.14 && npm run build",
                warn=True,
                env=dict(BN_SVELTE_BASE=settings.base),
            )
            c.run(
                f"aws s3 cp build/ s3://{env['bndev_bucket']}/{settings.destination} --recursive",
            )
            c.run("rm -rf build")


@task()
def snapshot_past(c):
    with c.cd("src/svelte_site"):
        bndev_bucket = os.environ["bndev_bucket"]
        now = arrow.utcnow().replace(hour=0, minute=0, second=0)
        start_date = now.shift(days=-3)
        dates = [start_date.format("YYYY-MM-DD")]
        while True:
            start_date = start_date.shift(days=1)
            if start_date.format("YYYY-MM-DD") == arrow.utcnow().replace(
                hour=0, minute=0, second=0
            ).format("YYYY-MM-DD"):
                break
            print(start_date)
            dates.append(start_date.format("YYYY-MM-DD"))

        print(dates)
        env = {}

        for date in dates:
            short = requests.get(
                f"http://localhost:8000/api/articles?date={date}"
            ).json()
            long = requests.get(
                f"http://localhost:8000/api/articles?longform=true&date={date}"
            ).json()
            articles = [x["id"] for x in short + long]

            for aid in articles:
                bs = BuildSettings(
                    base=f"/{date}/{aid}",
                    destination=f"{date}/{aid}",
                )

                c.run("rm -rf build")
                print(bs.base)
                # nvm = ". ~/.bash_profile && nvm use 16.14"
                nvm = ". ~/.nvm/nvm.sh && nvm use 16.14"
                env.update(dict(BN_SVELTE_BASE=bs.base))
                attempts = 0
                write_env(
                    c,
                    prerender="true",
                    ssr="true",
                    csr="true",
                    snapshot=date,
                    aid=aid,
                    dest="/home/ubuntu/btcnewstoday_static/src/svelte_site/.env",
                )
                while attempts < 5:
                    ok = c.run(f"{nvm} && npm run build", env=env, warn=True).ok
                    if ok:
                        c.run(
                            f"aws s3 cp build/ s3://{bndev_bucket}/{bs.destination} --recursive",
                        )
                        break
                    c.run("rm -rf build")
                    attempts += 1


@task()
def create_daily_indices(c):
    with c.cd("src/svelte_site"):
        bndev_bucket = os.environ["bndev_bucket"]
        now = arrow.utcnow().replace(hour=0, minute=0, second=0)
        start_date = arrow.get("2022-11-11")
        dates = [start_date.format("YYYY-MM-DD")]
        while True:
            start_date = start_date.shift(days=1)
            dates.append(start_date.format("YYYY-MM-DD"))
            if start_date.format("YYYY-MM-DD") == arrow.utcnow().replace(
                hour=0, minute=0, second=0
            ).format("YYYY-MM-DD"):
                break
            print(start_date)

        print(dates)
        env = {}

        for date in dates:
            short = requests.get(
                f"http://localhost:8000/api/articles?date={date}"
            ).json()
            long = requests.get(
                f"http://localhost:8000/api/articles?longform=true&date={date}"
            ).json()
            articles = [x["id"] for x in short + long]
            with open("/tmp/index.html", "w") as w:
                items = "<br>".join(
                    f'<a href="/{date}/{x}">/{date}/{x}</a>' for x in articles
                )
                content = dedent(
                    f"""\
                        <html>
                        {items}
                        </html>"""
                )
                w.write(content)
                print(content)
            c.run(
                f"aws s3 cp /tmp/index.html s3://{bndev_bucket}/{date}/",
            )


@task()
def snapshot_past_remote(c):
    with c.cd("btcnewstoday_static"):
        c.run(
            ". src/api/venv/bin/activate && env bndev_bucket=btcnewstoday fab snapshot.snapshot-past"
        )


@task()
def snapshot_remote(c):
    with c.cd("btcnewstoday_static"):
        c.run(
            ". src/api/venv/bin/activate && env bndev_bucket=btcnewstoday fab snapshot.snapshot"
        )

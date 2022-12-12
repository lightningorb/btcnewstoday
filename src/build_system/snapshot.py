import arrow
from invoke import task
import requests
import boto3


class BuildSettings:
    def __init__(self, base, destination):
        self.base = base
        self.destination = destination


@task()
def snapshot(c):
    with c.cd("src/svelte_site"):
        latest_snapshot = requests.get(
            "http://localhost:8000/api/latest_snapshot/"
        ).json()
        if latest_snapshot:
            today = arrow.utcnow().format("YYYY-MM-DD")
            print(today, f"_{latest_snapshot}_")
            if latest_snapshot.split(":")[0] != today:
                print("No DB snapshot for today. Refusing to upload.")
                return

            settings = [
                BuildSettings(base="", destination=""),
                BuildSettings(
                    base=latest_snapshot, destination=f"snapshots/{latest_snapshot}"
                ),
            ]

            for bs in settings:
                c.run("rm -rf build")
                c.run(". ~/.bash_profile && nvm use 16.14 && npm run build", warn=True)
                c.run(
                    f"aws s3 cp build/ s3://btcnewstoday/{bs.destination} --recursive",
                )
                c.run("rm -rf build")

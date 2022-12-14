import os
import arrow
from invoke import task
import requests
import boto3


"""
BN Snapshot mechanism:

The site takes a snapshot every 4 hours, the format is like so:


------------------------------------------------------------------------------------------------
H 0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16  17  18  19  20  21  22  23
------------------------------------------------------------------------------------------------
  D:0             D:2             D:3             D:4             D:5             D:6
          /\


"""


class BuildSettings:
    def __init__(self, base, destination):
        self.base = base
        self.destination = destination


@task()
def snapshot(c):
    with c.cd("src/svelte_site", env=os.environ):
        assert env["bndev_bucket"]
        latest_snapshot = requests.get(
            "http://localhost:8000/api/latest_snapshot/"
        ).json()
        if latest_snapshot:
            today = arrow.utcnow().format("YYYY-MM-DD")
            if latest_snapshot.split(":")[0] != today:
                print("No DB snapshot for today. Refusing to upload.")
                return

            settings = [
                BuildSettings(
                    base=f"/{latest_snapshot}",
                    destination=f"{latest_snapshot}",
                ),
                BuildSettings(base="", destination=""),
            ]

            for bs in settings:
                c.run("rm -rf build")
                print(bs.base)
                c.run(
                    ". ~/.nvm/nvm.sh && nvm use 16.14 && npm run build",
                    warn=True,
                    env=dict(BN_SVELTE_BASE=bs.base),
                )
                c.run(
                    f"aws s3 cp build/ s3://{env['bndev_bucket']}/{bs.destination} --recursive",
                )
                c.run("rm -rf build")

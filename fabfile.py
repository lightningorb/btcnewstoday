from invoke import task
from fabric import Connection
import os
from pathlib import Path


@task
def deploy(_):
    cert = (Path(os.getcwd()) / "btcnewstoday.cer").as_posix()
    with Connection(
        "btcnews.today", connect_kwargs={"key_filename": cert}, user="ubuntu"
    ) as c:
        c.run(f"uname -a", warn=True)

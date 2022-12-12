import re
import os
from fabric import Connection
from invoke import task, Context, Collection
from src.build_system.monkey_patch import fix_annotations

fix_annotations()


from src.build_system import provision
from src.build_system import configure
from src.build_system import build
from src.build_system import snapshot


@task(
    help=dict(
        instance_type="EC2 instance type, recommended: t3.medium",
        region="The region, e.g us-west-2",
        availability_zone="Exact zone, e.g if you're using us-west-1 as your default zone, this has to be e.g us-west-2a",
        name="EC2 instances have names, a good name would be mainnet",
        security_group_name="Name of the security group",
        keypair_name="Name of the keypair for ssh-ing",
        ami="Which AMI to use.. look it up manually using EC2 create instance in console",
    )
)
def deploy(
    c,
    instance_type: str,
    availability_zone: str,
    region: str,
    keypair_name: str,
    security_group_name: str,
    name: str,
    ami: str,
):
    ip = provision.create(
        c,
        instance_type=instance_type,
        availability_zone=availability_zone,
        region=region,
        keypair_name=keypair_name,
        security_group_name=security_group_name,
        name=name,
        ami=ami,
    )
    return
    with Connection(
        ip,
        **dict(connect_kwargs={"key_filename": f"{keypair_name}.pem"}, user="ubuntu"),
    ) as connection:
        configure.main(connection)
        build.main(connection)
        print(f"Site deployed to: http://{ip}")


namespace = Collection(deploy, provision, configure, build, snapshot)

import os
from time import sleep
from invoke import task
from fabric import Connection
from textwrap import dedent
import socket

import boto3
from botocore.exceptions import ClientError


@task(
    help=dict(
        name="The EC2 key-pair to ssh into this node",
        region="Region in which to create keypair",
    )
)
def create_keypair(c, name, region):
    """
    Create a key-pair called 'name' in given region
    """
    client = boto3.client("ec2", region_name=region)
    ec2 = boto3.resource("ec2", region_name=region)

    response = ec2.create_key_pair(KeyName=name)
    with open(f"{name}.pem", "w") as file:
        file.write(response.key_material)
    os.chmod(f"{name}.pem", 0o400)


@task
def describe_keypairs(c, region):
    """
    Print and retrieve all key-pairs for default AWS region
    """
    client = boto3.client("ec2", region_name=region)
    ec2 = boto3.resource("ec2", region_name=region)
    response = client.describe_key_pairs()
    print(response)
    return response


@task
def describe_elastic_ips(c, region):
    """
    Print and retrieve all key-pairs for default AWS region
    """
    client = boto3.client("ec2", region_name=region)
    ec2 = boto3.resource("ec2", region_name=region)
    response = client.describe_addresses()
    for address in response["Addresses"]:
        print(address["PublicIp"])


@task(help=dict(name="The EC2 key-pair to delete"))
def delete_keypair(c, name, region):
    """
    Delete a key-pair called 'name' in the default AWS region
    """
    client = boto3.client("ec2", region_name=region)
    ec2 = boto3.resource("ec2", region_name=region)
    response = client.delete_key_pair(KeyName=name)
    print("deleted keypair")
    print(response)


@task
def create_security_group(c, name: str, region):
    """
    Create the security group. This is the AWS EC2 level
    firewall protection that prevents the outside world from connecting
    to your node. Please note this is created in your default region.
    """
    client = boto3.client("ec2", region_name=region)
    ec2 = boto3.resource("ec2", region_name=region)

    response = client.describe_vpcs()
    vpc_id = response.get("Vpcs", [{}])[0].get("VpcId", "")

    try:
        response = client.create_security_group(
            GroupName=name,
            Description="security group for btcnews.today",
            VpcId=vpc_id,
        )
        security_group_id = response["GroupId"]
        print("Security Group Created %s in vpc %s." % (security_group_id, vpc_id))

        data = client.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {
                    "IpProtocol": pr,
                    "FromPort": p,
                    "ToPort": p,
                    "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
                }
                for p, pr in [
                    (22, "tcp"),  # SSH
                    (80, "tcp"),  # HTTP
                    (443, "tcp"),  # HTTPS
                    (60000, "udp"),  # mosh
                    (60001, "udp"),  # mosh
                    (60002, "udp"),  # mosh
                ]
            ],
        )
        print("Ingress Successfully Set %s" % data)
    except ClientError as e:
        print(e)


def get_public_ip(instance_id, region):
    """
    Return the public ip address for given instance
    """
    client = boto3.client("ec2", region_name=region)
    ec2 = boto3.resource("ec2", region_name=region)

    for reservation in client.describe_instances(InstanceIds=[instance_id]).get(
        "Reservations"
    ):
        for instance in reservation["Instances"]:
            return instance.get("PublicIpAddress")


@task(
    help=dict(
        instance_type="EC2 instance type, recommended: t3.medium",
        region="The region, e.g us-west-2",
        availability_zone="Exact zone, e.g if you're using us-west-1 as your default zone, this has to be e.g us-west-2a",
        name="EC2 instances have names, a good name would be mainnet",
        security_group_name="Name of the security group",
        keypair_name="Name of the keypair for ssh-ing",
        ami="Which AMI to use.. look it up manually using EC2 create instance in console",
        elastic_ip="The elastic ip to associate",
    )
)
def create(
    c,
    instance_type: str,
    availability_zone: str,
    region: str,
    keypair_name: str,
    security_group_name: str,
    name: str,
    ami: str,
    elastic_ip: str,
):
    """
    Create the AWS EC2 instance, and wait until it's running, has a public
    IP, and we're able to SSH into it.
    """
    client = boto3.client("ec2", region_name=region)
    ec2 = boto3.resource("ec2", region_name=region)

    print("Creating instance...")
    print(f"using AMI: {ami}")
    inst = ec2.create_instances(
        Placement={"AvailabilityZone": availability_zone},
        TagSpecifications=[
            {
                "ResourceType": "instance",
                "Tags": [
                    {"Key": "Name", "Value": name},
                ],
            },
        ],
        ImageId=ami,
        BlockDeviceMappings=[
            {
                "DeviceName": "/dev/sda1",
                "Ebs": {
                    "DeleteOnTermination": True,
                    "VolumeSize": 25,
                    "VolumeType": "io2",
                    "Iops": 200,
                    "Encrypted": True,
                },
            },
        ],
        MinCount=1,
        MaxCount=1,
        InstanceType=instance_type,
        KeyName=keypair_name,
        SecurityGroupIds=[security_group_name],
    )[0]

    print("waiting until running..")
    inst.wait_until_running()

    while True:
        ip = get_public_ip(inst.id, region=region)
        if ip:
            print(ip)
            break
        print("waiting for ip address")
        sleep(5)

    print(f"ip address: {ip}")

    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((ip, 22))
        if result == 0:
            print("Instance is UP & accessible on port 22, the IP address is:  ", ip)
            break
        else:
            print("instance is still down retrying...")
            sleep(5)

    connection = Connection(
        ip,
        connect_timeout=60,
        connect_kwargs={"key_filename": f"{keypair_name}.pem"},
        user="ubuntu",
    )

    while True:
        try:
            connection.run("whoami")
            break
        except:
            print("Cannot SSH.. let's wait")
            sleep(5)

    response = client.associate_address(InstanceId=inst.id, PublicIp=elastic_ip)
    print(response)

    print(f"Created instance: {inst.id}, {ip} with elastic ip: {elastic_ip}")

    return elastic_ip


def get_instance(name, region):
    """
    Return the aws instance for the given instance name
    """
    client = boto3.client("ec2", region_name=region)
    ec2 = boto3.resource("ec2", region_name=region)
    instances = ec2.instances.filter(
        Filters=[
            {"Name": "tag:Name", "Values": [name]},
            {"Name": "instance-state-name", "Values": ["running"]},
        ]
    )
    return next(iter(instances), None)


@task()
def kill(c, name: str, region: str, force: bool = False):
    """
    Delete the node.
    """
    client = boto3.client("ec2", region_name=region)
    ec2 = boto3.resource("ec2", region_name=region)
    instance = get_instance(name=name, region=region)
    if not instance:
        print(f"no instance {name} found")
        exit()
    if force or "y" in input(f"kill instance {name}? y/n: "):
        client.stop_instances(InstanceIds=[instance.id])
        client.terminate_instances(InstanceIds=[instance.id])
        print(f"Stopped instance: {instance.id}")
        print(f"Terminated instance: {instance.id}")

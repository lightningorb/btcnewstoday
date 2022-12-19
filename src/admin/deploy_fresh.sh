#!/bin/bash

# Deployment script, to deploy a fresh instance of BN

. src/api/venv/bin/activate

# If a key-pair already exists, you can comment this out
# fab provision.create-keypair --name ${bndev_name} --region ${bndev_region}

# If a security group already exists, you can comment his out
# fab provision.create-security-group --name ${bndev_name} --region ${bndev_region}

# Perform full deployment
fab provision.create \
            --name ${bndev_name} \
            --instance-type t2.medium \
            --availability-zone ${bndev_availability_zone} \
            --keypair-name ${bndev_name} \
            --security-group-name ${bndev_name} \
            --ami ${bndev_ami} \
            --region ${bndev_region} \
            --elastic-ip ${bndev_elastic_ip}

fab -i ${bndev_name}.pem -H ubuntu@${bndev_url} configure.setup
fab -i ${bndev_name}.pem -H ubuntu@${bndev_url} configure.aws-cli
# fab -i ${bndev_name}.pem -H ubuntu@${bndev_url} configure.generate-cert
# fab -i ${bndev_name}.pem -H ubuntu@${bndev_url} configure.copy-certs-to-s3
fab -i ${bndev_name}.pem -H ubuntu@${bndev_url} configure.get-certs-from-s3
fab -i ${bndev_name}.pem -H ubuntu@${bndev_url} build.supervisord-conf
fab -i ${bndev_name}.pem -H ubuntu@${bndev_url} build.build
fab -i ${bndev_name}.pem -H ubuntu@${bndev_url} build.build-static
fab -i ${bndev_name}.pem -H ubuntu@${bndev_url} build.nginx-conf
# fab -i ${bndev_name}.pem -H ubuntu@${bndev_url} build.cron
# fab -i ${bndev_name}.pem -H ubuntu@${bndev_url} snapshot.snapshot-remote
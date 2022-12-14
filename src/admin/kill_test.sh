#!/bin/bash

. src/api/venv/bin/activate

fab provision.kill --force --name ${bndev_name} --region ${bndev_region}
#!/bin/bash

. src/api/venv/bin/activate

fab provision.kill --force --name test --region us-west-2
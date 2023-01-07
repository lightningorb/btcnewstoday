import os
import unittest
import requests
import json
import pytest

host = os.environ["bndev_test_url"]

from bn_test_case import *


@pytest.mark.order(1)
def test_registration():
    r = requests.post(
        f"{host}/api/register/",
        data=json.dumps(
            {
                "username": "test_account_test123",
                "password": "test123test123test123",
                "twitter_username": "jack",
            }
        ),
    )
    j = r.json()
    if j == {"detail": "Username already taken"}:
        assert j == {"detail": "Username already taken"}
    else:
        assert j["access_token"]
        assert j["token_type"] == "bearer"


@pytest.mark.order(2)
def test_login():
    j = requests.request(
        "POST",
        f"{host}/token/",
        data={
            "username": "test_account_test123",
            "password": "test123test123test123",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    ).json()
    assert j["access_token"]
    assert j["token_type"] == "bearer"

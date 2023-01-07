import os
import pytest
import requests
import json


class BNTestCase:
    @pytest.fixture
    def host(self, request):
        host = os.environ["bndev_test_url"]
        yield host

    @pytest.fixture
    def access_token(self, request):
        host = os.environ["bndev_test_url"]
        requests.post(
            f"{host}/api/register/",
            data=json.dumps(
                {
                    "username": "test_account_test123",
                    "password": "test123test123test123",
                    "twitter_username": "jack",
                }
            ),
        )
        j = requests.request(
            "POST",
            f"{host}/token/",
            data={
                "username": "test_account_test123",
                "password": "test123test123test123",
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        ).json()
        yield j["access_token"]

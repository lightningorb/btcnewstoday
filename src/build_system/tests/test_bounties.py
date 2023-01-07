import unittest
import requests
import json
import pytest

from bn_test_case import *


class TestBounties(BNTestCase):
    @pytest.mark.order(8)
    def test_bounties(self, access_token, host):
        r = requests.get(
            f"{host}/api/users/me/", headers={"Authorization": f"Bearer {access_token}"}
        )
        j = r.json()
        assert j == {
            "username": "test_account_test123",
            "role": "admin",
            "twitter_uid": "123",
            "twitter_username": "jack",
            "num_tweets": 1,
            "num_notes": 1,
            "redeemable_sats": 750,
            "redeemed_sats": 0,
        }

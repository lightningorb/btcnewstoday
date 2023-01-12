import unittest
import requests
import json
import pytest

from bn_auth_test_case import *


class TestBounties(BNContributedArticleTestCase):
    def test_bounties(self, host, access_token, note_tweet):
        r = requests.get(
            f"{host}/api/users/me/", headers={"Authorization": f"Bearer {access_token}"}
        )
        j = r.json()
        assert j == {
            "username": "test_account_test123",
            "role": "admin",
            "twitter_uid": "123",
            "twitter_username": "jack",
            "ln_address": "movingmine80@walletofsatoshi.com",
            "num_notes_approved": 1,
            "num_tweets_approved": 1,
            "num_tweets": 1,
            "num_notes": 1,
            "redeemable_sats": 200,
            "redeemed_sats": 0,
        }

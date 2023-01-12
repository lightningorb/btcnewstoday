import os
import unittest
import requests
import json
import pytest

from bn_auth_test_case import *


class TestArticles(BNArticleTestCase):
    def test_posting(self, article):
        j = article
        assert j["author"] == "An amazing author"
        assert j["category"] == "Something or the other"
        assert j["is_draft"] == False
        assert j["is_longform"] == False
        assert j["image"] == ""
        assert j["title"] == "Test Article 123"
        assert j["blurb"] == "This is a Test Article 123"
        assert (
            j["link"]
            == "https://www.coindesk.com/markets/2023/01/01/what-will-it-take-for-bitcoin-mining-companies-to-survive-in-2023/"
        )
        assert j["outlet"] == "Somewhere magical"

    def test_image(self, access_token, host, article):
        requests.get(f"{host}/api/images/")
        r = requests.get(f"{host}/api/articles/")
        j = r.json()
        assert (
            j[0]["image"]
            == "https://www.coindesk.com/resizer/Qexn1SWbVkkjlTMY2O6VSaAn0Rw=/1200x628/center/middle/cloudfront-us-east-1.images.arcpublishing.com/coindesk/JZ3RPH7C5FCOZHDZSR5NEUKMZM.jpg"
        )

    def test_search(self, access_token, host, article):
        requests.get(f"{host}/api/meta/")
        requests.get(f"{host}/api/meta/index/")
        r = requests.get(f"{host}/api/meta/search/?term=Bitcoin Mining")
        j = r.json()
        assert "mining" in j[0]["highlights"]

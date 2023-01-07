import os
import unittest
import requests
import json
import pytest

from bn_test_case import *


class TestArticles(BNTestCase):
    @pytest.mark.order(3)
    def test_posting(self, access_token, host):
        r = requests.post(
            f"{host}/api/articles/",
            headers={"Authorization": f"Bearer {access_token}"},
            data=json.dumps(
                {
                    "title": "Test Article 123",
                    "blurb": "This is a Test Article 123",
                    "link": "https://www.coindesk.com/markets/2023/01/01/what-will-it-take-for-bitcoin-mining-companies-to-survive-in-2023/",
                    "outlet": "Somewhere magical",
                    "author": "An amazing author",
                    "category": "Something or the other",
                    "is_draft": False,
                    "is_longform": False,
                }
            ),
        )
        j = r.json()
        if j == {"detail": "Article with this link already exists"}:
            assert j == {"detail": "Article with this link already exists"}
        else:
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

    @pytest.mark.order(4)
    def test_add_tweet(self, access_token, host):
        r = requests.post(
            f"{host}/api/tweets/",
            headers={"Authorization": f"Bearer {access_token}"},
            data=json.dumps(
                dict(
                    username="jack",
                    text="just setting up my twttr",
                    article_id="1",
                    tweet_id="20",
                )
            ),
        )
        j = r.json()
        assert j == {
            "tweet_id": 20,
            "username": "jack",
            "text": "just setting up my twttr",
            "article_id": 1,
        }

    @pytest.mark.order(5)
    def test_add_note(self, access_token, host):
        r = requests.post(
            f"{host}/api/nostr_notes/",
            headers={"Authorization": f"Bearer {access_token}"},
            data=json.dumps(
                dict(
                    article_id="1",
                    text="This is my funky note",
                    note_id="note1cwcagc75tv3vucrxz3092mxn32phkyc9glr3mt9x6akeag2w7rys2xn0f2",
                    username="DerekRoss",
                )
            ),
        )
        j = r.json()
        assert j == {
            "article_id": 1,
            "text": "This is my funky note",
            "note_id": "note1cwcagc75tv3vucrxz3092mxn32phkyc9glr3mt9x6akeag2w7rys2xn0f2",
            "username": "DerekRoss",
        }

    @pytest.mark.order(6)
    def test_image(self, access_token, host):
        requests.get(f"{host}/api/images/")
        r = requests.get(f"{host}/api/articles/")
        j = r.json()
        assert (
            j[0]["image"]
            == "https://www.coindesk.com/resizer/Qexn1SWbVkkjlTMY2O6VSaAn0Rw=/1200x628/center/middle/cloudfront-us-east-1.images.arcpublishing.com/coindesk/JZ3RPH7C5FCOZHDZSR5NEUKMZM.jpg"
        )

    @pytest.mark.order(7)
    def test_search(self, access_token, host):
        requests.get(f"{host}/api/meta/")
        requests.get(f"{host}/api/meta/index/")
        r = requests.get(f"{host}/api/meta/search/?term=Bitcoin Mining")
        j = r.json()
        assert "mining" in j[0]["highlights"]

import os
import pytest
import requests
import json


class BNAuthTestCase:
    @pytest.fixture
    def host(self, request):
        host = os.environ["bndev_test_url"]
        yield host

    @pytest.fixture
    def access_token(self, request):
        host = os.environ["bndev_test_url"]
        j = requests.post(
            f"{host}/api/register/",
            data=json.dumps(
                {
                    "username": "test_account_test123",
                    "password": "test123test123test123",
                    "ln_address": "movingmine80@walletofsatoshi.com",
                    "twitter_username": "jack",
                }
            ),
        ).json()
        assert j["access_token"]
        assert j["token_type"] == "bearer"
        j = requests.request(
            "POST",
            f"{host}/token/",
            data={
                "username": "test_account_test123",
                "password": "test123test123test123",
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        ).json()
        access_token = j["access_token"]
        yield access_token
        requests.delete(
            f"{host}/api/users/me/",
            headers={"Authorization": f"Bearer {access_token}"},
        )


class BNArticleTestCase(BNAuthTestCase):
    @pytest.fixture
    def article(self, access_token, host):
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
        yield j
        requests.post(
            f"{host}/api/delete_article/{j['id']}",
            headers={"Authorization": f"Bearer {access_token}"},
        )


def get_tweet(access_token, host, article):
    r = requests.post(
        f"{host}/api/tweets/",
        headers={"Authorization": f"Bearer {access_token}"},
        data=json.dumps(
            dict(
                username="jack",
                text="just setting up my twttr",
                article_id=article["id"],
                tweet_id="20",
            )
        ),
    )
    j = r.json()
    assert j == {
        "tweet_id": 20,
        "username": "jack",
        "text": "just setting up my twttr",
        "article_id": article["id"],
    }
    return j


def get_note(access_token, host, article):
    r = requests.post(
        f"{host}/api/nostr_notes/",
        headers={"Authorization": f"Bearer {access_token}"},
        data=json.dumps(
            dict(
                article_id=article["id"],
                text="This is my funky note",
                note_id="note1cwcagc75tv3vucrxz3092mxn32phkyc9glr3mt9x6akeag2w7rys2xn0f2",
                username="DerekRoss",
            )
        ),
    )
    j = r.json()
    assert j == {
        "article_id": article["id"],
        "text": "This is my funky note",
        "note_id": "note1cwcagc75tv3vucrxz3092mxn32phkyc9glr3mt9x6akeag2w7rys2xn0f2",
        "username": "DerekRoss",
    }
    return j


class BNContributedArticleTestCase(BNArticleTestCase):
    @pytest.fixture
    def tweet(self, access_token, host, article):
        return get_tweet(access_token, host, article)

    @pytest.fixture
    def note(self, access_token, host, article):
        return get_note(access_token, host, article)

    @pytest.fixture
    def note_tweet(self, access_token, host, article):
        return get_note(access_token, host, article), get_tweet(
            access_token, host, article
        )

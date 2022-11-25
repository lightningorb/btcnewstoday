import requests
import simplexml
import arrow
import json


def ingest_decrypt():
    r = requests.get("https://decrypt.co/feed").text
    d = simplexml.loads(r)
    for channel in list(d["rss"]["channel"].values()):
        if type(channel) is list:
            for item in channel:
                print("=" * 100)
                print(item["title"])
                date = arrow.get(
                    item["pubDate"][5:-6], "DD MMM YYYY HH:mm:ss"
                ).timestamp()

                doc = {
                    "title": item["title"],
                    "blurb": item["description"],
                    "link": item["link"],
                    "outlet": "Decrypt.co",
                    "author": item.get("dc:author"),
                    "category": item["category"],
                    "is_draft": True,
                    "is_longform": False,
                    "date": date,
                }
                headers = {
                    "Content-Type": "application/json",
                }
                r = requests.post(
                    "http://localhost:8000/api/articles/",
                    data=json.dumps(doc),
                    headers=headers,
                )
                print(r.text)


ingest_decrypt()

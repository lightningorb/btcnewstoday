import requests
import simplexml
import arrow
import json


def ingest():
    url = "https://volatilityviews.libsyn.com/rss"
    r = requests.get(url).text
    d = simplexml.loads(r)
    for channel in list(d["rss"]["channel"].values()):
        if type(channel) is list:
            for item in channel:
                if type(item) == dict and "title" in item and "enclosure" in item:
                    print("=" * 100)
                    print(item["title"])
                    date = arrow.get(
                        item["pubDate"][5:-6], "DD MMM YYYY HH:mm:ss"
                    ).timestamp()

                    doc = {
                        "episode_title": item["title"],
                        "link": item["link"],
                        "outlet": item.get('itunes:author', 'Volatility Views'),
                        "is_draft": True,
                        "date": date,
                    }

                    headers = {
                        "Content-Type": "application/json",
                    }
                    r = requests.post(
                        "http://localhost:8000/api/podcasts/",
                        data=json.dumps(doc),
                        headers=headers,
                    )
                    print(r.text)


ingest()

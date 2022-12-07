import datetime
import re
import requests
from pathlib import Path
import json
import arrow
from string import ascii_lowercase

# Import the required modules
import requests
import xml.etree.ElementTree as ET


class Feed:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.clean_name = "".join(("_", x)[x.lower() in ascii_lowercase] for x in name)
        self.rss_path = Path("pod_feeds/" + self.clean_name + ".rss")
        self.content = ""

    def read(self, cached=False):
        get_fresh = (not self.rss_path.exists()) or (not cached)
        Path("pod_feeds").mkdir(exist_ok=True)
        print("Get Fresh?", get_fresh)
        if get_fresh:
            r = requests.get(self.url)
            if r.status_code == 200:
                feed_data = "\n".join([x for x in r.text.split("\n") if x])
                with self.rss_path.open("w") as w:
                    w.write(feed_data)
                    self.content = feed_data
            else:
                print("Could not get:")
                print(r.status_code)
                print(self.url)
        else:
            with self.rss_path.open() as f:
                self.content = f.read()

    def parse(self, cached=False):
        self.read(cached=cached)
        print("=" * 100)
        print(self.name)
        root = ET.fromstring(self.content)

        def find_text(item, key):
            v = item.find(key)
            if v:
                return b.text

        def find_enclosure(item, key="enclosure"):
            enclosure = item.find(key)
            if not enclosure is None:
                return enclosure.attrib["url"]

        for item in root.iter("item"):
            # print("=" * 100)
            title = item.find("title").text
            # print(title)
            pubDate = item.find("pubDate").text
            formats = ["%a, %d %b %Y %H:%M:%S %Z", "%a, %d %b %Y %H:%M:%S %z"]
            for f in formats:
                try:
                    date = datetime.datetime.strptime(pubDate, f)
                    break
                except:
                    pass
            delta = datetime.datetime.now() - date.replace(tzinfo=None)
            if delta.days > 2:
                continue
            date = int(date.timestamp())
            link = find_text(item, "link")
            enclosure = find_enclosure(item)
            link = enclosure or link
            # print(link)
            outlet = (
                find_text(item, "itunes:author")
                or find_text(item, "author")
                or self.name
            )

            print([title, date, link, outlet])

            if all([title, date, link, outlet]):
                doc = {
                    "episode_title": title,
                    "link": link,
                    "outlet": outlet,
                    "is_draft": True,
                    "date": date,
                }
                # print(doc)
                headers = {
                    "Content-Type": "application/json",
                }
                r = requests.post(
                    "http://localhost:8000/api/podcasts/",
                    data=json.dumps(doc),
                    headers=headers,
                )
                print(r.text)


def get_feeds():
    feeds = []
    with open("BN-podcast-list-Rev1.csv") as f:
        for line in f.readlines()[1:]:
            _, name, url = [x.strip() for x in line.split(",")]
            if not all([name, url]):
                continue
            feeds.append(Feed(name=name, url=url))
    return feeds


def main():
    feeds = get_feeds()
    for f in feeds:
        f.parse(cached=False)
        print("#" * 500)


if __name__ == "__main__":
    main()

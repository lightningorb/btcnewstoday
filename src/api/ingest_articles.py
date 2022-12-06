import re
import requests
from pathlib import Path
import json
import arrow
# Import the required modules
import requests
import xml.etree.ElementTree as ET

class Feed:
    def __init__(self, name, content):
        self.name = name
        self.content = content

def get_feeds(cached=False):
    feeds = []
    with open("article_feeds.txt") as f:
        for line in f.readlines():
            line = line.strip()
            domain = re.match(r'https://(www\.)?([^\.]*)', line).groups()[1]
            rss_path = Path('feeds/' + domain + '.rss')
            get_fresh = (not rss_path.exists()) or (not cached)
            content = ''
            if get_fresh:
                r = requests.get(line)
                if r.status_code == 200:
                    feed_data = '\n'.join([x for x in r.text.split('\n') if x])
                    with rss_path.open('w') as w:
                        w.write(feed_data)
                        content = feed_data
                else:
                    print("Could not get:")
                    print(r.status_code)
                    print(line)
            else:
                with rss_path.open() as f:
                    content = f.read()
            if content and domain:
                feeds.append(Feed(name=domain, content=content))
    return feeds

def parse_feed(feed):
    print("="*100)
    print(feed.name)
    root = ET.fromstring(feed.content)

    for item in root.iter('item'):
        author = (item.find('author') or item.find('dc:author'))
        if author:
            author = author.text
        date = arrow.get(
            item.find("pubDate").text[5:-6], "DD MMM YYYY HH:mm:ss"
        ).timestamp()

        obj = {
            'title': item.find('title').text,
            'blurb': item.find('description').text or '',
            'link': item.find('link').text,
            'author': author,
            'category': item.find('category').text,
            "is_draft": True,
            "is_longform": False,
            "outlet": feed.name,
            'date': date
        }
        headers = {
            "Content-Type": "application/json",
        }
        r = requests.post(
            "http://localhost:8000/api/articles/",
            data=json.dumps(obj),
            headers=headers,
        )
        print(r.text)

def parse_feeds(feeds):
    for f in feeds:
        parse_feed(f)

def main():
    feeds = get_feeds()
    parse_feeds(feeds)

if __name__ == '__main__':
    main()
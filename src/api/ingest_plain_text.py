import shutil
import os
import arrow
import requests
from whoosh.qparser import QueryParser
from whoosh import index
from whoosh.index import create_in
from readabilipy import simple_json_from_html_string
from models import *
from whoosh.fields import TEXT, ID, Schema
from sqlmodel import select


def ingest_plain_text(session):
    articles = session.exec(select(Article).where(Article.is_draft == False)).all()
    for a in articles:
        if not a.meta:
            if "notable tweets" in a.title.lower():
                continue
            article_html = requests.get(a.link).text
            article = simple_json_from_html_string(article_html, use_readability=True)
            plain_text = " ".join(x["text"] for x in article["plain_text"])
            a.meta.append(Meta(article_id=a.id, type="plain_text", data=plain_text))
            a.meta.append(
                Meta(article_id=a.id, type="content", data=article["content"])
            )
            a.meta.append(
                Meta(
                    article_id=a.id, type="plain_content", data=article["plain_content"]
                )
            )
    session.commit()


schema = Schema(
    title=TEXT(stored=True),
    path=ID(stored=True),
    content=TEXT(stored=True),
    date=TEXT(stored=True),
)


def create_index(session):
    if os.path.exists("indexdir"):
        shutil.rmtree("indexdir")
    os.makedirs("indexdir")
    ix = create_in("indexdir", schema)
    writer = ix.writer()
    metas = session.exec(select(Meta).where(Meta.type == "plain_text")).all()
    for m in metas:
        date = arrow.get(m.article.date, tzinfo="UTC").format("YYYY-MM-DD")
        writer.add_document(
            title=m.article.title, path=f"{m.article.id}", content=m.data, date=date
        )
    writer.commit()


def search_index(session, term: str):
    ix = index.open_dir("indexdir")
    res = []
    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse(term)
        results = searcher.search(query, limit=100)
        return [
            dict(
                id=r["path"],
                date=r["date"],
                title=r["title"],
                highlights=r.highlights("content"),
            )
            for r in results
        ]

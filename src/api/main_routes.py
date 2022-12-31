import ssl
import os
import requests
import simplexml
import json
from typing import Optional, List
import arrow
from functools import lru_cache
from models import *
from role_checker import *
from auth_helpers import *

import time

from bs4 import BeautifulSoup
from traceback import print_exc
from fastapi import FastAPI, Request
from pydantic import BaseModel
from sqlalchemy.sql.expression import not_
from slowapi import Limiter, _rate_limit_exceeded_handler
from fastapi.middleware.cors import CORSMiddleware
from bn_secrets import *
from ingest_articles import main as ingest_articles_func
from ingest_podcasts import main as ingest_podcasts_func
from collections import namedtuple
from limiter import *

import ingest_plain_text
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from limiter import limiter
from fastapi import APIRouter
from db import *

router = APIRouter()


@router.on_event("shutdown")
def shutdown_event():
    # relay_manager.close_connections()
    pass


@router.on_event("startup")
def on_startup():
    # if os.path.exists("database.db"):
    #     os.unlink("database.db")
    create_db_and_tables()
    # add_fixtures()
    with Session(engine) as session:
        articles = session.exec(select(Article))
        for a in articles:
            if a.is_draft is None:
                a.is_draft = True
            for attr in ("category", "author", "image"):
                if getattr(a, attr) is None:
                    setattr(a, attr, "")
        session.commit()


@router.post(
    "/api/articles/",
    response_model=Optional[Article],
    dependencies=[Depends(allow_create_resource)],
)
def create_article(
    article: Article, current_user: User = Depends(get_current_active_user)
):
    with Session(engine) as session:
        articles = session.exec(
            select(Article).where(Article.link == article.link)
        ).all()
        if articles:
            raise HTTPException(
                status_code=400,
                detail="Article with this link already exists",
            )
        if not (
            article.link.startswith("https://") or article.link.startswith("http://")
        ):
            raise HTTPException(
                status_code=400,
                detail="Link looks invalid, it should contain http:// or https://",
            )
        for field in ["title", "blurb", "outlet"]:
            if not getattr(article, field):
                raise HTTPException(
                    status_code=400,
                    detail=f"field: {field} is required",
                )
        deleted_article = session.exec(
            select(ArticleDeleted).where(ArticleDeleted.link == article.link)
        ).all()
        if deleted_article:
            raise HTTPException(
                status_code=400,
                detail="This link was previously added, then deleted",
            )
        session.add(article)
        session.commit()
        print("added")
        session.refresh(article)
        return article


@router.post(
    "/api/delete_article/{article_id}/",
    dependencies=[Depends(allow_create_resource)],
)
def delete_article(
    article_id: int, current_user: User = Depends(get_current_active_user)
):
    with Session(engine) as session:
        db_article = session.exec(select(Article).where(Article.id == article_id)).one()
        if not db_article:
            print("Article ID not found")
            return None
        session.add(ArticleDeleted(link=db_article.link))
        for tweet in db_article.tweets:
            session.delete(tweet)
        session.delete(db_article)
        session.commit()
        print("deleted")


@router.post(
    "/api/update_article/{article_id}/",
    response_model=Optional[Article],
    dependencies=[Depends(allow_create_resource)],
)
def update_article(
    article: Article, current_user: User = Depends(get_current_active_user)
):
    with Session(engine) as session:
        db_article = session.exec(
            select(Article).where(Article.link == article.link)
        ).one()
        if not db_article:
            print("Article ID not found")
            return None
        db_article.title = article.title
        db_article.blurb = article.blurb
        db_article.link = article.link
        db_article.outlet = article.outlet
        db_article.category = article.category
        db_article.is_draft = article.is_draft
        db_article.is_longform = article.is_longform
        db_article.date = article.date
        session.commit()
        print("updated")
        session.refresh(db_article)
        return db_article


@router.post("/api/tweets/", response_model=Tweet)
def add_tweet(tweet: Tweet, current_user: User = Depends(get_current_active_user)):
    with Session(engine) as session:
        print(f"adding tweet: {tweet.id}")
        session.add(tweet)
        session.commit()
        session.refresh(tweet)
        return tweet


@router.post("/api/nostr_notes/", response_model=NostrNote)
def add_nostr_notes(
    nost_note: NostrNote, current_user: User = Depends(get_current_active_user)
):
    with Session(engine) as session:
        print(f"adding NostrNote: {nost_note.note_id}")
        session.add(nost_note)
        session.commit()
        session.refresh(nost_note)
        return nost_note


# , response_model=List[str]
@router.get("/api/articles/categories/")
def get_article_categories():
    session = Session(engine)
    query = select(Article.category.distinct())
    return set(session.exec(query).all()) - set([None]) | set(["BN: Tech & Dev"])


@router.get("/api/articles/", response_model=List[ArticleReadWithTweets])
def get_articles(
    longform: bool = False,
    is_draft: bool = False,
    limit: int = 25,
    date: str = None,
    category_include: str = "",
    category_exclude: str = "",
):
    if date is None:
        date = int(arrow.utcnow().shift(days=1).timestamp())
    else:
        date = int(arrow.get(date).shift(days=1).timestamp())

    session = Session(engine)
    query = (
        select(Article)
        .order_by(Article.date.desc())
        .limit(limit)
        .where(Article.is_longform == longform)
        .where(Article.is_draft == is_draft)
        .where(Article.date <= date)
    )

    if category_include:
        query = query.where(Article.category.in_(category_include.split(",")))

    if category_exclude:
        query = query.where(Article.category.not_in(category_exclude.split(",")))

    articles = session.exec(query).all()

    return articles


@router.get("/api/past_articles/")
def get_past_articles(date: str = None, limit: int = 100):
    from collections import defaultdict

    if date is None:
        date = int(arrow.utcnow().timestamp())
    else:
        date = int(arrow.get(date).shift(days=1).timestamp())

    dd = defaultdict(list)
    with Session(engine) as session:
        articles = session.exec(
            select(Article)
            .where(Article.is_draft == False)
            .where(Article.date <= date)
            .order_by(Article.date.desc())
            .limit(limit)
        ).all()
        for a in articles:
            date = int(
                arrow.get(a.date)
                .replace(hour=0, minute=0, second=0, microsecond=0)
                .timestamp()
            )
            dd[date].append(a)

        return [x for x in dict(dd).items()]


@router.post(
    "/api/podcasts/",
    response_model=Optional[Podcast],
    dependencies=[Depends(allow_create_resource)],
)
def create_podcast(
    podcast: Podcast, current_user: User = Depends(get_current_active_user)
):
    with Session(engine) as session:
        db_podcast = session.exec(
            select(Podcast).where(Podcast.link == podcast.link)
        ).all()
        if db_podcast:
            print("already exists")
            return None
        session.add(podcast)
        session.commit()
        session.refresh(podcast)
        return podcast


@router.post(
    "/api/update_podcast/",
    response_model=Optional[Podcast],
    dependencies=[Depends(allow_create_resource)],
)
def update_podcast(
    podcast: PodcastUpdate, current_user: User = Depends(get_current_active_user)
):
    with Session(engine) as session:
        db_podcast = session.exec(select(Podcast).where(Podcast.id == podcast.id)).one()
        if not db_podcast:
            print("Podcast ID not found")
            return None
        db_podcast.outlet = podcast.outlet
        db_podcast.is_draft = podcast.is_draft
        db_podcast.episode_title = podcast.episode_title
        session.commit()
        print("updated")
        session.refresh(db_podcast)
        return db_podcast


@router.post(
    "/api/jobs/",
    response_model=Job,
    dependencies=[Depends(allow_create_resource)],
)
def create_job(Job: Job, current_user: User = Depends(get_current_active_user)):
    with Session(engine) as session:
        session.add(Job)
        session.commit()
        session.refresh(Job)
        return Job


@router.post(
    "/api/events/",
    response_model=Event,
    dependencies=[Depends(allow_create_resource)],
)
def create_event(Event: Event, current_user: User = Depends(get_current_active_user)):
    with Session(engine) as session:
        session.add(Event)
        session.commit()
        session.refresh(Event)
        return Event


@router.post(
    "/api/delete_event/{event_id}/",
    dependencies=[Depends(allow_create_resource)],
)
def delete_event(event_id: int, current_user: User = Depends(get_current_active_user)):
    with Session(engine) as session:
        db_event = session.exec(select(Event).where(Event.id == event_id)).one()
        if not db_event:
            print("Event ID not found")
            return None
        session.delete(db_event)
        session.commit()
        print("deleted")


@router.post(
    "/api/delete_podcast/{podcast_id}/",
    dependencies=[Depends(allow_create_resource)],
)
def delete_podcast(
    podcast_id: int, current_user: User = Depends(get_current_active_user)
):
    with Session(engine) as session:
        db_podcast = session.exec(select(Podcast).where(Podcast.id == podcast_id)).one()
        if not db_podcast:
            print("Podcast ID not found")
            return None
        session.delete(db_podcast)
        session.commit()
        print("deleted")


@router.post(
    "/api/delete_job/{job_id}/",
    dependencies=[Depends(allow_create_resource)],
)
def delete_podcast(job_id: int, current_user: User = Depends(get_current_active_user)):
    with Session(engine) as session:
        db_job = session.exec(select(Job).where(Job.id == job_id)).one()
        if not db_job:
            print("Job ID not found")
            return None
        session.delete(db_job)
        session.commit()
        print("deleted")


@router.get("/api/podcasts/", response_model=List[Podcast])
def get_podcasts(is_draft: bool = False, limit: int = 25, date: str = None):
    if date is None:
        date = int(arrow.utcnow().timestamp())
    else:
        date = int(arrow.get(date).shift(days=1).timestamp())
    session = Session(engine)
    return session.exec(
        select(Podcast)
        .order_by(Podcast.date.desc())
        .limit(limit)
        .where(Podcast.date <= date)
        .where(Podcast.is_draft == is_draft)
    ).all()


@router.get("/api/events/", response_model=List[Event])
def get_events():
    with Session(engine) as session:
        return session.exec(select(Event)).all()


@router.get("/api/jobs/", response_model=List[Job])
def get_jobs():
    with Session(engine) as session:
        return session.exec(select(Job).order_by(Job.date.desc())).all()


@lru_cache(maxsize=None)
@router.get("/api/third_party/tweet_text/")
def get_tweet_text(tweet_id: int):
    import twitter

    return twitter.get_tweet(tweet_id)


# @router.get("/api/third_party/nostr_note_text/")
# def get_nostr_text(note_id: str, author_pk: str):
#     from get_nostr_post import get_post

#     return get_post(sender_publickey=author_pk, note_id=note_id)


@router.post("/api/ingest/articles/")
@limiter.limit("1/hour")
def ingest_articles(request: Request):
    ingest_articles_func()


@router.post("/api/ingest/podcasts/")
@limiter.limit("1/hour")
def ingest_podcasts(request: Request):
    ingest_podcasts_func()


@router.get("/api/latest_snapshot/", response_model=Optional[str])
def get_latest_snapshot():
    midnight = arrow.utcnow().replace(hour=0, minute=0, second=0)
    return f"{midnight.format('YYYY-MM-DD')}"


@router.get("/api/images/")
def get_images(session: Session = Depends(get_session)):
    print("get_images")
    query = select(Article)
    articles = session.exec(query).all()
    for a in articles:
        if a.image or a.is_draft == 1:
            continue
        if a.link:
            print(f"image missing, let's get it for {a.id}")
            print(f"link is: {a.link}")
            try:
                text = requests.get(a.link, timeout=10).text
                soup = BeautifulSoup(text)
                for tag in soup.find_all("meta"):
                    if tag.get("property", None) == "og:image":
                        image = tag.get("content", None)
                        if image:
                            a.image = image
                            print(image)
                            session.commit()
            except:
                print(print_exc())


@router.get("/api/meta/")
def get_meta():
    session = Session(engine)
    ingest_plain_text.ingest_plain_text(session)


@router.get("/api/meta/index/")
def create_meta_index():
    session = Session(engine)
    ingest_plain_text.create_index(session)


@router.get("/api/meta/search/")
def search_meta_index(term: str):
    session = Session(engine)
    return ingest_plain_text.search_index(session, term)

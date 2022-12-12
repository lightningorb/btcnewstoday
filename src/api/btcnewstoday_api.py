import os
import requests
import simplexml
import json
from typing import Optional, List
import arrow
from functools import lru_cache
from models import *
from fastapi import FastAPI, Request
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from typing import Union
from bn_secrets import *
from ingest_articles import main as ingest_articles_func
from ingest_podcasts import main as ingest_podcasts_func

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "e982e6831af2af1226deafa5e48a9ee3042d7e20b29203ea4b66cc337114b519"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 365


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


origins = ["http://127.0.0.1:5173", "https://btcnews.today", "*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token/", response_model=Token)
@limiter.limit("5/minute")
async def login_for_access_token(
    request: Request, form_data: OAuth2PasswordRequestForm = Depends()
):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]


@app.on_event("startup")
def on_startup():
    # if os.path.exists("database.db"):
    #     os.unlink("database.db")
    create_db_and_tables()
    # add_fixtures()


@app.post("/api/articles/", response_model=Optional[Article])
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


@app.post("/api/delete_article/{article_id}/")
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


@app.post("/api/update_article/{article_id}/", response_model=Optional[Article])
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


@app.post("/api/tweets/", response_model=Tweet)
def add_tweet(tweet: Tweet, current_user: User = Depends(get_current_active_user)):
    with Session(engine) as session:
        print(f"adding tweet: {tweet.id}")
        session.add(tweet)
        session.commit()
        session.refresh(tweet)
        return tweet


@app.get("/api/latest_snapshot/", response_model=Optional[str])
def get_latest_snapshot():
    session = Session(engine)
    midnight = arrow.utcnow().replace(hour=0, minute=0, second=0)
    date = midnight.timestamp()
    next_day = arrow.utcnow().shift(days=1).timestamp()
    snaps = session.exec(
        select(Snapshot).where(Snapshot.date > date, Snapshot.date < next_day)
    ).all()
    if len(snaps):
        return f"{midnight.format('YYYY-MM-DD')}:{len(snaps) // 3 - 1}"


@app.get("/api/articles/", response_model=List[ArticleReadWithTweets])
def get_articles(
    longform: bool = False, is_draft: bool = False, limit: int = 25, snapshot: str = ""
):
    session = Session(engine)
    articles = []
    if snapshot:
        date, sn = snapshot.split(":")
        sn = int(sn)
        date = arrow.get(date).replace(tzinfo="utc").timestamp()
        next_day = arrow.get(date).replace(tzinfo="utc").shift(days=1).timestamp()
        sn_type = ("Article", "Longform")[int(longform)]
        snaps = session.exec(
            select(Snapshot).where(
                Snapshot.date > date, Snapshot.date < next_day, Snapshot.type == sn_type
            )
        ).all()
        if snaps:
            snap = snaps[sn]
            articles = session.exec(
                select(Article)
                .where(Article.id.in_(snap.ids))
                .order_by(Article.date.desc())
            ).all()
    else:
        articles = session.exec(
            select(Article)
            .order_by(Article.date.desc())
            .limit(limit)
            .where(Article.is_longform == longform)
            .where(Article.is_draft == is_draft)
        ).all()
    return articles


@app.get("/api/past_articles/")
def get_past_articles():
    from collections import defaultdict

    dd = defaultdict(list)
    with Session(engine) as session:
        articles = session.exec(
            select(Article)
            .where(Article.is_draft == False)
            .order_by(Article.date.desc())
            .limit(100)
        ).all()
        for a in articles:
            date = int(
                arrow.get(a.date)
                .replace(hour=0, minute=0, second=0, microsecond=0)
                .timestamp()
            )
            dd[date].append(a)

        return [x for x in dict(dd).items()]


@app.post("/api/podcasts/", response_model=Optional[Podcast])
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


@app.post("/api/update_podcast/", response_model=Optional[Podcast])
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


@app.post("/api/jobs/", response_model=Job)
def create_job(Job: Job, current_user: User = Depends(get_current_active_user)):
    with Session(engine) as session:
        session.add(Job)
        session.commit()
        session.refresh(Job)
        return Job


@app.post("/api/events/", response_model=Event)
def create_event(Event: Event, current_user: User = Depends(get_current_active_user)):
    with Session(engine) as session:
        session.add(Event)
        session.commit()
        session.refresh(Event)
        return Event


@app.post("/api/delete_event/{event_id}/")
def delete_event(event_id: int, current_user: User = Depends(get_current_active_user)):
    with Session(engine) as session:
        db_event = session.exec(select(Event).where(Event.id == event_id)).one()
        if not db_event:
            print("Event ID not found")
            return None
        session.delete(db_event)
        session.commit()
        print("deleted")


@app.post("/api/delete_podcast/{podcast_id}/")
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


@app.post("/api/delete_job/{job_id}/")
def delete_podcast(job_id: int, current_user: User = Depends(get_current_active_user)):
    with Session(engine) as session:
        db_job = session.exec(select(Job).where(Job.id == job_id)).one()
        if not db_job:
            print("Job ID not found")
            return None
        session.delete(db_job)
        session.commit()
        print("deleted")


@app.get("/api/podcasts/", response_model=List[Podcast])
def get_podcasts(is_draft: bool = False, limit: int = 25, snapshot: str = ""):
    session = Session(engine)
    if snapshot:
        date, sn = snapshot.split(":")
        sn = int(sn)
        date = arrow.get(date).replace(tzinfo="utc").timestamp()
        next_day = arrow.get(date).replace(tzinfo="utc").shift(days=1).timestamp()
        snaps = session.exec(
            select(Snapshot).where(
                Snapshot.type == "Podcast",
                Snapshot.date > date,
                Snapshot.date < next_day,
            )
        ).all()
        if snaps:
            snap = snaps[sn]
            return session.exec(
                select(Podcast)
                .where(Podcast.id.in_(snap.ids))
                .order_by(Podcast.date.desc())
            ).all()
    else:
        podcasts = session.exec(
            select(Podcast)
            .order_by(Podcast.date.desc())
            .limit(limit)
            .where(Podcast.is_draft == is_draft)
        ).all()
        return podcasts


@app.get("/api/events/", response_model=List[Event])
def get_events():
    with Session(engine) as session:
        return session.exec(select(Event)).all()


@app.get("/api/jobs/", response_model=List[Job])
def get_jobs():
    with Session(engine) as session:
        return session.exec(select(Job).order_by(Job.date.desc())).all()


@lru_cache(maxsize=None)
@app.get("/api/third_party/tweet_text/")
def get_tweet_text(tweet_id: int):
    import tweepy

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    client = tweepy.Client(
        bearer_token=bearer_token,
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )

    tweet = client.get_tweet(id=tweet_id)
    return tweet[0].text


@app.post("/api/events/", response_model=Event)
def create_event(Event: Event, current_user: User = Depends(get_current_active_user)):
    with Session(engine) as session:
        session.add(Event)
        session.commit()
        session.refresh(Event)
        return Event


@app.post("/api/ingest/articles/")
@limiter.limit("1/hour")
def ingest_articles(request: Request):
    ingest_articles_func()


@app.post("/api/ingest/podcasts/")
@limiter.limit("1/hour")
def ingest_podcasts(request: Request):
    ingest_podcasts_func()


@app.post("/api/snapshot/")
@limiter.limit("4/hour")
def create_snapshot(request: Request):
    ts = int(arrow.utcnow().timestamp())
    to_snap = [
        [
            "Article",
            [x.id for x in get_articles(longform=False, is_draft=False, limit=25)],
        ],
        [
            "Longform",
            [x.id for x in get_articles(longform=True, is_draft=False, limit=25)],
        ],
        ["Podcast", [x.id for x in get_podcasts(is_draft=False, limit=25)]],
    ]
    with Session(engine) as session:
        for snap_type, ids in to_snap:
            session.add(Snapshot(type=snap_type, date=ts, ids=ids))
            session.commit()

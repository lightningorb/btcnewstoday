import os
import requests
import simplexml
import json
from typing import Optional, List
import arrow
from functools import lru_cache
from models import *
from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from typing import Union
from secrets import *

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "e982e6831af2af1226deafa5e48a9ee3042d7e20b29203ea4b66cc337114b519"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 365


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI()

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


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
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


# , current_user: User = Depends(get_current_active_user)
@app.post("/api/articles/", response_model=Optional[Article])
def create_article(article: Article):
    with Session(engine) as session:
        articles = session.exec(
            select(Article).where(Article.link == article.link)
        ).all()
        if articles:
            print("Already exists")
            return None
        deleted_article = session.exec(
            select(ArticleDeleted).where(ArticleDeleted.link == article.link)
        ).all()
        if deleted_article:
            print("article previously deleted")
            return None
        session.add(article)
        session.commit()
        print("added")
        session.refresh(article)
        return article


# , current_user: User = Depends(get_current_active_user)
@app.post("/api/delete_article/{article_id}/")
def delete_article(article_id: int):
    with Session(engine) as session:
        db_article = session.exec(select(Article).where(Article.id == article_id)).one()
        if not db_article:
            print("Article ID not found")
            return None
        session.add(ArticleDeleted(link=db_article.link))
        session.delete(db_article)
        session.commit()
        print("deleted")


# , current_user: User = Depends(get_current_active_user)
@app.post("/api/update_article/{article_id}/", response_model=Optional[Article])
def update_article(article: Article):
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


# , current_user: User = Depends(get_current_active_user)
@app.post("/api/tweets/", response_model=Tweet)
def add_tweet(tweet: Tweet):
    with Session(engine) as session:
        print(f"adding tweet: {tweet.id}")
        session.add(tweet)
        session.commit()
        session.refresh(tweet)
        return tweet


@app.get("/api/articles/", response_model=List[ArticleReadWithTweets])
def get_articles(longform: bool = False, is_draft: bool = False):
    session = Session(engine)
    articles = session.exec(
        select(Article)
        .order_by(Article.date.desc())
        .limit(25)
        .where(Article.is_longform == longform)
        .where(Article.is_draft == is_draft)
    ).all()
    return articles
    res = []
    for a in articles:
        tweets = [json.loads(t.json()) for t in a.tweets]
        ids = [t.id for t in a.tweets]
        for t, i in zip(tweets, ids):
            t["id"] = i
        a = json.loads(a.json())
        a["tweets"] = tweets
        res.append(a)
    print(res)
    return res


@app.get("/api/past_articles/")
def get_articles():
    from collections import defaultdict

    dd = defaultdict(list)
    with Session(engine) as session:
        articles = session.exec(
            select(Article).order_by(Article.date.desc()).limit(100)
        ).all()
        for a in articles:
            date = int(
                arrow.get(a.date)
                .replace(hour=0, minute=0, second=0, microsecond=0)
                .timestamp()
            )
            dd[date].append(a)

        return [x for x in dict(dd).items()]


# , current_user: User = Depends(get_current_active_user)
@app.post("/api/podcasts/", response_model=Podcast)
def create_podcast(Podcast: Podcast):
    with Session(engine) as session:
        session.add(Podcast)
        session.commit()
        session.refresh(Podcast)
        return Podcast


# , current_user: User = Depends(get_current_active_user)
@app.post("/api/jobs/", response_model=Job)
def create_job(Job: Job):
    with Session(engine) as session:
        session.add(Job)
        session.commit()
        session.refresh(Job)
        return Job


# , current_user: User = Depends(get_current_active_user)
@app.post("/api/events/", response_model=Event)
def create_event(Event: Event):
    with Session(engine) as session:
        session.add(Event)
        session.commit()
        session.refresh(Event)
        return Event


@app.get("/api/podcasts/", response_model=List[Podcast])
def get_podcasts():
    with Session(engine) as session:
        return session.exec(select(Podcast).order_by(Podcast.date.desc())).all()


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


# , current_user: User = Depends(get_current_active_user)
@app.post("/api/events/", response_model=Event)
def create_event(Event: Event):
    with Session(engine) as session:
        session.add(Event)
        session.commit()
        session.refresh(Event)
        return Event


@app.post("/api/ingest/decrypt")
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

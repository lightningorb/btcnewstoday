from sqlalchemy.orm import contains_eager, joinedload
from sqlmodel import Field, Session, SQLModel, create_engine, select, delete
from sqlalchemy.orm import aliased
import os

from db import *
from models import *

local_engine = create_engine(
    f"postgresql://btcnewstoday:abc_abc_123_abc_abc_123-abc_abc_123@localhost:5432/postgres"
)
session = Session(local_engine)
subq = (
    session.query(Tweet.article_id, func.count(Tweet.id).label("tweet_count"))
    .group_by(Tweet.article_id)
    .subquery()
)
articles_with_approved_tweets = (
    session.query(Article, subq.c.tweet_count)
    .outerjoin(subq, Article.id == subq.c.article_id)
    .all()
)

n = 0
for a in articles_with_approved_tweets:
    print(a[1], a[0].title)
    n += 1

print("n", n)

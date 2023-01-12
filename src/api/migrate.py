from random import choice
from sqlmodel import Field, Session, SQLModel, create_engine, select, delete
import os

from db import *
from models import *

local_engine = create_engine(
    f"postgresql://btcnewstoday:abc_abc_123_abc_abc_123-abc_abc_123@localhost:5432/postgres"
)

local_session = Session(local_engine)
# for t in data.tweets:
#     tweet = local_session.exec(select(Tweet).where(Tweet.id == t)).one()
#     tweet.bounty_paid = True
#     print(tweet)

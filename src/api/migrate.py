from random import choice
from sqlmodel import Field, Session, SQLModel, create_engine, select, delete
import os

from db import *
from models import *

local_engine = create_engine(
    f"postgresql://btcnewstoday:abc_abc_123_abc_abc_123-abc_abc_123@localhost:5432/postgres"
)

local_session = Session(local_engine)
for c in [Tweet, NostrNote]:
    for t in local_session.exec(select(c)).all():
        t.contributor_username = "rs"
        t.bounty_sats = 100
        t.bounty_paid = False
        t.date = t.article.date
        t.approved = True

local_session.commit()

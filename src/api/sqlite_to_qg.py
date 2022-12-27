from sqlmodel import Field, Session, SQLModel, create_engine, select
import os

from db import *
from models import *


sqlite_file_name = os.path.expanduser("~/database.db")
sqlite_url = f"sqlite:///{sqlite_file_name}"

pg_url = f"postgresql://localhost:5433/postgres"
pg_url = f"postgresql://btcnewstoday:abc_abc_123_abc_abc_123-abc_abc_123@localhost:5432/postgres"

connect_args = {"check_same_thread": False}
sq_engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)
pg_engine = create_engine(pg_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(sq_engine)
    SQLModel.metadata.create_all(pg_engine)


create_db_and_tables()

with Session(sq_engine) as sq_session:
    with Session(pg_engine) as pg_session:
        for a in sq_session.exec(select(Article)).all():
            pg_session.add(
                Article(
                    title=a.title,
                    blurb=a.blurb,
                    link=a.link,
                    outlet=a.outlet,
                    author=a.author,
                    category=a.category,
                    is_draft=a.is_draft,
                    is_longform=a.is_longform,
                    date=a.date,
                    image=a.image,
                    id=a.id,
                )
            )
        for t in sq_session.exec(select(Tweet)).all():
            pg_session.add(
                Tweet(
                    id=t.id, username=t.username, text=t.text, article_id=t.article_id
                )
            )
        for t in sq_session.exec(select(NostrNote)).all():
            pg_session.add(
                NostrNote(
                    id=t.id,
                    username=t.username,
                    text=t.text,
                    article_id=t.article_id,
                    note_id=t.note_id,
                    author_pk=t.author_pk,
                )
            )
        for t in sq_session.exec(select(Podcast)).all():
            pg_session.add(
                Podcast(
                    id=t.id,
                    link=t.link,
                    outlet=t.outlet,
                    date=t.date,
                    episode_title=t.episode_title,
                    is_draft=t.is_draft,
                )
            )
        for t in sq_session.exec(select(Meta)).all():
            pg_session.add(
                Meta(**{x: getattr(t, x) for x in ["id", "data", "type", "article_id"]})
            )
        for t in sq_session.exec(select(Job)).all():
            pg_session.add(
                Job(
                    **{
                        x: getattr(t, x)
                        for x in ["id", "link", "company", "role", "date"]
                    }
                )
            )
        for t in sq_session.exec(select(Event)).all():
            pg_session.add(
                Event(
                    **{
                        x: getattr(t, x)
                        for x in ["id", "link", "name", "place", "date"]
                    }
                )
            )
        for t in sq_session.exec(select(ArticleDeleted)).all():
            pg_session.add(ArticleDeleted(**{x: getattr(t, x) for x in ["id", "link"]}))
        for t in sq_session.exec(select(AlembicVersion)).all():
            pg_session.add(
                AlembicVersion(**{x: getattr(t, x) for x in ["version_num"]})
            )
        pg_session.commit()

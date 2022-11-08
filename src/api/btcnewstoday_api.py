import os
from typing import Optional, List
import arrow

from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi.middleware.cors import CORSMiddleware


class Article(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    blurb: str = Field(index=True)
    link: str = Field(index=True)
    outlet: str = Field(index=True)
    is_longform: bool = Field(index=True, default=False)


class Podcast(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    link: str = Field(index=True)
    outlet: str = Field(index=True)
    date: int = Field(index=True)


class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    link: str = Field(index=True)
    name: str = Field(index=True)
    date: int = Field(index=True)
    place: str = Field(index=True)


class Job(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    link: str = Field(index=True)
    company: str = Field(index=True)
    role: str = Field(index=True)
    date: int = Field(index=True)


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI()

origins = ["http://127.0.0.1:5173", "https://btcnews.today"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    if os.path.exists("database.db"):
        os.unlink("database.db")
    create_db_and_tables()
    add_fixtures()


@app.post("/api/articles/", response_model=Article)
def create_Article(Article: Article):
    with Session(engine) as session:
        session.add(Article)
        session.commit()
        session.refresh(Article)
        return Article


@app.get("/api/articles/", response_model=List[Article])
def get_articles(longform: bool = False):
    with Session(engine) as session:
        articles = session.exec(
            select(Article).where(Article.is_longform == longform)
        ).all()
        return articles


@app.get("/api/podcasts/", response_model=List[Podcast])
def get_podcasts():
    with Session(engine) as session:
        return session.exec(select(Podcast)).all()


@app.get("/api/events/", response_model=List[Event])
def get_events():
    with Session(engine) as session:
        return session.exec(select(Event)).all()


@app.get("/api/jobs/", response_model=List[Job])
def get_jobs():
    with Session(engine) as session:
        return session.exec(select(Job)).all()


def add_fixtures():
    with Session(engine) as session:
        session.add(
            Article(
                title="Malicious Python Packages Replace Crypto Addresses in Developer Clipboards",
                blurb="Phylum uncovers a new campaign targeting Python developers. Malware authors surreptitiously replace cryptocurrency addresses in developer clipboards.",
                link="https://blog.phylum.io/pypi-malware-replaces-crypto-addresses-in-developers-clipboard",
                outlet="Phylum",
            )
        )
        session.add(
            Article(
                title="Iran's Currency In Freefall As Protests Sweep The Country",
                blurb="Iran's battered currency, the rial, was in a freefall on Saturday, hitting a historic low of more than 360,000 against the US dollar amid continuing protests.",
                link="https://www.iranintl.com/en/202211053491",
                outlet="Iran International",
            )
        )
        session.add(
            Article(
                title="Digital euro may have transaction limits and store-of-value caps",
                blurb="The European Union’s potential central bank digital currency may have low transaction and storage thresholds for individual users",
                link="https://www.theblock.co/post/183646/digital-euro-transaction-limits-store-value-caps",
                outlet="The Block",
            )
        )
        session.add(
            Article(
                title="FTX Agrees to Sell Itself to Rival Binance Amid Liquidity Scare at Crypto Exchange",
                blurb="The two crypto exchange giants signed a a non-binding letter of intent, Binance CEO Changpeng 'CZ' Zhao confirmed on Twitter.",
                link="https://www.coindesk.com/business/2022/11/08/ftx-reaches-deal-with-binance-amid-liquidity-scare-sam-bankman-fried-says/",
                outlet="Coindesk",
            )
        )
        session.add(
            Article(
                title="A Look at the Lightning Network",
                blurb="This article examines the relationship between a monetary asset being a store of value vs being a medium of exchange.",
                link="https://www.lynalden.com/lightning-network/",
                outlet="Lyn Alden",
                is_longform=True,
            )
        )
        session.add(
            Podcast(
                link="https://podcasts.google.com/feed/aHR0cHM6Ly9yc3MuYXJ0MTkuY29tL2xhdGUtY29uZmlybWF0aW9u/episode/Z2lkOi8vYXJ0MTktZXBpc29kZS1sb2NhdG9yL1YwLzJuOW4zdlQxVXEzY09BNTJVSlk5TFQ5ckpJZ2I5elRFRnZhNTJpeUZweEU",
                outlet="The Breakdown",
                date=arrow.get("2022-11-07T00:00:00Z").timestamp(),
            )
        )
        session.add(
            Podcast(
                link="https://www.whatbitcoindid.com/podcast/the-fundamentals-of-bitcoins-value",
                outlet="What Bitcoin Did",
                date=arrow.get("2022-11-07T00:00:00Z").timestamp(),
            )
        )
        session.add(
            Event(
                link="https://events.bizzabo.com/crypto_state_world_tour",
                name="Crypto Slate by Coindesk",
                place="Southeast Asia",
                date=arrow.get("2022-02-24T00:00:00Z").timestamp(),
            )
        )
        session.add(
            Job(
                link="https://example.com",
                company="Exodus",
                role="Senior PR Manager",
                date=arrow.get("2022-02-24T00:00:00Z").timestamp(),
            ),
        )
        session.add(
            Job(
                link="https://example.com",
                company="Google",
                role="Lightning Engineer",
                date=arrow.get("2022-02-24T00:00:00Z").timestamp(),
            ),
        )
        session.add(
            Job(
                link="https://example.com",
                company="AWS",
                role="BLockchain Infrastructure",
                date=arrow.get("2022-02-24T00:00:00Z").timestamp(),
            ),
        )
        session.commit()

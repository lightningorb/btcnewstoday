import os
from typing import Optional

from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi.middleware.cors import CORSMiddleware


class Article(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    blurb: str = Field(index=True)
    link: str = Field(index=True)
    outlet: str = Field(index=True)


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


@app.post("/articles/", response_model=Article)
def create_Article(Article: Article):
    with Session(engine) as session:
        session.add(Article)
        session.commit()
        session.refresh(Article)
        return Article


@app.get("/articles/")
def read_articles():
    with Session(engine) as session:
        articles = session.exec(select(Article)).all()
        return articles


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
        session.commit()

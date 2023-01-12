from sqlalchemy.dialects import postgresql
from typing import Optional, List, Union, Set
from pydantic import BaseModel
import arrow

from sqlalchemy import TIMESTAMP, func, cast, BigInteger, Integer
from sqlalchemy.orm import column_property, declared_attr
from sqlmodel import DateTime, Field, Column

from sqlmodel import (
    Field,
    Session,
    SQLModel,
    create_engine,
    select,
    Relationship,
    JSON,
    Column,
)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class UserBase(SQLModel):
    username: str = Field(primary_key=True)
    role: str = Field()
    twitter_uid: str = Field()
    twitter_username: str = Field()
    ln_address: str = Field(nullable=True)


class User(UserBase, table=True):
    hashed_password: str = Field()


class UserRead(UserBase):
    num_tweets: int
    num_notes: int
    num_tweets_approved: int
    num_notes_approved: int
    redeemable_sats: int
    redeemed_sats: int
    ln_address: str


class ArticleBase(SQLModel):
    title: str = Field(index=True)
    blurb: str = Field(index=True)
    link: str = Field(index=True)
    outlet: str = Field(index=True)
    author: Optional[str] = Field(index=True)
    category: Optional[str] = Field(index=True)
    is_draft: Optional[bool] = Field(index=True, default=False)
    is_longform: bool = Field(index=True, default=False)
    date: int = Field(index=True, default=arrow.utcnow().timestamp(), nullable=True)
    image: Optional[str] = Field(index=False, nullable=True, default="")


class Article(ArticleBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tweets: List["Tweet"] = Relationship(back_populates="article")
    nostr_notes: List["NostrNote"] = Relationship(back_populates="article")
    meta: List["Meta"] = Relationship(back_populates="article")


class MetaBase(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    data: str = Field(index=False)
    type: str = Field(index=True)
    article_id: int = Field(index=True, foreign_key="article.id")


class Meta(MetaBase, table=True):
    article: Optional[Article] = Relationship(back_populates="meta")


class ContributionBase(SQLModel):
    contributor_username: str = Field(
        index=True, foreign_key="user.username", nullable=True
    )
    approved: bool = Field(index=True, nullable=True)
    bounty_sats: int = Field(index=False, nullable=True)
    bounty_paid: bool = Field(index=False, nullable=True)


class TweetBase(ContributionBase):
    id: Optional[int] = Field(default=None, primary_key=True)
    tweet_id: Optional[int] = Field(
        sa_column=Column(BigInteger(), primary_key=False, autoincrement=False)
    )
    username: str = Field(index=True)
    text: str = Field(index=True)
    article_id: int = Field(index=True, foreign_key="article.id")
    date: int = Field(index=True, default=arrow.utcnow().timestamp(), nullable=True)


class TweetAdd(BaseModel):
    tweet_id: int
    username: str
    text: str
    article_id: int


class NostrNoteBase(ContributionBase):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    note_id: str = Field(index=True)
    text: str = Field(index=True)
    article_id: int = Field(index=True, foreign_key="article.id")
    date: int = Field(index=True, default=arrow.utcnow().timestamp(), nullable=True)


class Tweet(TweetBase, table=True):
    article: Optional[Article] = Relationship(back_populates="tweets")


class NostrNote(NostrNoteBase, table=True):
    article: Optional[Article] = Relationship(back_populates="nostr_notes")


class NostrNoteAdd(BaseModel):
    article_id: int
    text: str
    note_id: str
    username: str


class TweetRead(TweetBase):
    id: str
    tweet_id: str


class NostrNoteRead(NostrNoteBase):
    id: str


class ArticleRead(ArticleBase):
    id: int


class ArticleReadWithTweets(ArticleRead):
    tweets: List[TweetRead] = []
    nostr_notes: List[NostrNoteRead] = []


class PodcastUpdate(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    outlet: str = Field(index=True)
    episode_title: str = Field(index=True, default="", nullable=True)
    is_draft: Optional[bool] = Field(index=True, default=False)


class Podcast(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    link: str = Field(index=True)
    outlet: str = Field(index=True)
    date: int = Field(index=True)
    episode_title: str = Field(index=True, default="", nullable=True)
    is_draft: Optional[bool] = Field(index=True, default=False)


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


class BountyRates(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    notes: int = Field(index=False)
    tweets: int = Field(index=False)
    date: int = Field(index=True, default=arrow.utcnow().timestamp(), nullable=False)


class Withdrawal(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, foreign_key="user.username", nullable=True)
    ln_address: str = Field(nullable=False)
    date: int = Field(index=True, nullable=False)
    notes: Optional[Set[int]] = Field(
        default=None, sa_column=Column(postgresql.ARRAY(BigInteger()))
    )
    tweets: Optional[Set[int]] = Field(
        default=None, sa_column=Column(postgresql.ARRAY(BigInteger()))
    )
    amount_msat: str = Field(index=False)
    amount_sent_msat: str = Field(index=False)
    api_version: str = Field(index=False)
    created_at: int = Field(index=False)
    destination: str = Field(index=False)
    msatoshi: int = Field(index=False)
    msatoshi_sent: int = Field(index=False)
    parts: int = Field(index=False)
    payment_hash: str = Field(index=False)
    payment_preimage: str = Field(index=False)
    status: str = Field(index=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class BountyRatesRead(BaseModel):
    notes: int
    tweets: int


class AlembicVersion(SQLModel, table=True):
    version_num: str = Field(default=None, primary_key=True)

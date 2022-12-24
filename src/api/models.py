from typing import Optional, List, Union
from pydantic import BaseModel
import arrow

from sqlalchemy import TIMESTAMP, func, cast
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


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str


class ArticleDeleted(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    link: str = Field(index=True)


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


class TweetBase(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    text: str = Field(index=True)
    article_id: int = Field(index=True, foreign_key="article.id")


class NostrNoteBase(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    author_pk: str = Field(index=True)
    note_id: str = Field(index=True)
    text: str = Field(index=True)
    article_id: int = Field(index=True, foreign_key="article.id")


class Tweet(TweetBase, table=True):
    article: Optional[Article] = Relationship(back_populates="tweets")


class NostrNote(NostrNoteBase, table=True):
    article: Optional[Article] = Relationship(back_populates="nostr_notes")


class TweetRead(TweetBase):
    id: str


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

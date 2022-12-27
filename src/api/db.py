from sqlmodel import Field, Session, SQLModel, create_engine, select
import os

use_postgres = True

if not use_postgres:
    sqlite_file_name = os.path.expanduser("~/database.db")
    sqlite_url = f"sqlite:///{sqlite_file_name}"
    connect_args = {"check_same_thread": False}
    engine = create_engine(sqlite_url, connect_args=connect_args)
else:
    pg_url = f"postgresql://btcnewstoday:abc_abc_123_abc_abc_123-abc_abc_123@localhost:5432/postgres"
    engine = create_engine(pg_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

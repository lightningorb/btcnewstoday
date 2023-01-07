from sqlmodel import Field, Session, SQLModel, create_engine, select
import os

pg_url = f"postgresql://btcnewstoday:abc_abc_123_abc_abc_123-abc_abc_123@localhost:5432/postgres"
pg_url = os.environ.get("bndev_pg_url", pg_url)
engine = create_engine(pg_url, pool_size=200, max_overflow=50, pool_pre_ping=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

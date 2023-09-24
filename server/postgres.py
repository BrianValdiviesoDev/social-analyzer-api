import os
from dotenv import load_dotenv

from sqlmodel import create_engine, SQLModel, Session

load_dotenv()

db_host = os.environ.get("DB_HOST")
db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASSWORD")
db_database = os.environ.get("DB_DATABASE")
db_port = os.environ.get("DB_PORT")

postgres_uri = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}"


engine = create_engine(postgres_uri, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


def init_db():
    SQLModel.metadata.create_all(engine)

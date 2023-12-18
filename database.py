from sqlalchemy import create_engine
# from alembic import context
from sqlalchemy.orm import sessionmaker
from users.alchemyModels import UsersBase
from matching.alchemyModels import MatchesBase
from messages.alchemyModels import MessagesBase
from peers.alchemyModels import PeersBase, PeerConnectionsBase
from tags.alchemyModels import TagsBase
from tags.alchemyModels import UsersTagsBase

import os
from dotenv import load_dotenv

load_dotenv()

# Create SSL context
# ssl_args = {'sslmode': 'require'}
# ssl_ca = '/ca-certificate.crt'

# db_user = os.getenv('POSTGRES_USER')
# password = os.getenv('POSTGRES_PASSWORD')
# db_name = os.getenv('POSTGRES_DB')
# host = os.getenv('DB_HOST', 'localhost')
# port_str = os.getenv('DB_PORT')
# port = int(port_str)


# database_url = f'postgresql://{db_user}:{password}@{host}:{port}/{db_name}?sslmode=require'

database_url = os.getenv('DATABASE_URL')

engine = create_engine(database_url)
# engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def connect_to_db():
    return SessionLocal()


def close_connection(db):
    db.close()


def initialize_database():
    UsersBase.metadata.create_all(engine)
    TagsBase.metadata.create_all(engine)
    UsersTagsBase.metadata.create_all(engine)
    MatchesBase.metadata.create_all(engine)
    PeersBase.metadata.create_all(engine)
    PeerConnectionsBase.metadata.create_all(engine)
    MessagesBase.metadata.create_all(engine)


def close_engine():
    engine.dispose()

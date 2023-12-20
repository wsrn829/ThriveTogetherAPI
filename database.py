from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
import os
from dotenv import load_dotenv
#importing models
from peers.alchemyModels import Peers, PeerConnections
from users.alchemyModels import Users
from tags.alchemyModels import Tags, UserTags
from messages.alchemyModels import Messages
from matching.alchemyModels import Matches
from accounts.alchemyModels import Accounts


load_dotenv()


database_url = os.getenv('DATABASE_URL')

engine = create_engine(database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def connect_to_db():
    return SessionLocal()


def close_connection(db):
    db.close()


def close_engine():
    engine.dispose()


def initialize_database():
    Base.metadata.create_all(bind=engine)

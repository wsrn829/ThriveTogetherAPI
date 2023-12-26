from sqlalchemy import Column, Integer, String
from base import Base

# Assuming Base is your declarative base instance in SQLAlchemy


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    hashed_password = Column(String(1000), nullable=False)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(50), nullable=False)
    pronouns = Column(String(10), nullable=False)
    profile_link = Column(String(75))
    profile_image = Column(String(1000))
    banner_image = Column(String(1000))
    email = Column(String(150), nullable=False)
    about_me = Column(String(5000))
    my_story = Column(String(5000))

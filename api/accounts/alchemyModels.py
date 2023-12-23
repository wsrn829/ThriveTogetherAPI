from sqlalchemy import Column, Integer, String
from base import Base


class Accounts(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    pronouns = Column(String)
    email = Column(String)

    def __repr__(self):
        return f"<Account(username='{self.username}', email='{self.email}')>"

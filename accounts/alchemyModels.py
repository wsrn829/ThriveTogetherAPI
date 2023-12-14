from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


# SQLAlchemy models for database mapping
AccountsBase = declarative_base()


class Accounts(AccountsBase):
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

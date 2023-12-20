from sqlalchemy import Column, Integer, String, ForeignKey
from base import Base
from sqlalchemy.orm import relationship


# Define the SQLAlchemy model corresponding to Tag
class Tags(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    tag = Column(String)


class UserTags(Base):
    __tablename__ = 'user_tags'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    tag_id = Column(Integer, ForeignKey('tags.id'), nullable=False)

    tag = relationship("Tags", backref="users_tags")
    user = relationship("Users", backref="users_tags")

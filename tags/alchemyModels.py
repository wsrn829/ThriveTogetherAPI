from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from users.alchemyModels import Users
from sqlalchemy.orm import relationship
from sqlalchemy import inspect
from users.alchemyModels import UsersBase
from sqlalchemy import inspect

TagsBase = declarative_base()
UsersTagsBase = declarative_base()

# print("Before code snippet")
# inspector = inspect(UsersBase.metadata)
# table_names = sorted(UsersBase.metadata.tables.keys())
# print(table_names)
# print("After code snippet")


# Define the SQLAlchemy model corresponding to Tag
class Tags(TagsBase):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    tag = Column(String)


class UsersTags(UsersTagsBase):
    __tablename__ = 'users_tags'

    id = Column(Integer, primary_key=True)
    # user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    # tag_id = Column(Integer, ForeignKey('tags.id'), nullable=False)

    # tag = relationship("Tags", backref="users_tags")
    # user = relationship("Users", backref="users_tags")

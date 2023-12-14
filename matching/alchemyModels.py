from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


MatchesBase = declarative_base()


# # Define the SQLAlchemy model corresponding to HttpError
# class HttpError(Base):
#     __tablename__ = 'http_errors'

#     id = Column(Integer, primary_key=True)
#     detail = Column(String)


# # Define the SQLAlchemy model corresponding to TagsOut
# class TagsOut(MatchBase):
#     __tablename__ = 'tags_out'

#     id = Column(Integer, primary_key=True)
#     tags = Column(JSON)  # Assuming storing list of strings as JSON


# Define the SQLAlchemy model corresponding to MatchOut
class Matches(MatchesBase):
    __tablename__ = 'matches'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    about_me = Column(String, nullable=True)
    profile_link = Column(String, nullable=True)
    profile_image = Column(String, nullable=True)
    gender = Column(String)
    pronouns = Column(String)

    # Relationship with TagsOut
    tags = relationship("TagsOut", secondary='match_tags')


# # Define the SQLAlchemy model corresponding to MatchesOut
# class MatchesOut(MatchBase):
#     __tablename__ = 'matches_out'

#     id = Column(Integer, primary_key=True)
#     matches = Column(JSON)

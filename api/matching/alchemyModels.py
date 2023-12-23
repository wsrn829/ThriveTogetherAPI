from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from base import Base


# Define the SQLAlchemy model corresponding to MatchOut
class Matches(Base):
    __tablename__ = 'matches'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    about_me = Column(String, nullable=True)
    profile_link = Column(String, nullable=True)
    profile_image = Column(String, nullable=True)
    gender = Column(String)
    pronouns = Column(String)

    # Relationship with Tags
    tags = relationship("Tags", secondary='match_tags')


# # Define the SQLAlchemy model corresponding to MatchesOut
# class MatchesOut(MatchBase):
#     __tablename__ = 'matches_out'

#     id = Column(Integer, primary_key=True)
#     matches = Column(JSON)

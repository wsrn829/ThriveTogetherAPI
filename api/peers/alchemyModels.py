from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from base import Base


# Define the SQLAlchemy model corresponding to PeerConnection
class PeerConnections(Base):
    __tablename__ = 'peer_connections'

    id = Column(Integer, primary_key=True)
    sender = Column(Integer)
    recipient = Column(Integer)
    status = Column(String)
    has_messaged = Column(String)
    sender_name = Column(String)
    recipient_name = Column(String)


# Define the SQLAlchemy model corresponding to Peer
class Peers(Base):
    __tablename__ = 'peers'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    peer_id = Column(Integer, ForeignKey('users.id'))
    # Assuming both peer and user are from the same table 'users'
    peer_name = Column(String)
    profile_link = Column(String)
    tags_id = Column(Integer)
    profile_image = Column(String)
    status = Column(Integer)

    # Relationships with User model for user and peer
    user = relationship("User", foreign_keys=[user_id])
    peer = relationship("User", foreign_keys=[peer_id])


# # Define the SQLAlchemy model corresponding to PeerConnections
# class PeerConnections(PeerBase):
#     __tablename__ = 'peer_connections_list'

#     id = Column(Integer, primary_key=True)
#     # Assuming peer_connections_list is a separate table
#     # for storing a list of peer connections
#     peer_connections = relationship(
#         "PeerConnection",
#         cascade="all, delete-orphan")

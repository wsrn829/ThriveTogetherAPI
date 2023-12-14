from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, \
    DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

MessagesBase = declarative_base()


# Define the SQLAlchemy model corresponding to MessageOut
class Messages(MessagesBase):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    # recipient = Column(Integer, ForeignKey('users.id'))
    # sender = Column(Integer, ForeignKey('users.id'))
    content = Column(String)
    date = Column(DateTime, default=datetime.utcnow)
    is_read = Column(Boolean, default=False)
    username = Column(String)
    profile_image = Column(String, nullable=True)
    profile_link = Column(String, nullable=True)
    user_id = Column(Integer)

    # Relationships with User model for recipient and sender
    # recipient_user = relationship("Users", foreign_keys=[recipient])
    # sender_user = relationship("Users", foreign_keys=[sender])

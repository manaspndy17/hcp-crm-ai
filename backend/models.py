from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from database import Base

class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    hcp_name = Column(String(100))
    interaction_type = Column(String(50))
    attendees = Column(String(255))
    topics_discussed = Column(Text)
    sentiment = Column(String(20))
    outcomes = Column(Text)
    follow_up_actions = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
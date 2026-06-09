from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ContactMessage(Base):
    __tablename__ = "contact_messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    subject = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

from sqlalchemy import Column, Integer, String, DateTime, Text

from core.database import Base


class RawNews(Base):
    __tablename__ = "raw_news"
    id = Column(Integer, primary_key=True)
    page = Column(String, nullable=True)
    url = Column(String, nullable=True)
    issued = Column(DateTime(timezone=True), nullable=True)
    modified = Column(DateTime(timezone=True), nullable=True)
    title = Column(String, nullable=True)
    body = Column(Text, nullable=True)
    caption = Column(Text, nullable=True)
    title_length = Column(Integer, nullable=True)
    body_length = Column(Integer, nullable=True)
    issued_year = Column(Integer, nullable=True)
    issued_month = Column(Integer, nullable=True)


class RawUsers(Base):
    __tablename__ = "raw_users"
    id = Column(Integer, primary_key=True)
    userId = Column(String, nullable=True)
    userType = Column(String, nullable=True)
    historySize = Column(Integer, nullable=True)
    history = Column(Text, nullable=True)
    timestampHistory = Column(Text, nullable=True)
    numberOfClicksHistory = Column(Text, nullable=True)
    timeOnPageHistory = Column(Text, nullable=True)
    scrollPercentageHistory = Column(Text, nullable=True)
    pageVisitsCountHistory = Column(Text, nullable=True)
    timestampHistory_new = Column(Text, nullable=True)

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import declarative_base
Base = declarative_base()
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    discord_id = Column(String, unique=True)
    calls = relationship("Call", back_populates="user")
    watchlist = relationship("Watchlist", back_populates="user")
    duplicate_messages = Column(Boolean, default=False)

class Call(Base):
    __tablename__ = 'calls'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    token_id = Column(Integer, ForeignKey('tokens.id'))
    entry_price = Column(Float)
    close_price = Column(Float)
    entry_fdv = Column(Float)
    close_fdv = Column(Float)
    open_time = Column(DateTime)
    close_time = Column(DateTime)
    user = relationship("User", back_populates="calls")
    token = relationship("Token")

class Token(Base):
    __tablename__ = 'tokens'
    id = Column(Integer, primary_key=True)
    address = Column(String, unique=True)
    name = Column(String)
    symbol = Column(String)
    chain = Column(String)
    price = Column(Float)  # Add this line
    fdv = Column(Float)  # Add this line
    volume24h = Column(Float)  # Add this line
    priceChange24h = Column(Float)  # Add this line

class Watchlist(Base):
    __tablename__ = 'watchlist'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    token_id = Column(Integer, ForeignKey('tokens.id'))
    user = relationship("User", back_populates="watchlist")
    token = relationship("Token")
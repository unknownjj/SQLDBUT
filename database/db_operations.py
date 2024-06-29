print("Importing db_operations.py")

def init_db():
    print("init_db function called")

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, joinedload
print("Importing db_operations.py")
try:
    from database.models import Base, User, Call, Token, Watchlist
    print("Successfully imported from models")
except ImportError as e:
    print(f"Error importing from models: {e}")
import logging
from config import DATABASE_URL
print(f"Database URL: {DATABASE_URL}")
from datetime import datetime
from bot.utils.api import get_token_info

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)

def get_or_create_user(discord_id):
    session = Session()
    user = session.query(User).filter_by(discord_id=str(discord_id)).first()
    if not user:
        user = User(discord_id=str(discord_id))
        session.add(user)
        session.commit()
    session.close()
    return user

def open_call(discord_id, token_info):
    session = Session()
    try:
        user = get_or_create_user(discord_id)
        token = session.query(Token).filter_by(address=token_info['address']).first()
        if not token:
            token = Token(**token_info)
            session.add(token)
        
        existing_call = session.query(Call).filter_by(user_id=user.id, token_id=token.id, close_time=None).first()
        if existing_call:
            session.close()
            return None

        call = Call(user=user, token=token, entry_price=token_info['price'], entry_fdv=token_info['fdv'], open_time=datetime.utcnow())
        session.add(call)
        session.commit()
        logging.info(f"Call opened: User {discord_id}, Token {token_info['address']}")

        # Eagerly load the token and user relationships
        call = session.query(Call).options(joinedload(Call.token), joinedload(Call.user)).filter_by(id=call.id).one()
        return call
    except Exception as e:
        logging.error(f"Error opening call: {str(e)}")
        session.rollback()
        return None
    finally:
        session.close()

def close_call(discord_id, address):
    session = Session()
    try:
        user = get_or_create_user(discord_id)
        token = session.query(Token).filter_by(address=address).first()
        if not token:
            return None
        
        call = session.query(Call).options(joinedload(Call.token), joinedload(Call.user)).filter_by(user_id=user.id, token_id=token.id, close_time=None).first()
        if not call:
            return None

        token_info = get_token_info(address)
        if not token_info:
            return None

        call.close_price = token_info['price']
        call.close_fdv = token_info['fdv']
        call.close_time = datetime.utcnow()
        session.commit()
        logging.info(f"Call closed: User {discord_id}, Token {address}")

        # Eagerly load the token and user relationships
        call = session.query(Call).options(joinedload(Call.token), joinedload(Call.user)).filter_by(id=call.id).one()
        return call
    except Exception as e:
        logging.error(f"Error closing call: {str(e)}")
        session.rollback()
        return None
    finally:
        session.close()

def get_user_calls(discord_id, limit=10):
    session = Session()
    try:
        user = get_or_create_user(discord_id)
        calls = session.query(Call).options(joinedload(Call.token), joinedload(Call.user)).filter_by(user_id=user.id).order_by(Call.open_time.desc()).limit(limit).all()
        return calls
    finally:
        session.close()

def get_leaderboard():
    session = Session()
    try:
        subquery = session.query(
            Call.user_id,
            func.avg(Call.close_fdv / Call.entry_fdv).label('avg_performance'),
            func.count(Call.id).label('total_calls')
        ).filter(Call.close_time != None).group_by(Call.user_id).subquery()

        leaderboard = session.query(
            User.discord_id,
            subquery.c.avg_performance,
            subquery.c.total_calls
        ).join(subquery, User.id == subquery.c.user_id).order_by(subquery.c.avg_performance.desc()).all()

        return leaderboard
    finally:
        session.close()

def toggle_duplicate_messages(discord_id):
    session = Session()
    try:
        user = get_or_create_user(discord_id)
        user.duplicate_messages = not user.duplicate_messages
        session.commit()
        return user.duplicate_messages
    finally:
        session.close()

def add_to_watchlist(discord_id, token_info):
    session = Session()
    try:
        user = get_or_create_user(discord_id)
        token = session.query(Token).filter_by(address=token_info['address']).first()
        if not token:
            token = Token(**token_info)
            session.add(token)

        existing_watch = session.query(Watchlist).filter_by(user_id=user.id, token_id=token.id).first()
        if existing_watch:
            return False

        watchlist_count = session.query(Watchlist).filter_by(user_id=user.id).count()
        if watchlist_count >= 10:
            return False

        watchlist_item = Watchlist(user=user, token=token)
        session.add(watchlist_item)
        session.commit()
        return True
    except Exception as e:
        logging.error(f"Error adding to watchlist: {str(e)}")
        session.rollback()
        return False
    finally:
        session.close()

def remove_from_watchlist(discord_id, symbol):
    session = Session()
    try:
        user = get_or_create_user(discord_id)
        watchlist_item = session.query(Watchlist).join(Token).options(joinedload(Watchlist.token), joinedload(Watchlist.user)).filter(Watchlist.user_id == user.id, Token.symbol == symbol).first()
        if watchlist_item:
            session.delete(watchlist_item)
            session.commit()
            return True
        return False
    finally:
        session.close()

def get_watchlist(discord_id):
    session = Session()
    try:
        user = get_or_create_user(discord_id)
        watchlist = session.query(Watchlist).options(joinedload(Watchlist.token), joinedload(Watchlist.user)).filter_by(user_id=user.id).all()
        return watchlist
    finally:
        session.close()

def export_calls():
    session = Session()
    try:
        calls = session.query(Call).options(joinedload(Call.token), joinedload(Call.user)).all()
        # Implement CSV export logic here
        return calls
    finally:
            session.close()

def import_calls(data):
    session = Session()
    try:
        # Implement CSV import logic here
        session.commit()
    except Exception as e:
        logging.error(f"Error importing calls: {str(e)}")
        session.rollback()
    finally:
        session.close()

def export_watchlist():
    session = Session()
    try:
        watchlist = session.query(Watchlist).options(joinedload(Watchlist.token), joinedload(Watchlist.user)).all()
        # Implement CSV export logic here
        return watchlist
    finally:
        session.close()

def import_watchlist(data):
    session = Session()
    try:
        # Implement CSV import logic here
        session.commit()
    except Exception as e:
        logging.error(f"Error importing watchlist: {str(e)}")
        session.rollback()
    finally:
        session.close()

__all__ = ['init_db']
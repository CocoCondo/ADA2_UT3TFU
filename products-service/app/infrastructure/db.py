from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from app.config import settings

engine = create_engine(settings.DATABASE_URL, future=True)

def get_connection():
    return engine.connect()
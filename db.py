import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
import subprocess

from dotenv import load_dotenv

# Explicitly load .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

def init_db():
    try:
        Base.metadata.create_all(engine)
    except Exception as e:
        print(f"Error initializing the database: {e}")
        raise

def get_db_session():
    Session = sessionmaker(bind=engine)
    return Session()

init_db()

import os
import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


if DATABASE_URL and "@" in DATABASE_URL:
    try:
        prefix, rest = DATABASE_URL.split("://", 1)
        auth, host_db = rest.split("@", 1)
        user, password = auth.split(":", 1)
        safe_password = urllib.parse.quote_plus(urllib.parse.unquote(password))
        DATABASE_URL = f"{prefix}://{user}:{safe_password}@{host_db}"
    except Exception:
        pass

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
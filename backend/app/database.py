import os
import shutil
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Environment DATABASE_URL (PostgreSQL, Neon, Supabase, etc.)
env_db_url = os.getenv("DATABASE_URL")

if env_db_url:
    if env_db_url.startswith("postgres://"):
        env_db_url = env_db_url.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URL = env_db_url
else:
    # 2. SQLite Database Path
    local_db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "ai_resume_screening.db"))
    
    # On Vercel Serverless environment, workspace filesystem is read-only.
    # We copy the pre-seeded SQLite DB to /tmp if running on Vercel.
    if os.getenv("VERCEL"):
        tmp_db_path = "/tmp/ai_resume_screening.db"
        if not os.path.exists(tmp_db_path):
            if os.path.exists(local_db_path):
                os.makedirs(os.path.dirname(tmp_db_path), exist_ok=True)
                shutil.copy2(local_db_path, tmp_db_path)
        SQLALCHEMY_DATABASE_URL = f"sqlite:///{tmp_db_path}"
    else:
        SQLALCHEMY_DATABASE_URL = f"sqlite:///{local_db_path}"

connect_args = {"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args=connect_args
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

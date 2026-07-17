from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os


# --------------------------------
# Database URL
# --------------------------------

# Local testing database
SQLITE_DATABASE_URL = "sqlite:///./quizverse.db"


# Railway/Supabase will provide this later
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    SQLITE_DATABASE_URL
)


# Fix for PostgreSQL URL on Railway
# Railway sometimes gives postgres://
if DATABASE_URL.startswith("postgres://"):

    DATABASE_URL = DATABASE_URL.replace(
        "postgres://",
        "postgresql://",
        1
    )


# --------------------------------
# Database Engine
# --------------------------------

connect_args = {}

if DATABASE_URL.startswith("sqlite"):

    connect_args = {
        "check_same_thread": False
    }


engine = create_engine(

    DATABASE_URL,

    connect_args=connect_args

)


# --------------------------------
# Session
# --------------------------------

SessionLocal = sessionmaker(

    autocommit=False,

    autoflush=False,

    bind=engine

)


# --------------------------------
# Base Model
# --------------------------------

Base = declarative_base()



# --------------------------------
# Create Database Tables
# --------------------------------

def create_tables():

    from models import User, Quiz, Result

    Base.metadata.create_all(
        bind=engine
    )


# --------------------------------
# Database Dependency
# --------------------------------

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()



if __name__ == "__main__":

    create_tables()

    print(
        "✅ Database tables created successfully"
    )
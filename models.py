from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base


# ----------------------------
# User Table
# ----------------------------

class User(Base):

    __tablename__ = "users"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    username = Column(
        String,
        unique=True,
        nullable=False
    )


    password_hash = Column(
        String,
        nullable=False
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    quizzes = relationship(
        "Quiz",
        back_populates="user"
    )



# ----------------------------
# Quiz Table
# ----------------------------

class Quiz(Base):

    __tablename__ = "quizzes"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )


    subject = Column(
        String,
        nullable=False
    )


    chapter = Column(
        String,
        nullable=False
    )


    difficulty = Column(
        String,
        nullable=False
    )


    questions_json = Column(
        Text,
        nullable=False
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    user = relationship(
        "User",
        back_populates="quizzes"
    )


    results = relationship(
        "Result",
        back_populates="quiz"
    )



# ----------------------------
# Result Table
# ----------------------------

class Result(Base):

    __tablename__ = "results"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )


    quiz_id = Column(
        Integer,
        ForeignKey("quizzes.id")
    )


    score = Column(
        Integer,
        nullable=False
    )


    total = Column(
        Integer,
        nullable=False
    )


    time_taken = Column(
        Integer
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    quiz = relationship(
        "Quiz",
        back_populates="results"
    )
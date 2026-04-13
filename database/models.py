from sqlalchemy import create_engine, Column, Integer, String, Text, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime
from dotenv import load_dotenv
import os

load_dotenv()

# PostgreSQL Connection String
# Format: postgresql://user:password@host:port/dbname
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/interview_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    id = Column(Integer, primary_key=True, index=True)
    roles = Column(String)  # Comma-separated roles
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    overall_score = Column(Float, nullable=True)
    overall_feedback = Column(Text, nullable=True)
    
    questions = relationship("Question", back_populates="session")

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("interview_sessions.id"))
    text = Column(Text)
    
    session = relationship("InterviewSession", back_populates="questions")
    evaluation = relationship("Evaluation", back_populates="question", uselist=False)

class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    user_answer = Column(Text)
    score = Column(Integer)
    strengths = Column(Text)
    weaknesses = Column(Text)
    missing_points = Column(Text)
    ideal_answer = Column(Text)
    improvement = Column(Text)

    question = relationship("Question", back_populates="evaluation")

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

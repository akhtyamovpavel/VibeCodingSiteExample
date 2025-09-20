from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Course(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    duration_hours = Column(Integer, default=0)
    difficulty_level = Column(String(50), default="beginner")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Связи
    topics = relationship("Topic", back_populates="course", cascade="all, delete-orphan")

class Topic(Base):
    __tablename__ = "topics"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    order_index = Column(Integer, default=0)
    duration_minutes = Column(Integer, default=0)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Связи
    course = relationship("Course", back_populates="topics")
    assignments = relationship("Assignment", back_populates="topic", cascade="all, delete-orphan")

class Assignment(Base):
    __tablename__ = "assignments"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    instructions = Column(Text, nullable=False)
    difficulty_level = Column(String(50), default="easy")
    estimated_hours = Column(Integer, default=1)
    is_required = Column(Boolean, default=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Связи
    topic = relationship("Topic", back_populates="assignments")
    hints = relationship("Hint", back_populates="assignment", cascade="all, delete-orphan")

class Hint(Base):
    __tablename__ = "hints"
    
    id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id"), nullable=False)
    order_index = Column(Integer, default=0)
    text = Column(Text, nullable=False)
    penalty = Column(Integer, default=10)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    assignment = relationship("Assignment", back_populates="hints")

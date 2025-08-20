import uuid
from datetime import datetime

from sqlalchemy import Column, String, Text, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False
    )
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False, default='')
    status = Column(String(20), nullable=False, default='создано')
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index('idx_tasks_status', 'status'),
        Index('idx_tasks_created_at', 'created_at'),
        Index('idx_tasks_updated_at', 'updated_at'),
        Index('idx_tasks_title', 'title'),
    )

    def __repr__(self) -> str:
        return f"<Task(id={self.id}, title='{self.title}', status='{self.status}')>"

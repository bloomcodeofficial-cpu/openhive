from .db import Base
from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import Boolean

# SQLAlchemy ORM models

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(String, unique=True, index=True, nullable=False)
    goal = Column(Text)
    agent_type = Column(String, index=True)
    workspace_id = Column(String, nullable=True)
    permissions = Column(JSONB)
    timeout_seconds = Column(Integer)
    status = Column(String, index=True)
    result = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self):
        return {
            'task_id': self.task_id,
            'goal': self.goal,
            'agent_type': self.agent_type,
            'workspace_id': self.workspace_id,
            'permissions': self.permissions,
            'timeout_seconds': self.timeout_seconds,
            'status': self.status,
            'result': self.result,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }


class Provider(Base):
    __tablename__ = 'providers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    base_url = Column(String)
    model_id = Column(String)
    # encrypted credentials stored as opaque text; never return raw in APIs
    credentials_enc = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Agent(Base):
    __tablename__ = 'agents'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    adapter_type = Column(String, nullable=True)
    capabilities = Column(JSONB)
    health = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Artifact(Base):
    __tablename__ = 'artifacts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(String, index=True)
    name = Column(String)
    uri = Column(String)
    metadata = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class MemoryMetadata(Base):
    __tablename__ = 'memory_metadata'
    id = Column(Integer, primary_key=True, autoincrement=True)
    workspace_id = Column(String, index=True)
    key = Column(String, index=True)
    value = Column(JSONB)
    vector = Column(JSONB)  # placeholder; pgvector integration handled separately
    created_at = Column(DateTime(timezone=True), server_default=func.now())

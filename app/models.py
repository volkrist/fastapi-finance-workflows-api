from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db import Base


class Workflow(Base):
    __tablename__ = "workflows"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    steps = relationship(
        "WorkflowStep", back_populates="workflow", order_by="WorkflowStep.order_index"
    )


class WorkflowStep(Base):
    __tablename__ = "workflow_steps"

    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"), nullable=False)
    order_index = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    status = Column(String(50), default="pending")
    completed_at = Column(DateTime(timezone=True), nullable=True)
    workflow = relationship("Workflow", back_populates="steps")


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String(100), nullable=False)
    workflow_id = Column(Integer, ForeignKey("workflows.id"), nullable=True)
    step_id = Column(Integer, nullable=True)
    message = Column(String(500), nullable=True)
    payload_json = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

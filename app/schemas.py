from datetime import datetime
from pydantic import BaseModel


class WorkflowBase(BaseModel):
    name: str
    description: str | None = None


class StepCreate(BaseModel):
    title: str


class WorkflowCreate(WorkflowBase):
    steps: list[StepCreate] = []


class StepOut(BaseModel):
    id: int
    workflow_id: int
    order_index: int
    title: str
    status: str
    completed_at: datetime | None

    class Config:
        from_attributes = True


class WorkflowOut(WorkflowBase):
    id: int
    created_at: datetime
    steps: list[StepOut] = []

    class Config:
        from_attributes = True


class StepCompleteResponse(BaseModel):
    workflow_id: int
    step_id: int
    status: str


class EventCreate(BaseModel):
    event_type: str
    workflow_id: int | None = None
    step_id: int | None = None
    message: str | None = None
    payload: dict | None = None


class EventOut(BaseModel):
    id: int
    event_type: str
    workflow_id: int | None
    step_id: int | None
    message: str | None
    payload_json: str | None
    created_at: datetime

    class Config:
        from_attributes = True

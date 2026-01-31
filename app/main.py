from datetime import datetime
import json

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import engine, Base, get_db
from app import models
from app.schemas import (
    WorkflowCreate,
    WorkflowOut,
    StepCompleteResponse,
    EventCreate,
    EventOut,
)

app = FastAPI(title="Finance Workflows API")

# создать таблицы
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Finance Workflows API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


# ---------- WORKFLOWS ----------


@app.get("/workflows", response_model=list[WorkflowOut])
def list_workflows(db: Session = Depends(get_db)):
    return db.query(models.Workflow).all()


@app.get("/workflows/{workflow_id}", response_model=WorkflowOut)
def get_workflow(workflow_id: int, db: Session = Depends(get_db)):
    workflow = (
        db.query(models.Workflow).filter(models.Workflow.id == workflow_id).first()
    )
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflow


@app.post("/workflows", response_model=WorkflowOut, status_code=201)
def create_workflow(data: WorkflowCreate, db: Session = Depends(get_db)):
    workflow = models.Workflow(
        name=data.name,
        description=data.description,
    )
    db.add(workflow)
    db.flush()

    for idx, step in enumerate(data.steps, start=1):
        db.add(
            models.WorkflowStep(
                workflow_id=workflow.id,
                order_index=idx,
                title=step.title,
            )
        )

    db.add(
        models.Event(
            event_type="workflow_created",
            workflow_id=workflow.id,
            message="Workflow created",
        )
    )

    db.commit()
    db.refresh(workflow)
    return workflow


@app.post(
    "/workflows/{workflow_id}/steps/{step_id}/complete",
    response_model=StepCompleteResponse,
)
def complete_step(
    workflow_id: int,
    step_id: int,
    db: Session = Depends(get_db),
):
    step = (
        db.query(models.WorkflowStep)
        .filter(
            models.WorkflowStep.id == step_id,
            models.WorkflowStep.workflow_id == workflow_id,
        )
        .first()
    )

    if not step:
        raise HTTPException(status_code=404, detail="Step not found")

    if step.status != "completed":
        step.status = "completed"
        step.completed_at = datetime.utcnow()

        db.add(
            models.Event(
                event_type="step_completed",
                workflow_id=workflow_id,
                step_id=step_id,
                message="Step completed",
            )
        )
        db.commit()

    return {
        "workflow_id": workflow_id,
        "step_id": step_id,
        "status": "completed",
    }


# ---------- EVENTS ----------


@app.post("/events", response_model=EventOut, status_code=201)
def create_event(data: EventCreate, db: Session = Depends(get_db)):
    event = models.Event(
        event_type=data.event_type,
        workflow_id=data.workflow_id,
        step_id=data.step_id,
        message=data.message,
        payload_json=json.dumps(data.payload) if data.payload else None,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


@app.get("/events", response_model=list[EventOut])
def list_events(limit: int = 100, db: Session = Depends(get_db)):
    return (
        db.query(models.Event)
        .order_by(models.Event.created_at.desc())
        .limit(limit)
        .all()
    )

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.incident import Incident
from app.schemas.incident import IncidentCreate, IncidentUpdate

VALID_SEVERITIES = {"Critical", "High", "Medium", "Low"}
VALID_STATUSES = {"Open", "Investigating", "Resolved"}


def create_incident(db: Session, data: IncidentCreate):
    if data.severity not in VALID_SEVERITIES:
        raise ValueError("Invalid severity")

    incident = Incident(**data.model_dump())

    db.add(incident)
    db.commit()
    db.refresh(incident)

    return incident


def get_incidents(db: Session):
    statement = select(Incident).order_by(Incident.created_at.desc())

    return db.scalars(statement).all()


def get_incident(db: Session, incident_id: int):
    return db.get(Incident, incident_id)


def update_incident(db: Session, incident: Incident, data: IncidentUpdate):
    updates = data.model_dump(exclude_unset=True)

    if "status" in updates and updates["status"] not in VALID_STATUSES:
        raise ValueError("Invalid status")

    if "severity" in updates and updates["severity"] not in VALID_SEVERITIES:
        raise ValueError("Invalid severity")

    for key, value in updates.items():
        setattr(incident, key, value)

    db.commit()
    db.refresh(incident)

    return incident

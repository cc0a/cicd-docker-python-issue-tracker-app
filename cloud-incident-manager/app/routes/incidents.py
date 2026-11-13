
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.incident import (
    IncidentCreate,
    IncidentUpdate,
    IncidentResponse
)
from app.services import incident_service


router = APIRouter(prefix="/api/incidents", tags=["Incidents"])


@router.post("/", response_model=IncidentResponse, status_code=201)
def create_incident(
    data: IncidentCreate,
    db: Session = Depends(get_db)
):
    try:
        return incident_service.create_incident(db, data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/", response_model=list[IncidentResponse])
def list_incidents(db: Session = Depends(get_db)):
    return incident_service.get_incidents(db)


@router.get("/{incident_id}", response_model=IncidentResponse)
def read_incident(
    incident_id: int,
    db: Session = Depends(get_db)
):
    incident = incident_service.get_incident(db, incident_id)

    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    return incident


@router.patch("/{incident_id}", response_model=IncidentResponse)
def update_incident(
    incident_id: int,
    data: IncidentUpdate,
    db: Session = Depends(get_db)
):
    incident = incident_service.get_incident(db, incident_id)

    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    try:
        return incident_service.update_incident(db, incident, data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

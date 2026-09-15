from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import require_role
from app.models.models import Incident

router = APIRouter(prefix="/api/incidents", tags=["Incidents"])

@router.get("/")
def get_incidents(db: Session = Depends(get_db), current_user=Depends(require_role(["Admin", "Analyst"]))):
    return db.query(Incident).order_by(Incident.timestamp.desc()).limit(20).all()
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import require_role
from app.models.models import Alert

router = APIRouter(prefix="/api/alerts", tags=["Alerts"])

@router.get("/")
def get_alerts(db: Session = Depends(get_db), current_user=Depends(require_role(["Admin", "Analyst"]))):
    return db.query(Alert).order_by(Alert.timestamp.desc()).limit(20).all()
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.models import ActivityLog, User
from app.schemas.schemas import ActivityCreate, ActivityOut
from app.services.orchestrator import orchestrator
from datetime import datetime, timezone

router = APIRouter(prefix="/api/activities", tags=["Activities"])

@router.post("/log")
def log_activity(activity_in: ActivityCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # 1. Store the exact activity in database
    log_entry = ActivityLog(
        user_id=current_user.id,
        action_type=activity_in.action_type,
        bytes_transferred=activity_in.bytes_transferred,
        is_sensitive_file=activity_in.is_sensitive_file,
        failed_attempts=activity_in.failed_attempts,
        privilege_level=activity_in.privilege_level,
        session_duration_sec=activity_in.session_duration_sec
    )
    db.add(log_entry)
    db.commit()

    # 2. Extract telemetry vector dynamically from user inputs
    # If bytes > 500 or sensitive > 0, assume realistic off-hour behavior unless specified
    current_hour = float(datetime.now(timezone.utc).hour)
    raw_telemetry = {
        "login_hour": 2.0 if activity_in.bytes_transferred > 500 else 11.0,
        "files_accessed": 80.0 if activity_in.bytes_transferred > 500 else 8.0,
        "sensitive_files_accessed": 15.0 if activity_in.is_sensitive_file else 0.0,
        "bytes_transferred_mb": float(activity_in.bytes_transferred),
        "failed_logins": float(activity_in.failed_attempts),
        "privilege_level": float(activity_in.privilege_level),
        "session_duration_min": float(activity_in.session_duration_sec / 60.0)
    }

    analysis = orchestrator.analyze_event(current_user.id, raw_telemetry, db)
    return {"message": "Activity analyzed", "assessment": analysis}

@router.get("/recent", response_model=list[ActivityOut])
def get_recent_activities(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(ActivityLog).order_by(ActivityLog.timestamp.desc()).limit(25).all()
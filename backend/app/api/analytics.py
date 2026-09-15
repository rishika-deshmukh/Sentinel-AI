from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import require_role
from app.models.models import User, ActivityLog, Alert, Incident, ThreatAnalysisRecord
from app.schemas.schemas import SimulationTrigger
from app.services.orchestrator import orchestrator

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])

@router.get("/dashboard-stats")
def get_dashboard_stats(db: Session = Depends(get_db), current_user=Depends(require_role(["Admin", "Analyst"]))):
    total_users = db.query(User).count()
    total_activities = db.query(ActivityLog).count()
    total_alerts = db.query(Alert).count()
    total_incidents = db.query(Incident).count()

    latest_assessment = db.query(ThreatAnalysisRecord).order_by(ThreatAnalysisRecord.timestamp.desc()).first()
    avg_risk = 0.0
    records = db.query(ThreatAnalysisRecord).all()
    if records:
        avg_risk = round(sum(r.risk_score for r in records) / len(records), 2)

    return {
        "total_users": total_users,
        "total_activities": total_activities,
        "total_alerts": total_alerts,
        "total_incidents": total_incidents,
        "average_risk": avg_risk,
        "latest_assessment": {
            "risk_score": latest_assessment.risk_score if latest_assessment else 0,
            "action": latest_assessment.game_action if latest_assessment else "ALLOW",
            "shap_attributions": latest_assessment.shap_attributions if latest_assessment else {}
        }
    }

@router.post("/simulate-threat")
def simulate_threat(payload: SimulationTrigger, db: Session = Depends(get_db), current_user=Depends(require_role(["Admin", "Analyst"]))):
    generator = orchestrator.generator
    results = []

    for i in range(payload.iterations):
        if payload.scenario == "DATA_EXFILTRATION":
            sample = {
                "login_hour": 2.0,
                "files_accessed": 80.0,
                "sensitive_files_accessed": 22.0,
                "bytes_transferred_mb": 1400.0 + (i * 200.0),
                "failed_logins": 2.0,
                "privilege_level": 2.0,
                "session_duration_min": 400.0
            }
            action_name = "DATA_EXFILTRATION_BURST"
        elif payload.scenario == "ADAPTIVE_EVASION":
            evasion = min(0.9, 0.15 * (i + 1))
            sample = generator.simulate_adaptive_sample(evasion_level=evasion)
            action_name = "STEALTH_DATA_EGRESS"
        else: # NORMAL
            sample = {
                "login_hour": 11.0,
                "files_accessed": 10.0,
                "sensitive_files_accessed": 0.0,
                "bytes_transferred_mb": 15.0,
                "failed_logins": 0.0,
                "privilege_level": 0.0,
                "session_duration_min": 180.0
            }
            action_name = "ROUTINE_ACCESS"

        # Record into the ActivityLog table so Telemetry count and Audit logs populate
        log_entry = ActivityLog(
            user_id=payload.user_id,
            action_type=action_name,
            bytes_transferred=sample["bytes_transferred_mb"],
            is_sensitive_file=(sample["sensitive_files_accessed"] > 0),
            failed_attempts=int(sample["failed_logins"]),
            privilege_level=int(sample["privilege_level"]),
            session_duration_sec=sample["session_duration_min"] * 60.0
        )
        db.add(log_entry)

        res = orchestrator.analyze_event(payload.user_id, sample, db)
        results.append(res)

    db.commit()
    return {"scenario": payload.scenario, "executions": results}
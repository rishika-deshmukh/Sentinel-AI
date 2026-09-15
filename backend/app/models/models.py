from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="User")  # Admin, Analyst, User
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    activities = relationship("ActivityLog", back_populates="user")
    alerts = relationship("Alert", back_populates="user")

class ActivityLog(Base):
    __tablename__ = "activity_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    action_type = Column(String, nullable=False)  # LOGIN, FILE_ACCESS, DATA_TRANSFER, PRIVILEGE_USE
    resource_id = Column(String, nullable=True)
    bytes_transferred = Column(Float, default=0.0)
    is_sensitive_file = Column(Boolean, default=False)
    failed_attempts = Column(Integer, default=0)
    privilege_level = Column(Integer, default=0)
    session_duration_sec = Column(Float, default=0.0)
    source_ip = Column(String, default="127.0.0.1")

    user = relationship("User", back_populates="activities")

class ThreatAnalysisRecord(Base):
    __tablename__ = "threat_analysis_records"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    raw_features = Column(JSON, nullable=False)
    iforest_score = Column(Float, nullable=False)
    ocsvm_score = Column(Float, nullable=False)
    risk_score = Column(Float, nullable=False)  # 0 to 100
    shap_attributions = Column(JSON, nullable=False)
    game_action = Column(String, nullable=False)  # ALLOW, MONITOR, STEP_UP_AUTH, RESTRICT, REVOKE
    attacker_state = Column(String, default="UNKNOWN")

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    severity = Column(String, nullable=False)  # LOW, MEDIUM, HIGH, CRITICAL
    risk_score = Column(Float, nullable=False)
    triggering_factors = Column(JSON, nullable=False)
    recommended_action = Column(String, nullable=False)
    is_resolved = Column(Boolean, default=False)

    user = relationship("User", back_populates="alerts")

class Incident(Base):
    __tablename__ = "incidents"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    risk_score = Column(Float, nullable=False)
    threat_type = Column(String, default="Adaptive Malicious Insider Threat with Data Exfiltration")
    shap_summary = Column(JSON, nullable=False)
    enforced_action = Column(String, nullable=False)
    status = Column(String, default="OPEN")  # OPEN, INVESTIGATING, MITIGATED
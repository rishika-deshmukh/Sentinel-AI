from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Any

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str
    username: str

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Optional[str] = "User"

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime
    class Config:
        from_attributes = True

class ActivityCreate(BaseModel):
    action_type: str
    bytes_transferred: float = 0.0
    is_sensitive_file: bool = False
    failed_attempts: int = 0
    privilege_level: int = 0
    session_duration_sec: float = 0.0

class ActivityOut(BaseModel):
    id: int
    user_id: int
    timestamp: datetime
    action_type: str
    bytes_transferred: float
    is_sensitive_file: bool
    failed_attempts: int
    class Config:
        from_attributes = True

class SimulationTrigger(BaseModel):
    user_id: int
    scenario: str  # NORMAL, DATA_EXFILTRATION, ABNORMAL_HOURS, ADAPTIVE_EVASION
    iterations: int = 5

class AnalysisResponse(BaseModel):
    user_id: int
    risk_score: float
    iforest_anomaly: bool
    ocsvm_anomaly: bool
    game_action: str
    top_explanations: dict[str, float]
    details: dict[str, Any]
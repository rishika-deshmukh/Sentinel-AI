from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import require_role
from app.models.models import User
from app.schemas.schemas import UserOut

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.get("/", response_model=list[UserOut])
def get_users(db: Session = Depends(get_db), current_user=Depends(require_role(["Admin", "Analyst"]))):
    return db.query(User).all()
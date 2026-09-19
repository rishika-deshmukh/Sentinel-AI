from app.core.database import SessionLocal
from app.models.models import User
from app.core.security import get_password_hash

def reset_admin():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    
    if not admin:
        print("Admin missing. Creating new admin user...")
        new_admin = User(
            username="admin",
            email="admin@sentinel.ai",
            hashed_password=get_password_hash("AdminSecurePass123!"),
            role="Admin"
        )
        db.add(new_admin)
    else:
        print("Admin found. Forcing password reset...")
        admin.hashed_password = get_password_hash("AdminSecurePass123!")
        
    db.commit()
    db.close()
    print("SUCCESS: You can now log in with admin / AdminSecurePass123!")

if __name__ == "__main__":
    reset_admin()
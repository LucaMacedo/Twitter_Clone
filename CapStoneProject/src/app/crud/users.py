from app.db_and_models.models import UserModel, User
from fastapi import HTTPException
from sqlmodel import Session, select

async def create_user(usermodel: UserModel, db: Session):

    existing_user = db.exec(select(User).where(User.email == usermodel.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already in use")
    # Hashen von Passwort
    user = User.from_orm(usermodel)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"success": f"User mit {user.id} erstellt"}
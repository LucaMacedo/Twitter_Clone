from fastapi import APIRouter, Depends, HTTPException
from app.db_and_models.models import UserModel, User
from sqlmodel import Session
from app.db_and_models.session import get_session
from app.crud.users import create_user

router = APIRouter(tags=["Users"])

@router.post("/users")
async def create_user_endpoint(usermodel: UserModel, db: Session = Depends(get_session)):
    return await create_user(usermodel=usermodel, db=db)
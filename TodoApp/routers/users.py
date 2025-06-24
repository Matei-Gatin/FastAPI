# users.py
import re
from fastapi import Depends, HTTPException, Path, APIRouter
from typing import Annotated, Optional
from pydantic import BaseModel, Field, field_validator
from sqlalchemy.orm import Session
from starlette import status
from ..models import Todos, Users
from ..database import SessionLocal
from .auth import get_current_user, bcrypt_context


router = APIRouter(
    prefix="/user",
    tags=["user"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]



class UserResponse(BaseModel):
    user_id: int
    username: str
    user_role: str
    email: str
    first_name: str
    last_name: str
    phone_number: Optional[str] = None



class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str = Field(min_length=8)


class PhoneNumberUpdate(BaseModel):
    phone_number: str

    @field_validator('phone_number')
    @classmethod
    def validate_phone_number(cls, v):
        if not re.match(r'^\+?[\d\s\-\(\)]{10,15}$', v):
            raise ValueError('Invalid phone number format')
        return v.strip()


@router.get("/", status_code=status.HTTP_200_OK,
            response_model=UserResponse)
async def get_current_logged_in_user(user: user_dependency,
                                     db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication required')

    user_model = db.query(Users).filter(Users.id == user.get(
        'id')).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail='User not found')

    return UserResponse(
        user_id=user_model.id,
        username=user_model.username,
        user_role=user_model.role,
        email=user_model.email,
        first_name=user_model.first_name,
        last_name=user_model.last_name,
        phone_number=user_model.phone_number
    )


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(password_data: ChangePasswordRequest,
                          user: user_dependency,
                          db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication required')

    user_model = db.query(Users).filter(Users.id == user.get(
        'id')).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail='User not found')

    if not bcrypt_context.verify(password_data.old_password,
                                 user_model.hashed_password):
        raise HTTPException(status_code=401, detail='Error on '
                                                    'password '
                                                    'change.')

    user_model.hashed_password = bcrypt_context.hash(
        password_data.new_password)

    db.add(user_model)
    db.commit()


@router.put("/phone_number", status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(phone_data: PhoneNumberUpdate,
                              user: user_dependency,
                              db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication required')

    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail='User not found.')

    user_model.phone_number = phone_data.phone_number
    db.commit()







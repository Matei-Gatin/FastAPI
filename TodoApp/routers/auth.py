from datetime import timedelta, datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Annotated
from starlette import status
from ..database import SessionLocal
from ..models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
import secrets
from fastapi.templating import Jinja2Templates


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


SECRET_KEY = secrets.token_hex(32)  # Generate a random secret key
ALGORITHM = "HS256"  # Algorithm for JWT encoding


bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    phone_number: str
    password: str
    role: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
templates = Jinja2Templates(directory="TodoApp/templates")


### Pages ###

@router.get("/login-page")
def render_longin_page(request: Request):
    return templates.TemplateResponse("login.html", {"request":
                                                         request})

@router.get("/register-page")
def render_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request":
                                                         request})


### Endpoints ###
def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: int, role: str,
                        expires_delta:
timedelta = None):
    encode = {
        'sub': username,
        'id': user_id,
        'role': role
    }
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(
    oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {"username": username, "id": user_id, "user_role": user_role}

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
        db: db_dependency,
        create_user_request: CreateUserRequest
):
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        phone_number=create_user_request.phone_number,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True
    )

    db.add(create_user_model)
    db.commit()
    return None


@router.post("/token", response_model=TokenResponse)
async def login_for_access_token(
        form_data: Annotated[
    OAuth2PasswordRequestForm, Depends()],
        db: db_dependency,
):
    user = authenticate_user(form_data.username,
                             form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Failed "
                                                  "Authentication")

    token = create_access_token(user.username, user.id,
                                user.role, timedelta(minutes=30))
    return {'access_token': token, 'token_type': 'bearer'}












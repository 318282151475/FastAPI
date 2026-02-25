from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session
from pydantic import BaseModel
from models import Users
from passlib.context import CryptContext
from database import SessionLocal
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta
from starlette import status

router = APIRouter(
    prefix = '/auth',
    tags=['auth']
)

SECRET_KEY = 'a70b26c182f069410abe94221de3cc17bdf4d2992f1af606b3ba8b0833137a49'
ALGORITHM = 'HS256'


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

class CreateUser(BaseModel):
    email: str
    username : str
    first_name : str
    last_name : str
    password : str
    role : str

class Token(BaseModel):
    access_token: str
    token_type: str
def validate_user(username, password, db):
    user = db.query(Users).filter(Users.username == username).first()

    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False

    return user

def create_access_token(username: str, user_id: int, expires_delta: timedelta):

    encode = {'sub': username, 'id': user_id}
    expires = datetime.utcnow()  + expires_delta            #current time - datetime.utcnow()
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')

        if user_id is None or username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized user')

        return {'username': username, 'id': user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized user')



@router.post("/")
def create_user(db: db_dependency, create_request: CreateUser):
    user_model = Users(
        email = create_request.email,
        username = create_request.username,
        first_name = create_request.first_name,
        last_name = create_request.last_name,
        hashed_password = pwd_context.hash(create_request.password),
        role = create_request.role,
        is_active = True
    )

    db.add(user_model)
    db.commit()


@router.get("/user_data")
def get_user(db: db_dependency):
    return db.query(Users).all()

@router.post("/token", response_model=Token)
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                           db: db_dependency):
    user = validate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(user.username, user.id, timedelta(minutes=20) )
    return {'access_token' :token, 'token_type': 'Bearer'}

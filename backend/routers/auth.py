from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from database import get_db
import models
from schemas import UserCreate, Token

router = APIRouter()
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

SECRET_KEY = 'your-secret-key-change-this-in-production'
ALGORITHM  = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24   # 24 hours

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post('/register')
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail='Username already taken')
    hashed = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed)
    db.add(db_user); db.commit()
    return {'message': 'User created successfully'}

@router.post('/login', response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form.username).first()
    if not user or not pwd_context.verify(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    token = create_access_token({'sub': user.username})
    return {'access_token': token, 'token_type': 'bearer'}

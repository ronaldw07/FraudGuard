# Author: Ronald Wen
# auth.py - Authentication routes: login and JWT token issuance

import os
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from database import get_db
from models import User
from schemas import Token, UserLogin

router = APIRouter(prefix='/auth', tags=['auth'])

JWT_SECRET = os.getenv('JWT_SECRET', 'change-me-in-production')
ALGORITHM = 'HS256'
TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(subject: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    payload = {'sub': subject, 'exp': expire}
    return jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)


def seed_demo_user(db: Session):
    existing = db.query(User).filter(User.username == 'demo').first()
    if not existing:
        user = User(username='demo', hashed_password=hash_password('fraudguard123'))
        db.add(user)
        db.commit()


@router.post('/login', response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == credentials.username).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username or password',
        )
    token = create_access_token(subject=user.username)
    return Token(access_token=token, token_type='bearer')

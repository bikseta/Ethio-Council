from datetime import timedelta, datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth import create_access_token, get_current_user, get_password_hash, verify_password
from config import settings
from database import get_db
from models import User
from schemas import LoginRequest, RefreshRequest, Token, UserCreate, UserRead


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter((User.email == payload.email) | (User.username == payload.username)).first()
    if existing:
        raise HTTPException(status_code=400, detail="User with email or username already exists")

    user = User(
        email=payload.email,
        username=payload.username,
        password_hash=get_password_hash(payload.password),
        full_name=payload.full_name,
        phone=payload.phone,
        role=payload.role,
        language_preference=payload.language_preference,
        region_id=payload.region_id,
        zone_id=payload.zone_id,
        woreda_id=payload.woreda_id,
        kebele_id=payload.kebele_id,
        is_verified=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=Token)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    user.last_login_at = datetime.utcnow()
    db.add(user)
    db.commit()
    token = create_access_token(
        {"sub": str(user.id), "email": user.email, "role": user.role.value},
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
    )
    return Token(access_token=token)


@router.get("/me", response_model=UserRead)
def me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/refresh", response_model=Token)
def refresh(payload: RefreshRequest, db: Session = Depends(get_db)):
    identifier = get_current_user.__globals__["verify_token"](payload.token)
    user = db.query(User).filter((User.id == identifier) | (User.email == identifier)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    token = create_access_token({"sub": str(user.id), "email": user.email, "role": user.role.value})
    return Token(access_token=token)

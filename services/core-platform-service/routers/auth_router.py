from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from database import get_db
from models import User
from schemas import LoginRequest, TokenResponse, UserCreate, UserOut
from auth import verify_password, get_password_hash, create_access_token, get_current_user

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is inactive")
    user.last_login = datetime.utcnow()
    db.commit()
    token = create_access_token({"sub": str(user.id), "email": user.email, "role": user.role.value})
    return TokenResponse(
        access_token=token,
        user_role=user.role.value,
        user_id=str(user.id),
        full_name=user.full_name,
    )

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(request: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == request.email).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    user = User(
        email=request.email,
        full_name=request.full_name,
        hashed_password=get_password_hash(request.password),
        role=request.role,
        denomination_id=request.denomination_id,
        region_id=request.region_id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

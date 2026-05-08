from fastapi import APIRouter, HTTPException, Depends, Body
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from app.core.security import create_token, verify_token
from app.models.user import UserInDB, users_db

router = APIRouter()

class RegisterPayload(BaseModel):
    username: str
    password: str
    full_name: str = "NAS User"
    email: str = "user@cloudnas.local"

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if not user or user.password != form_data.password:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    return {"access_token": create_token(user.username), "token_type": "bearer"}

@router.post("/register")
def register(payload: RegisterPayload = Body(...)):
    if payload.username in users_db:
        raise HTTPException(status_code=400, detail="用户已存在")
    user = UserInDB(
        username=payload.username,
        full_name=payload.full_name,
        email=payload.email,
        password=payload.password,
    )
    users_db[payload.username] = user
    return {"message": "注册成功", "username": user.username}

@router.get("/me")
def get_current_user(token: str = Depends(verify_token)):
    return {"username": token}

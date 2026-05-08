from fastapi import APIRouter, Depends, HTTPException, Body
from app.core.security import verify_token
from app.models.user import UserInDB, users_db

router = APIRouter()

@router.get("/list")
def list_users(token: str = Depends(verify_token)):
    users = [{"username": user.username, "full_name": user.full_name, "email": user.email} for user in users_db.values()]
    return {"users": users}

@router.post("/create")
def create_user(username: str = Body(...), password: str = Body(...), full_name: str = Body(""), email: str = Body(""), token: str = Depends(verify_token)):
    if username in users_db:
        raise HTTPException(status_code=400, detail="用户已存在")
    users_db[username] = UserInDB(username=username, full_name=full_name or username, email=email or f"{username}@cloudnas.local", password=password)
    return {"message": "用户创建成功", "username": username}

@router.delete("/delete")
def delete_user(username: str = Body(...), token: str = Depends(verify_token)):
    if username not in users_db:
        raise HTTPException(status_code=404, detail="用户不存在")
    users_db.pop(username)
    return {"message": "用户已删除", "username": username}

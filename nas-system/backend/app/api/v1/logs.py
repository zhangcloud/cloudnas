from fastapi import APIRouter, Depends
from app.core.security import verify_token
from datetime import datetime

router = APIRouter()

fake_logs = [
    {"timestamp": datetime.utcnow().isoformat() + 'Z', "level": "INFO", "message": "系统启动成功"},
    {"timestamp": datetime.utcnow().isoformat() + 'Z', "level": "WARN", "message": "存储池 Archive 状态 degraded"},
    {"timestamp": datetime.utcnow().isoformat() + 'Z', "level": "INFO", "message": "用户 admin 登录"},
]

@router.get("/list")
def list_logs(token: str = Depends(verify_token)):
    return {"logs": fake_logs}

@router.get("/latest")
def latest_logs(token: str = Depends(verify_token)):
    return {"latest": fake_logs[-10:]}

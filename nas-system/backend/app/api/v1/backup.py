from fastapi import APIRouter, Depends
from app.core.security import verify_token

router = APIRouter()

fake_backups = [
    {"id": "bkp-001", "name": "weekly-snapshot", "created_at": "2026-05-08T08:00:00Z", "status": "available"},
    {"id": "bkp-002", "name": "daily-config", "created_at": "2026-05-07T22:00:00Z", "status": "available"},
]

@router.get("/list")
def list_backups(token: str = Depends(verify_token)):
    return {"backups": fake_backups}

@router.post("/create")
def create_backup(name: str, token: str = Depends(verify_token)):
    backup = {"id": f"bkp-{len(fake_backups)+1:03d}", "name": name, "created_at": "2026-05-08T12:00:00Z", "status": "available"}
    fake_backups.append(backup)
    return {"message": "备份创建成功", "backup": backup}

@router.post("/restore")
def restore_backup(backup_id: str, token: str = Depends(verify_token)):
    for item in fake_backups:
        if item["id"] == backup_id:
            return {"message": "备份恢复已触发", "backup": item}
    return {"message": "未找到指定备份", "backup_id": backup_id}

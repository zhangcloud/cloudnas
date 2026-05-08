from fastapi import APIRouter, Depends, Body
from app.core.security import verify_token
from datetime import datetime

router = APIRouter()

fake_tasks = [
    {"id": "task1", "name": "每日备份", "type": "backup", "schedule": "0 2 * * *", "status": "enabled"},
    {"id": "task2", "name": "周末磁盘检查", "type": "scrub", "schedule": "0 3 * * 0", "status": "enabled"},
]

@router.get("/list")
def list_tasks(token: str = Depends(verify_token)):
    return {"tasks": fake_tasks}

@router.post("/create")
def create_task(name: str = Body(...), type: str = Body(...), schedule: str = Body(...), token: str = Depends(verify_token)):
    task = {"id": f"task{len(fake_tasks)+1}", "name": name, "type": type, "schedule": schedule, "status": "enabled"}
    fake_tasks.append(task)
    return {"message": "任务已创建", "task": task}

@router.post("/toggle")
def toggle_task(task_id: str = Body(...), enable: bool = Body(...), token: str = Depends(verify_token)):
    for task in fake_tasks:
        if task["id"] == task_id:
            task["status"] = "enabled" if enable else "disabled"
            return {"message": "任务状态已更新", "task": task}
    return {"message": "未找到任务", "task_id": task_id}

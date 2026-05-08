from fastapi import APIRouter, Depends, Body, HTTPException
from app.core.security import verify_token
from datetime import datetime

router = APIRouter()

fake_snapshots = [
    {"id": "snap1", "name": "系统快照 2026-05-08", "created_at": "2026-05-08T08:00:00Z", "status": "available"},
    {"id": "snap2", "name": "配置备份 2026-05-07", "created_at": "2026-05-07T22:00:00Z", "status": "available"},
]

@router.get("/list")
def list_snapshots(token: str = Depends(verify_token)):
    return {"snapshots": fake_snapshots}

@router.post("/create")
def create_snapshot(name: str = Body(...), token: str = Depends(verify_token)):
    snap = {"id": f"snap{len(fake_snapshots)+1}", "name": name, "created_at": datetime.utcnow().isoformat() + 'Z', "status": "available"}
    fake_snapshots.append(snap)
    return {"message": "快照已创建", "snapshot": snap}

@router.post("/restore")
def restore_snapshot(snapshot_id: str = Body(...), token: str = Depends(verify_token)):
    snapshot = next((s for s in fake_snapshots if s["id"] == snapshot_id), None)
    if not snapshot:
        raise HTTPException(status_code=404, detail="快照未找到")
    return {"message": "快照恢复已触发", "snapshot": snapshot}

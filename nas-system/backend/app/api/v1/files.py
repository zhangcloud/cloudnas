import os
import shutil
from pathlib import Path
from typing import List

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Body
from fastapi.responses import FileResponse
from app.core.security import verify_token
from app.core.config import settings

router = APIRouter()
BASE_PATH = Path(settings.local_storage_path)
BASE_PATH.mkdir(parents=True, exist_ok=True)

class FileEntry:
    def __init__(self, name: str, path: str, is_dir: bool, size: int):
        self.name = name
        self.path = path
        self.is_dir = is_dir
        self.size = size

    def dict(self):
        return {
            "name": self.name,
            "path": self.path,
            "is_dir": self.is_dir,
            "size": self.size,
        }


def get_target(path: str) -> Path:
    target = (BASE_PATH / path).resolve()
    if not str(target).startswith(str(BASE_PATH)):
        raise HTTPException(status_code=400, detail="非法路径")
    return target

@router.get("/list")
def list_files(path: str = "", token: str = Depends(verify_token)):
    target = get_target(path)
    if not target.exists() or not target.is_dir():
        raise HTTPException(status_code=404, detail="文件夹不存在")
    entries: List[FileEntry] = []
    for item in sorted(target.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower())):
        entries.append(FileEntry(
            name=item.name,
            path=str(item.relative_to(BASE_PATH)),
            is_dir=item.is_dir(),
            size=item.stat().st_size,
        ))
    return {"path": str(target.relative_to(BASE_PATH)), "entries": [e.dict() for e in entries]}

@router.post("/mkdir")
def make_directory(path: str = Body(...), token: str = Depends(verify_token)):
    target = get_target(path)
    target.mkdir(parents=True, exist_ok=True)
    return {"message": "创建成功", "path": str(target.relative_to(BASE_PATH))}

@router.post("/upload")
async def upload_file(path: str = Body(""), file: UploadFile = File(...), token: str = Depends(verify_token)):
    target = get_target(path)
    if not target.exists():
        target.mkdir(parents=True, exist_ok=True)
    destination = target / file.filename
    content = await file.read()
    destination.write_bytes(content)
    return {"message": "上传成功", "path": str(destination.relative_to(BASE_PATH))}

@router.get("/download")
def download_file(path: str, token: str = Depends(verify_token)):
    target = get_target(path)
    if not target.exists() or target.is_dir():
        raise HTTPException(status_code=404, detail="文件不存在")
    return FileResponse(path=target, filename=target.name)

@router.get("/acl")
def get_acl(path: str, token: str = Depends(verify_token)):
    target = get_target(path)
    if not target.exists():
        raise HTTPException(status_code=404, detail="路径不存在")
    # Simulate ACL retrieval
    fake_acls = [
        {"user": "admin", "permissions": ["read", "write", "execute"]},
        {"user": "guest", "permissions": ["read"]}
    ]
    return {"path": str(target.relative_to(BASE_PATH)), "acls": fake_acls}

@router.post("/acl")
def set_acl(path: str, acls: List[dict], token: str = Depends(verify_token)):
    target = get_target(path)
    if not target.exists():
        raise HTTPException(status_code=404, detail="路径不存在")
    # Simulate ACL setting
    return {"message": "ACL 设置成功", "path": str(target.relative_to(BASE_PATH)), "acls": acls}

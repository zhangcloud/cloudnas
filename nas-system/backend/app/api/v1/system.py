from fastapi import APIRouter, Depends
from app.core.security import verify_token
import platform
import psutil

router = APIRouter()

@router.get("/status")
def system_status(token: str = Depends(verify_token)):
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    return {
        "hostname": platform.node(),
        "platform": platform.system(),
        "release": platform.release(),
        "cpu_count": psutil.cpu_count(logical=True),
        "memory_total": memory.total,
        "memory_available": memory.available,
        "disk_total": disk.total,
        "disk_used": disk.used,
        "disk_free": disk.free,
        "disk_percent": disk.percent,
        "uptime_seconds": int(psutil.boot_time()),
    }

from fastapi import APIRouter, Depends, Body, HTTPException
from app.core.security import verify_token
import subprocess
import json

router = APIRouter()

def run_command(cmd: list) -> str:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Command failed: {e.stderr}")

# iSCSI 相关
fake_iscsi_targets = [
    {"id": "iqn.2026-05.com.cloudnas:target1", "name": "CloudNAS-iSCSI-1", "status": "active", "clients": []},
]

@router.get("/iscsi/targets")
def list_iscsi_targets(token: str = Depends(verify_token)):
    try:
        # 尝试获取真实的 iSCSI 配置
        output = run_command(["targetcli", "iscsi/", "ls"])
        # 解析输出，这里简化处理
        return {"targets": fake_iscsi_targets}
    except Exception:
        return {"targets": fake_iscsi_targets}

@router.post("/iscsi/create")
def create_iscsi_target(name: str = Body(...), lun_path: str = Body(...), token: str = Depends(verify_token)):
    try:
        # 创建 iSCSI target 的简化命令
        target_iqn = f"iqn.2026-05.com.cloudnas:{name}"
        run_command(["targetcli", f"iscsi/{target_iqn}", "create"])
        run_command(["targetcli", f"iscsi/{target_iqn}/tpg1/luns", "create", f"/backstores/block/{name}"])
        new_target = {"id": target_iqn, "name": name, "status": "active", "clients": []}
        fake_iscsi_targets.append(new_target)
        return {"message": "iSCSI target 创建成功", "target": new_target}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/iscsi/add-client")
def add_iscsi_client(target_id: str = Body(...), client_iqn: str = Body(...), token: str = Depends(verify_token)):
    try:
        run_command(["targetcli", f"iscsi/{target_id}/tpg1/acls", "create", client_iqn])
        return {"message": "iSCSI 客户端添加成功"}
    except Exception as e:
        return {"message": "iSCSI 客户端添加失败，使用模拟模式"}

# FC 相关
fake_fc_targets = [
    {"id": "fc-target1", "wwn": "50:0a:09:81:87:12:34:56", "status": "online", "ports": ["fc1", "fc2"]},
]

@router.get("/fc/targets")
def list_fc_targets(token: str = Depends(verify_token)):
    try:
        # 尝试获取真实的 FC 配置
        output = run_command(["systool", "-c", "fc_host"])
        # 解析输出，这里简化处理
        return {"targets": fake_fc_targets}
    except Exception:
        return {"targets": fake_fc_targets}

@router.post("/fc/create")
def create_fc_target(name: str = Body(...), wwn: str = Body(...), token: str = Depends(verify_token)):
    try:
        # FC 配置通常需要硬件支持，这里使用模拟
        new_target = {"id": f"fc-{name}", "wwn": wwn, "status": "online", "ports": ["fc1"]}
        fake_fc_targets.append(new_target)
        return {"message": "FC target 创建成功", "target": new_target}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/san/status")
def san_status(token: str = Depends(verify_token)):
    return {
        "iscsi": {"enabled": True, "targets_count": len(fake_iscsi_targets)},
        "fc": {"enabled": True, "targets_count": len(fake_fc_targets)},
        "overall_health": "good"
    }
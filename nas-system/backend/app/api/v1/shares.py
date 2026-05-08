from fastapi import APIRouter, Depends, HTTPException, Body
from app.core.security import verify_token
import subprocess
import os
from typing import List, Optional

router = APIRouter()

class NfsShare:
    def __init__(self, path: str, clients: List[str], options: str = "rw,sync,no_subtree_check"):
        self.path = path
        self.clients = clients
        self.options = options

class CifsShare:
    def __init__(self, name: str, path: str, comment: str = "", public: bool = False, writable: bool = True):
        self.name = name
        self.path = path
        self.comment = comment
        self.public = public
        self.writable = writable

fake_nfs_shares = [
    NfsShare("/tmp/cloudnas_storage/Public", ["192.168.1.0/24"], "rw,sync,no_subtree_check"),
    NfsShare("/tmp/cloudnas_storage/Private", ["192.168.1.100"], "rw,sync,no_subtree_check"),
]

fake_cifs_shares = [
    CifsShare("Public", "/tmp/cloudnas_storage/Public", "Public share", True, True),
    CifsShare("Private", "/tmp/cloudnas_storage/Private", "Private share", False, True),
]

def is_production():
    """检查是否为生产环境"""
    return os.getenv("ENVIRONMENT") == "production"

def run_command(cmd: list) -> str:
    if not is_production():
        # 开发环境：模拟成功
        return "simulated success"
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Command failed: {e.stderr}")

# NFS 共享管理
@router.get("/nfs/list")
def list_nfs_shares(token: str = Depends(verify_token)):
    if not is_production():
        return {"shares": [{"path": s.path, "clients": s.clients, "options": s.options} for s in fake_nfs_shares]}
    
    try:
        # 尝试读取真实的 /etc/exports
        if os.path.exists("/etc/exports"):
            with open("/etc/exports", "r") as f:
                exports_content = f.read()
            # 解析 exports 文件，这里简化处理
            return {"shares": fake_nfs_shares, "exports_content": exports_content}
        else:
            return {"shares": fake_nfs_shares, "exports_content": ""}
    except Exception:
        return {"shares": fake_nfs_shares, "exports_content": ""}

@router.post("/nfs/create")
def create_nfs_share(path: str = Body(...), clients: List[str] = Body(...), options: str = Body("rw,sync,no_subtree_check"), token: str = Depends(verify_token)):
    if not is_production():
        # 开发环境：只添加到内存
        share = NfsShare(path, clients, options)
        fake_nfs_shares.append(share)
        return {"message": "NFS 共享创建成功", "share": {"path": path, "clients": clients, "options": options}}
    
    try:
        # 创建 NFS 导出
        export_line = f"{path} {' '.join(clients)}({options})"
        with open("/etc/exports", "a") as f:
            f.write(f"\n{export_line}\n")

        # 重新导出 NFS
        run_command(["exportfs", "-ra"])

        share = NfsShare(path, clients, options)
        fake_nfs_shares.append(share)
        return {"message": "NFS 共享创建成功", "share": {"path": path, "clients": clients, "options": options}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/nfs/delete")
def delete_nfs_share(path: str = Body(...), token: str = Depends(verify_token)):
    global fake_nfs_shares
    
    if not is_production():
        # 开发环境：从内存移除
        fake_nfs_shares = [share for share in fake_nfs_shares if share.path != path]
        return {"message": "NFS 共享删除成功", "path": path}
    
    try:
        # 从 /etc/exports 中移除
        if os.path.exists("/etc/exports"):
            with open("/etc/exports", "r") as f:
                lines = f.readlines()

            with open("/etc/exports", "w") as f:
                for line in lines:
                    if not line.strip().startswith(path):
                        f.write(line)

            # 重新导出 NFS
            run_command(["exportfs", "-ra"])

        fake_nfs_shares = [share for share in fake_nfs_shares if share.path != path]
        return {"message": "NFS 共享删除成功", "path": path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# CIFS/SMB 共享管理
@router.get("/cifs/list")
def list_cifs_shares(token: str = Depends(verify_token)):
    if not is_production():
        return {"shares": [{"name": s.name, "path": s.path, "comment": s.comment, "public": s.public, "writable": s.writable} for s in fake_cifs_shares]}
    
    try:
        # 尝试读取真实的 /etc/samba/smb.conf
        if os.path.exists("/etc/samba/smb.conf"):
            with open("/etc/samba/smb.conf", "r") as f:
                smb_content = f.read()
            return {"shares": fake_cifs_shares, "smb_content": smb_content}
        else:
            return {"shares": fake_cifs_shares, "smb_content": ""}
    except Exception:
        return {"shares": fake_cifs_shares, "smb_content": ""}

@router.post("/cifs/create")
def create_cifs_share(name: str = Body(...), path: str = Body(...), comment: str = Body(""), public: bool = Body(False), writable: bool = Body(True), token: str = Depends(verify_token)):
    if not is_production():
        # 开发环境：只添加到内存
        share = CifsShare(name, path, comment, public, writable)
        fake_cifs_shares.append(share)
        return {"message": "CIFS 共享创建成功", "share": {"name": name, "path": path, "comment": comment, "public": public, "writable": writable}}
    
    try:
        # 添加到 /etc/samba/smb.conf
        share_config = f"""
[{name}]
   path = {path}
   comment = {comment}
   public = {'yes' if public else 'no'}
   writable = {'yes' if writable else 'no'}
   create mask = 0644
   directory mask = 0755
"""

        with open("/etc/samba/smb.conf", "a") as f:
            f.write(share_config)

        # 重启 Samba 服务
        run_command(["systemctl", "restart", "smbd"])
        run_command(["systemctl", "restart", "nmbd"])

        share = CifsShare(name, path, comment, public, writable)
        fake_cifs_shares.append(share)
        return {"message": "CIFS 共享创建成功", "share": {"name": name, "path": path, "comment": comment, "public": public, "writable": writable}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/cifs/delete")
def delete_cifs_share(name: str = Body(...), token: str = Depends(verify_token)):
    global fake_cifs_shares
    
    if not is_production():
        # 开发环境：从内存移除
        fake_cifs_shares = [share for share in fake_cifs_shares if share.name != name]
        return {"message": "CIFS 共享删除成功", "name": name}
    
    try:
        # 从 /etc/samba/smb.conf 中移除
        if os.path.exists("/etc/samba/smb.conf"):
            with open("/etc/samba/smb.conf", "r") as f:
                content = f.read()

            # 移除共享配置块
            start_marker = f"[{name}]"
            end_marker = "\n["
            start_idx = content.find(start_marker)
            if start_idx != -1:
                end_idx = content.find(end_marker, start_idx + len(start_marker))
                if end_idx == -1:
                    end_idx = len(content)
                new_content = content[:start_idx] + content[end_idx:]
                with open("/etc/samba/smb.conf", "w") as f:
                    f.write(new_content)

            # 重启 Samba 服务
            run_command(["systemctl", "restart", "smbd"])
            run_command(["systemctl", "restart", "nmbd"])

        fake_cifs_shares = [share for share in fake_cifs_shares if share.name != name]
        return {"message": "CIFS 共享删除成功", "name": name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 通用共享管理 (向后兼容)
@router.get("/list")
def list_shares(token: str = Depends(verify_token)):
    nfs_shares = [{"id": f"nfs-{i}", "name": share.path.split('/')[-1], "path": share.path, "protocol": "NFS", "access": f"{share.clients} ({share.options})"} for i, share in enumerate(fake_nfs_shares)]
    cifs_shares = [{"id": f"cifs-{i}", "name": share.name, "path": share.path, "protocol": "CIFS", "access": f"{'Public' if share.public else 'Private'} ({'RW' if share.writable else 'RO'})"} for i, share in enumerate(fake_cifs_shares)]
    return {"shares": nfs_shares + cifs_shares}

@router.post("/create")
def create_share(name: str = Body(...), path: str = Body(...), protocol: str = Body("NFS"), access: str = Body("Everyone"), token: str = Depends(verify_token)):
    if protocol.upper() == "NFS":
        clients = ["192.168.1.0/24"] if access == "Everyone" else ["192.168.1.100"]
        return create_nfs_share(path, clients, "rw,sync,no_subtree_check")
    elif protocol.upper() == "CIFS":
        public = access == "Everyone"
        return create_cifs_share(name, path, f"{name} share", public, True)
    else:
        raise HTTPException(status_code=400, detail="不支持的协议")

@router.delete("/delete")
def delete_share(share_id: str = Body(...), token: str = Depends(verify_token)):
    if share_id.startswith("nfs-"):
        path = fake_nfs_shares[int(share_id.split("-")[1])].path
        return delete_nfs_share(path)
    elif share_id.startswith("cifs-"):
        name = fake_cifs_shares[int(share_id.split("-")[1])].name
        return delete_cifs_share(name)
    else:
        raise HTTPException(status_code=400, detail="无效的共享ID")

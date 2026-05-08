from fastapi import APIRouter, Depends
from app.core.security import verify_token

router = APIRouter()

fake_network = {
    "hostname": "cloudnas.local",
    "ip_address": "192.168.1.100",
    "netmask": "255.255.255.0",
    "gateway": "192.168.1.1",
    "dns": ["8.8.8.8", "8.8.4.4"],
    "services": {
        "SMB": "running",
        "NFS": "running",
        "FTP": "stopped",
    },
}

@router.get("/status")
def network_status(token: str = Depends(verify_token)):
    return fake_network

@router.post("/update")
def update_network(ip_address: str, netmask: str, gateway: str, dns: list[str], token: str = Depends(verify_token)):
    fake_network.update({"ip_address": ip_address, "netmask": netmask, "gateway": gateway, "dns": dns})
    return {"message": "网络配置已更新", "network": fake_network}

@router.post("/toggle-service")
def toggle_service(service: str, action: str, token: str = Depends(verify_token)):
    if service not in fake_network["services"]:
        return {"message": "未知服务"}
    fake_network["services"][service] = "running" if action == "start" else "stopped"
    return {"message": "服务状态已更新", "services": fake_network["services"]}

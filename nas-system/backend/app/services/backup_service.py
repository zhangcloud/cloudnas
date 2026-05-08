from datetime import datetime

fake_backups = []

def create_backup(name: str) -> dict:
    item = {"id": f"bkp-{len(fake_backups)+1:03d}", "name": name, "created_at": datetime.utcnow().isoformat() + 'Z', "status": "available"}
    fake_backups.append(item)
    return item

def list_backups() -> list:
    return fake_backups

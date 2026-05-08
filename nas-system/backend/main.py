from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import auth, files, storage, backup, system, users, shares, network, tasks, logs, apps, snapshots, san

app = FastAPI(title="CloudNAS Backend", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(files.router, prefix="/api/v1/files", tags=["files"])
app.include_router(storage.router, prefix="/api/v1/storage", tags=["storage"])
app.include_router(backup.router, prefix="/api/v1/backup", tags=["backup"])
app.include_router(system.router, prefix="/api/v1/system", tags=["system"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(shares.router, prefix="/api/v1/shares", tags=["shares"])
app.include_router(network.router, prefix="/api/v1/network", tags=["network"])
app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["tasks"])
app.include_router(logs.router, prefix="/api/v1/logs", tags=["logs"])
app.include_router(apps.router, prefix="/api/v1/apps", tags=["apps"])
app.include_router(snapshots.router, prefix="/api/v1/snapshots", tags=["snapshots"])
app.include_router(san.router, prefix="/api/v1/san", tags=["san"])

@app.get("/api/v1/health")
def health_check():
    return {"status": "ok", "service": "cloudnas"}

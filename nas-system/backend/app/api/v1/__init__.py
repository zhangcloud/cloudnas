from fastapi import APIRouter

router = APIRouter()

from . import auth, files, storage, backup, system, users, shares, network, tasks, logs, apps, snapshots, san  # noqa: F401

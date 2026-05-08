from pydantic import BaseModel
from typing import List

class ACL(BaseModel):
    user: str
    permissions: List[str]  # e.g., ["read", "write", "execute"]

class FileACL(BaseModel):
    path: str
    acls: List[ACL]

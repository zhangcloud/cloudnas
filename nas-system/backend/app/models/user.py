from pydantic import BaseModel

class User(BaseModel):
    username: str
    full_name: str
    email: str

class UserInDB(User):
    password: str

users_db = {
    "admin": UserInDB(username="admin", full_name="Administrator", email="admin@cloudnas.local", password="admin123"),
}

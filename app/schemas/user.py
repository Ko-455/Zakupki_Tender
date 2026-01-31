from fastapi_users import schemas
from typing import Optional

class UserRead(schemas.BaseUser[int]):
    preferences: Optional[str] = None

class UserCreate(schemas.BaseUserCreate):
    preferences: Optional[str] = None

class UserUpdate(schemas.BaseUserUpdate):
    preferences: Optional[str] = None

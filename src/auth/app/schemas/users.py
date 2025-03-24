from pydantic import BaseModel, ConfigDict, EmailStr


class SUser(BaseModel):
    model_config = ConfigDict(strict=True)

    id: int
    email: EmailStr
    role: str
    hash_password: bytes


class SInfoUser(BaseModel):
    model_config = ConfigDict(strict=True)

    user_id: int
    nickname: str
    is_active: bool
    is_verified: bool
    avatar: bool


class SRegisterUser(BaseModel):
    model_config = ConfigDict(strict=True)

    email: EmailStr
    nickname: str
    password: str

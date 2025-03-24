from typing import Annotated

from annotated_types import MaxLen, MinLen
from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    PositiveInt,
    model_validator,
)

from auth.app.exceptions.data import PasswordNotMatchException


class SBaseSignUp(BaseModel):
    model_config = ConfigDict(strict=True)

    nickname: Annotated[str, MinLen(2), MaxLen(25)]
    email: Annotated[EmailStr, MinLen(5), MaxLen(80)]
    password: Annotated[str, MinLen(8), MaxLen(100)]
    confirm_password: Annotated[str, MinLen(8), MaxLen(100)]

    @model_validator(mode="after")
    def check_passwords_match(self) -> "SBaseSignUp":
        if self.password != self.confirm_password:
            raise PasswordNotMatchException()
        return self


class SBaseSignIn(BaseModel):
    model_config = ConfigDict(strict=True)

    email: Annotated[EmailStr, MinLen(5), MaxLen(60)]
    password: Annotated[str, MinLen(8), MaxLen(50)]


class SSuccessfulRequest(BaseModel):
    message: str = "success"


class TokenInfo(BaseModel):
    model_config = ConfigDict(strict=True)

    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class SAddInfoUser(BaseModel):

    user_id: PositiveInt
    nickname: str

from typing import Literal

from pydantic import BaseModel, Field, EmailStr, ConfigDict


class UserCreateRequestSchema(BaseModel):
    email: EmailStr = Field(description='Email пользователя')
    password: str = Field(
        min_length=8, description='Пароль (минимум 8 символов)'
    )
    role: Literal['buyer', 'seller'] = Field(
        default='buyer', description='Роль: "buyer" или "seller"'
    )


class UserResponseSchema(BaseModel):
    id: int = Field(description='Уникальный идентификатор пользователя')
    email: EmailStr = Field(description='Email пользователя')
    is_active: bool = Field(
        default=True,
        description='Активность пользователя (показывается или нет)',
    )
    role: Literal['buyer', 'seller', 'admin'] = Field(
        description='Роль пользователя'
    )

    model_config = ConfigDict(from_attributes=True)


class AuthRequestSchema(BaseModel):
    username: EmailStr = Field(description='Email пользователя')
    password: str = Field(
        min_length=8, description='Пароль (минимум 8 символов)'
    )


class AuthResponseSchema(BaseModel):
    access_token: str = Field(description='Access token')
    refresh_token: str = Field(description='Refresh token')
    token_type: Literal['bearer'] = 'bearer'

    model_config = ConfigDict(from_attributes=True)


class RefreshTokenResponseSchema(BaseModel):
    access_token: str = Field(description='Access token')
    token_type: Literal['bearer'] = 'bearer'

    model_config = ConfigDict(from_attributes=True)

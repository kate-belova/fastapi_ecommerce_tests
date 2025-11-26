from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field, ConfigDict


class HealthStatus(str, Enum):
    HEALTHY = 'healthy'
    UNHEALTHY = 'unhealthy'


class HealthResponseSchema(BaseModel):
    status: HealthStatus = Field(description='Service health status')
    timestamp: datetime = Field(description='Current time in UTC')
    service: Literal['FastAPI Ecommerce'] = 'FastAPI Ecommerce'

    model_config = ConfigDict(from_attributes=True)


class RootResponseSchema(BaseModel):
    message: Literal['Добро пожаловать в API интернет-магазина!'] = (
        'Добро пожаловать в API интернет-магазина!'
    )

    model_config = ConfigDict(from_attributes=True)

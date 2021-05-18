from pydantic import BaseModel, Field, EmailStr


class PostSchema(BaseModel):
    id: int = Field(default=None)
    title: str = Field(...)
    content: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "title": "TEST post title",
                "content": "TEST post content"
            }
        }


class UserSchema(BaseModel):
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "fullname": "wooseok jang",
                "email": "mmyu2090@gmail.com",
                "password": "SuperPowerfulPW"
            }
        }


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "mmyu2090@gmail.com",
                "password": "SuperPowerfulPW"
            }
        }


class DeviceStatusSchema(BaseModel):
    deviceSerial: int = Field(...)
    longitude: float = Field(...)
    latitude: float = Field(...)
    temp: float = Field(...)
    accelMax: float = Field(...)
    heartRate: int = Field(...)
    batteryLevel: int = Field(...)
    critical: int = Field(...)
    button: int = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "deviceSerial": "1",
                "longitude": "128.39457",
                "latitude": "36.14199",
                "temp": "36.5",
                "accelMax": "0.5",
                "heartRate": "80",
                "batteryLevel": "50",
                "critical": "0",
                "button": "0"
            }
        }

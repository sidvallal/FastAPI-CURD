
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class StudentCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(ge=1, le=120)


class StudentUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(ge=1, le=120)


class StudentResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int

    model_config = ConfigDict(from_attributes=True)

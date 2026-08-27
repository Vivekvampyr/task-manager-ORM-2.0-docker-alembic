from pydantic import BaseModel, Field, ConfigDict, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8,max_length=128)
    first_name: str = Field(min_length=1,max_length=100)
    last_name: str = Field(min_length=1, max_length=100)

class UserResponse(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

from pydantic import BaseModel, EmailStr
from typing import Optional


class RegisterDTO(BaseModel):
    username: str
    email: EmailStr
    password: str

class LoginDTO(BaseModel):
    username: str
    password: str

class ChangePasswordDTO(BaseModel):
    username: str
    current_password: str
    new_password: str

class ForgotPasswordDTO(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None


class GetPackageDTO(BaseModel):
    package_id: int
    package_name: str
    download_speed: int
    upload_speed: int
    monthly_price: float

class CreateCustomerDTO(BaseModel):
    package_id: int
    customer_name: str


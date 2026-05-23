
from fastapi import APIRouter, Request
from auth.services.registrationService import registration_service
from auth.services.loginService import login_service
from auth.services.forgotPasswordService import forgot_password_service
from auth.services.changePasswordService import change_password_service
from auth.dtos.dtos import RegisterDTO, LoginDTO, ForgotPasswordDTO, ChangePasswordDTO, CreateCustomerDTO, ChangePasswordAVDTO
from auth.services.deletePackageService import delete_package_service
from auth.services.createCustomerService import create_customer_service
from auth.services.deleteAllCustomersService import delete_all_customers_service
from auth.services.changePasswordAfterVerificationService import change_password_service_after_verification_service
router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/registration")
def register_user(user: RegisterDTO):
    try:
        return registration_service(user)
    except:
        return {"message": "error thrown from registration service"}


@router.post("/login")
def login_user(request: Request, user: LoginDTO):
    try:
        return login_service(user, request.client.host)
    except Exception as e:
        return {"message": "error thrown from login service"}

@router.post("/change-password-after-verification")
def change_password_service_after_verification(user: ChangePasswordAVDTO):
    try:
        return change_password_service_after_verification_service(user)
    except Exception as e:
        return {"message": "error thrown from change password service"}

@router.post("/forgot-password")
def forgot_password(user: ForgotPasswordDTO):
    return forgot_password_service(user)


@router.get("/change-password")
def change_password():
    return {"message": "change password route"}


@router.post("/change-password")
def change_password_post(user: ChangePasswordDTO):
    try:
        return change_password_service(user)
    except Exception as e:
        return {"message": "error thrown from change password service"}

@router.delete("/delete-package/{customer_name:path}")
def delete_package(customer_name: str):
    return delete_package_service(customer_name)

@router.delete("/delete-all-customers")
def delete_all_customers():
    return delete_all_customers_service()

@router.post("/create-customer")
def create_customer(customer: CreateCustomerDTO):
    return create_customer_service(customer.package_id, customer.customer_name)

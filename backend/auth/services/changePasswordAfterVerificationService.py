from auth.dtos.dtos import ChangePasswordAVDTO
from auth.services.passwordBlacklist import is_blacklisted
from database.connection import connection, cursor


def change_password_service_after_verification_service(user: ChangePasswordAVDTO):
    if is_blacklisted(user.new_password):
        return {"message": "Password is too common, please choose a stronger one."}

    try:
        cursor.execute(
            f"""
            update users
            set password = ?
            where username = ?
            """
        , (user.new_password, user.username))
        connection.commit()

        return {"message": "Password changed successfully"}

    except Exception as e:
        return {
            "message": "Change password failed",
            "error": str(e)
        }
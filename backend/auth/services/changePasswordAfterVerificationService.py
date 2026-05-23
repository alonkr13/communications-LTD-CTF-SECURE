from auth.dtos.dtos import ChangePasswordAVDTO
from database.connection import connection, cursor


def change_password_service_after_verification_service(user: ChangePasswordAVDTO):
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
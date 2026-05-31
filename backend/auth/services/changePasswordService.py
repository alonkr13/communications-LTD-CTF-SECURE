from auth.dtos.dtos import ChangePasswordDTO
from auth.services.passwordBlacklist import is_blacklisted
from database.connection import connection, cursor


def change_password_service(user: ChangePasswordDTO):
    if is_blacklisted(user.new_password):
        return {"message": "Password is too common, please choose a stronger one."}

    try:
        cursor.execute(
            """
            select username, password FROM users WHERE username = ?
            """,
            (user.username,)
        )
        existing_user = cursor.fetchone()

        if existing_user == None:
            raise Exception("Username does not exist")

        if existing_user[1] != user.current_password:
            raise Exception("Current password is incorrect")

    except Exception as e:
        return {"message": str(e)}

    try:
        cursor.execute(
            """
            update users
            set password = ?
            where username = ?
            """,
            (user.new_password, user.username)
        )
        connection.commit()

        return {"message": "Password changed successfully"}

    except Exception as e:
        return {
            "message": "Change password failed",
            "error": str(e)
        }
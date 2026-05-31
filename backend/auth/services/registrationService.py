from fastapi import HTTPException, status
import sqlite3
from auth.dtos.dtos import RegisterDTO
from auth.services.passwordBlacklist import is_blacklisted
from database.connection import connection, cursor

def registration_service(user: RegisterDTO):
    if is_blacklisted(user.password):
        return {"message": "Password is too common, please choose a stronger one."}

    try:
        cursor.execute(
            """
            INSERT INTO users (username, email, password)
            VALUES (?, ?, ?)
            """,
            (user.username, user.email, user.password)
        )
        
        connection.commit()

        return {
            "status_code": status.HTTP_201_CREATED,
            "message": "User registered successfully",
            "user": {
                "username": user.username,
                "email": user.email
            }
        }
    
    except sqlite3.IntegrityError as e:
        return {"message": f"Integrity error: {str(e)}"}

     
    except Exception as e:
        return {
            "message": "Registration failed",
            "error": str(e)
        }
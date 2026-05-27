import sqlite3
from datetime import datetime, timedelta
from auth.dtos.dtos import LoginDTO
from database.connection import connection, cursor
from sendEmail import send_verification_email
MAX_ATTEMPTS = 5
LOCKOUT_MINUTES = 15

def login_service(user: LoginDTO, ip: str):

    # --- rate limit check ---
    cursor.execute("SELECT failed_count, last_failed FROM login_attempts WHERE ip = ?", (ip,))
    attempt_row = cursor.fetchone()

    if attempt_row:
        failed_count, last_failed_str = attempt_row
        last_failed = datetime.fromisoformat(last_failed_str)
        if failed_count >= 3:
            userEmail = cursor.execute(
                """
                SELECT email FROM users WHERE username = ?
                """
            )(user.username)
            send_verification_email(userEmail)

        if failed_count >= MAX_ATTEMPTS and datetime.now() - last_failed < timedelta(minutes=LOCKOUT_MINUTES):
            remaining = LOCKOUT_MINUTES - int((datetime.now() - last_failed).total_seconds() // 60)
            return {"message": f"Too many failed attempts. Try again in {remaining} minute(s)."}

    try:
        cursor.execute(
            """
            SELECT username, password FROM users WHERE username = ? AND password = ?
            """
        , (user.username, user.password))

        existing_user = cursor.fetchone()

        if existing_user is None:
            # increment failed attempts
            cursor.execute("""
                INSERT INTO login_attempts (ip, failed_count, last_failed)
                VALUES (?, 1, ?)
                ON CONFLICT(ip) DO UPDATE SET
                    failed_count = failed_count + 1,
                    last_failed  = excluded.last_failed
            """, (ip, datetime.now().isoformat()))
            connection.commit()
            raise Exception("Wrong username or password")

    except Exception as e:
        return {
            "message": str(e)
        }

    # login succeeded — clear any previous failed attempts for this IP
    cursor.execute("DELETE FROM login_attempts WHERE ip = ?", (ip,))
    connection.commit()

    try:
        cursor.execute("""
        SELECT id, package_name, download_speed, upload_speed, monthly_price FROM packages
                       """)

        existing_packages = cursor.fetchall()

        cursor.execute("""
            SELECT package_id, customer_name FROM customers
                       """)

        existing_customers = cursor.fetchall()

        if existing_customers == False:

            raise Exception("no customers to display")

        return {
                "message": "Login successful",
                "username": existing_user[0],
                "data": {
                    "packages": existing_packages,
                    "customers": existing_customers
                }
            }


    except Exception as e:
        return {
            "message": "Login Failed",
            "error": str(e)
        }

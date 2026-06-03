import sqlite3
from datetime import datetime, timedelta
from auth.dtos.dtos import LoginDTO
from database.connection import connection, cursor
from auth.services.sendEmail import send_verification_email,check_if_code_exists,verify_code

MAX_ATTEMPTS = 5
LOCKOUT_MINUTES = 15
def login_service(user: LoginDTO, ip: str):

    # --- rate limit check ---
    cursor.execute("SELECT failed_count, last_failed FROM login_attempts WHERE ip = ?", (ip,))
    attempt_row = cursor.fetchone()
    if attempt_row:
        failed_count, last_failed_str = attempt_row
        last_failed = datetime.fromisoformat(last_failed_str)
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
            increaseLoginFailes(ip,user)
            connection.commit()
            cursor.execute("SELECT failed_count, last_failed,user_name FROM login_attempts WHERE ip = ?", (ip,))
            failed_attemps = cursor.fetchone()

            if failed_attemps[0] == 3:
                    cursor.execute(
                    """
                    SELECT email FROM users WHERE username = ?
                    """,
                    (failed_attemps[2],))
                    userEmailFetch = cursor.fetchone()
                    if userEmailFetch != None:
                        userEmail = userEmailFetch[0]
                        if userEmailFetch:
                            send_verification_email(userEmail)
                            return {"message": "A Verification Code was sent to youre Email"}
                    else:
                        return {"message": "Wrong username or password"}
            else:
                return {"message": "Wrong username or password"}
        else:
            cursor.execute(
                    """
                    SELECT email FROM users WHERE username = ?
                    """,
                    (user.username,))
                    
            userEmailFetch = cursor.fetchone()
            userEmail = userEmailFetch[0]
            if check_if_code_exists(userEmail):
                if verify_code(userEmail,user.code):
                    return loginUser(ip,existing_user)
                else:
                    increaseLoginFailes(ip,user)
                    return {"message": "Wrong username,password or code"}
            else:
                #Check if the user didnt log in the last day or is loggin from a different ip
                cursor.execute(
                    """
                    SELECT last_logon_time,last_logon_ip,email FROM users WHERE username = ?
                    """,
                    (user.username,))
                userData = cursor.fetchone()
                yesterdayTime = datetime.now() - timedelta(days=1)
                if((userData[0] is None) or (userData[1] is None)):
                    send_verification_email(userData[2])
                    return {"message": "A Verification Code was sent to youre Email"}
                
                last_logon_time = datetime.fromisoformat(userData[0])

                if((last_logon_time < yesterdayTime) or (userData[1] != ip)):
                    send_verification_email(userEmail)
                    return {"message": "A Verification Code was sent to youre Email"}
                else:
                    return loginUser(ip,existing_user)

            
             
        
    except Exception as e:
        return {
            "message": str(e)
        }

def increaseLoginFailes(ip, user):
    cursor.execute("""
    INSERT INTO login_attempts (ip, failed_count, last_failed,user_name)
    VALUES (?, 1, ?, ?)
    ON CONFLICT(ip) DO UPDATE SET
    failed_count = failed_count + 1,
    last_failed  = excluded.last_failed
    """, (ip, datetime.now().isoformat(),user.username))
    connection.commit()

def loginUser(ip,existing_user):
    # login succeeded — clear any previous failed attempts for this IP
    cursor.execute("DELETE FROM login_attempts WHERE ip = ?", (ip,))
    connection.commit()

    cursor.execute(
            """
            UPDATE users SET last_logon_ip =?, last_logon_time=?
            WHERE username=?
            """,
            (ip, datetime.now().isoformat(),existing_user[0]))
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

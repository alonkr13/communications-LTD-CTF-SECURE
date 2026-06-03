import sqlite3
import hmac
from auth.dtos.dtos import ForgotPasswordDTO
from database.connection import cursor
import hashlib
import smtplib
from email.message import EmailMessage
import string
import secrets

hash_dic = {}
SECRET_KEY = "COMM_LTD_CTF"
def forgot_password_service(user: ForgotPasswordDTO):
    if user.email in hash_dic:
            if (verify_code(user.email,user.code)):
                return {
                    "message": "Password reset successful"
                }
            else:
                return {
                    "message": "Invalid code"
                }
    else:
        return reset_password(user)


def reset_password(user: ForgotPasswordDTO):
    
        try:
            cursor.execute(
                """
                select email FROM users WHERE email = ?
                """,
                (user.email,)
            )

            existing_user = cursor.fetchone()
            
            if existing_user:
                send_email(existing_user[0], f"One time code for changing password: {code_hash(user.email)}")
                return {
                    "message": "Password reset link sent to email" 
                }
            else:
                return {
                    "message": "Invalid email"
                }


        except Exception as e:
            return {
                "message": "Password reset failed",
                "error": str(e)
            }

def verify_code(email, code):
    if email not in hash_dic or code is None:
        return False
    
    hashed_code = hmac.new(
        SECRET_KEY.encode(),
        code.encode(),
        hashlib.sha1
    ).hexdigest()

    if hmac.compare_digest(hash_dic[email], hashed_code):
        del hash_dic[email]
        return True
    return False

def code_hash(email):
    digits = string.digits
    code = ''.join(secrets.choice(digits) for _ in range(6))
    hash_dic[email] = hmac.new(
        SECRET_KEY.encode(),
        code.encode(),
        hashlib.sha1
    ).hexdigest()
    return code 

def send_email(to_email, body):
    SENDER_EMAIL = "ltdcommrp@gmail.com"
    SENDER_PASSWORD = "nksr dbog ewcj pzwa"
    RECIPIENT_EMAIL = to_email

    msg = EmailMessage()
    msg["Subject"] = "Reset Password"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECIPIENT_EMAIL
    msg.set_content(body)

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")
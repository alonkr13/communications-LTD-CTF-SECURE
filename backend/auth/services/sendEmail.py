import hmac
import hashlib
import smtplib
from email.message import EmailMessage
import string
import secrets

hash_dic = {}
SECRET_KEY = "COMM_LTD_CTF"

def check_if_code_exists(email):
    if email in hash_dic:
        return True
    else:
        return False

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
    msg["Subject"] = "Verification Code"
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


def send_verification_email(userEmail):
    code = code_hash(userEmail)
    bodyForMail = f"Verification Code is  {code}"
    send_email(userEmail,bodyForMail)
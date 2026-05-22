import sqlite3
from auth.dtos.dtos import LoginDTO
from database.connection import connection, cursor

def login_service(user: LoginDTO):


    try:
        cursor.execute(
            f"""
            select username, password FROM users WHERE username = '{user.username}' AND password = '{user.password}'
            """
        )

        existing_user = cursor.fetchone()
        
        if existing_user == None:

            raise Exception("Wrong username or password")

    except Exception as e:
        return {
            "message": str(e)
        }

    try:
        cursor.execute(f"""
        select id, package_name, download_speed, upload_speed, monthly_price from packages
                       """)
        
        existing_packages = cursor.fetchall()
        
        cursor.execute(f"""
            select package_id, customer_name from customers
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
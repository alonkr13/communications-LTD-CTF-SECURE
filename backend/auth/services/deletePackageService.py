from database.connection import connection, cursor

def delete_package_service(customer_name: str):
    try:
        cursor.execute(
            f"""
            DELETE FROM customers WHERE customer_name = '{customer_name}'
            """
        )
        connection.commit()

        if cursor.rowcount == 0:
            raise Exception("Customer not found")

        return {
            "message": "Customer deleted successfully",
            "customer_name": customer_name
        }
    except Exception as e:
        return {
            "message": str(e)
        }

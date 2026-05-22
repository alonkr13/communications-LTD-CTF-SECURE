from database.connection import connection, cursor

def create_customer_service(package_id: int, customer_name: str):
    try:
        cursor.execute(
            f"""
            SELECT id FROM packages WHERE id = {package_id}
            """
        )
        package = cursor.fetchone()

        if package is None:
            raise Exception("Package ID does not exist")

        cursor.execute(
            f"""
            INSERT INTO customers (package_id, customer_name)
            VALUES ({package_id}, '{customer_name}')
            """
        )
        connection.commit()

        return {
            "message": "Customer created successfully",
            "package_id": package_id,
            "customer_name": customer_name
        }
    except Exception as e:
        return {
            "message": str(e)
        }
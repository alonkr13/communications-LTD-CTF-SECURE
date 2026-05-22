from database.connection import connection, cursor


def delete_all_customers_service():
    try:
        cursor.execute(
            """
            DELETE FROM customers
            """
        )
        deleted_count = cursor.rowcount
        connection.commit()

        return {
            "message": "All customers deleted successfully",
            "deleted_count": deleted_count
        }
    except Exception as e:
        return {
            "message": str(e)
        }

import mysql.connector

def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Ps27@6086",
        database="smart_saving_system"
    )
    return conn

if __name__ == "__main__":
    conn = get_db_connection()
    print("Database connected successfully")
    conn.close()
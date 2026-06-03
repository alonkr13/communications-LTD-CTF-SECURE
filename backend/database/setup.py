from database.connection import connection, cursor

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    last_logon_time TEXT,
    last_logon_ip TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS packages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    package_name TEXT NOT NULL UNIQUE,
    download_speed INTEGER NOT NULL,
    upload_speed INTEGER NOT NULL,
    monthly_price REAL NOT NULL
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    package_id INTEGER NOT NULL, 
    FOREIGN KEY (package_id) REFERENCES packages(id)
)
""")


cursor.execute("""
INSERT or ignore INTO packages (id, package_name, download_speed, upload_speed, monthly_price)
VALUES
    (1,'Starter 100', 100, 20, 79.90),
    (2, 'Home 300', 300, 50, 109.90),
    (3, 'Business 600', 600, 100, 159.90),
    (4, 'Fiber Pro 1000', 1000, 250, 219.90)
               """)


cursor.execute("""
INSERT or ignore INTO customers (package_id, customer_name)
VALUES
    (2, 'Pizza America'),
    (3, 'Southern Garage Ltd'),
    (1, 'Blue Market Cafe'),
    (4, 'TechVision Office'), 
    (4, 'KSP'),
    (3, 'Ivory')
               """)


cursor.execute("""
CREATE TABLE IF NOT EXISTS login_attempts (
    ip          TEXT PRIMARY KEY,
    failed_count INTEGER DEFAULT 0,
    user_name TEXT,
    last_failed  TEXT
)
""")

connection.commit()

import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",   
    database="banking_database"    
)
cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS Banking_Database")


# --- Create accounts table ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS accounts (
    account_id VARCHAR(10) PRIMARY KEY,   -- e.g. "A1", "B2"
    account_number VARCHAR(50) NOT NULL,
    firstname VARCHAR(100),
    surname VARCHAR(100),
    telephoneno VARCHAR(20),
    email VARCHAR(100),
    balance DECIMAL(12,2) NOT NULL DEFAULT 0.00
)
""")

# --- Create addresses table ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS addresses (
    address_id INT AUTO_INCREMENT PRIMARY KEY,
    account_id VARCHAR(10) NOT NULL,
    street_number VARCHAR(20),
    street_name VARCHAR(100),
    city VARCHAR(100),
    postcode VARCHAR(20),
    country VARCHAR(100),
    FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE CASCADE
)
""")

conn.commit()
conn.close()
print("Database tables created successfully.")
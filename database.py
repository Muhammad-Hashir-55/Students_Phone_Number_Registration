import psycopg2
import os
from dotenv import load_dotenv
import streamlit as st
from psycopg2 import OperationalError

load_dotenv()

def get_connection():
    """Create connection to PostgreSQL database with error handling"""
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            database=os.getenv("DB_NAME", "student_phones"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", ""),
            port=os.getenv("DB_PORT", "5432"),
            connect_timeout=5  # Add timeout
        )
        return conn
    except OperationalError as e:
        st.error(f"Database connection failed: {e}")
        # Fallback to SQLite if PostgreSQL is not available
        import sqlite3
        return sqlite3.connect('students.db')

def create_table():
    """Create students table if it doesn't exist"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        # Check if we're using PostgreSQL or SQLite
        is_postgres = isinstance(conn, psycopg2.extensions.connection)
        
        if is_postgres:
            # Create table for PostgreSQL
            cur.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    reg_number VARCHAR(20) UNIQUE NOT NULL,
                    phone_number VARCHAR(20),
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        else:
            # Create table for SQLite
            cur.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    reg_number TEXT UNIQUE NOT NULL,
                    phone_number TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        
        # Check if table is empty
        cur.execute("SELECT COUNT(*) FROM students")
        count = cur.fetchone()[0]
        
        if count == 0:
            students = [
                ("Arsalan Khalil", "2023130"),
                ("Hamza Mukhtar", "2023682"),
                ("Abdul Raffay bin Ilyas", "2023021"),
                ("Muhammad", "2023339"),
                ("Muhammad Usman Nazir", "2023546"),
                ("Muhammad Hamza khan", "2023425"),
                ("Abdul Ahad Ali Khan", "2023004"),
                ("Muhammad Umer Farooq", "2023540"),
                ("Riyan khan Durrani", "2023611"),
                ("Hamza Saeed", "2023903"),
                ("Muhammad Umar", "2023535"),
                ("Zain", "2023773"),
                ("Hashir", "2023429"),
                ("Bushrah Zulfiqar", "2023165"),
                ("Syeda Masooma Shah", "2023705"),
                ("Warisha Arshad", "2023757"),
                ("Rameen Zia", "2023594"),
                ("Shumaz saeed", "2023662"),
                ("Nishat Ahmed", "2023574"),
                ("Muhammad Rohaan Mirza", "2023495"),
                ("Ahmad Saeed Zaidi", "2023073"),
                ("Saad Khurshid", "2023622")
            ]
            
            for name, reg in students:
                try:
                    if is_postgres:
                        cur.execute(
                            "INSERT INTO students (name, reg_number) VALUES (%s, %s) ON CONFLICT (reg_number) DO NOTHING",
                            (name, reg)
                        )
                    else:
                        cur.execute(
                            "INSERT OR IGNORE INTO students (name, reg_number) VALUES (?, ?)",
                            (name, reg)
                        )
                except:
                    pass
        
        conn.commit()
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"Error creating table: {e}")

# Rest of the functions remain the same...
def get_student_by_reg(reg_number):
    """Get student by registration number"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        # Check if we're using PostgreSQL or SQLite
        is_postgres = isinstance(conn, psycopg2.extensions.connection)
        
        if is_postgres:
            cur.execute("SELECT * FROM students WHERE reg_number = %s", (reg_number,))
        else:
            cur.execute("SELECT * FROM students WHERE reg_number = ?", (reg_number,))
            
        student = cur.fetchone()
        cur.close()
        conn.close()
        return student
    except Exception as e:
        print(f"Error getting student: {e}")
        return None

def update_phone_number(reg_number, phone_number):
    """Update phone number for a student"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        # Check if we're using PostgreSQL or SQLite
        is_postgres = isinstance(conn, psycopg2.extensions.connection)
        
        if is_postgres:
            cur.execute(
                "UPDATE students SET phone_number = %s, updated_at = CURRENT_TIMESTAMP WHERE reg_number = %s",
                (phone_number, reg_number)
            )
        else:
            cur.execute(
                "UPDATE students SET phone_number = ?, updated_at = CURRENT_TIMESTAMP WHERE reg_number = ?",
                (phone_number, reg_number)
            )
            
        conn.commit()
        rows_affected = cur.rowcount
        cur.close()
        conn.close()
        return rows_affected > 0
    except Exception as e:
        print(f"Error updating phone number: {e}")
        return False

def get_all_students():
    """Get all students with their phone numbers"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        # Check if we're using PostgreSQL or SQLite
        is_postgres = isinstance(conn, psycopg2.extensions.connection)
        
        if is_postgres:
            cur.execute("""
                SELECT name, reg_number, phone_number, 
                       CASE WHEN phone_number IS NOT NULL THEN '✅ Submitted' ELSE '❌ Pending' END as status
                FROM students 
                ORDER BY name
            """)
        else:
            cur.execute("""
                SELECT name, reg_number, phone_number, 
                       CASE WHEN phone_number IS NOT NULL THEN '✅ Submitted' ELSE '❌ Pending' END as status
                FROM students 
                ORDER BY name
            """)
            
        students = cur.fetchall()
        cur.close()
        conn.close()
        return students
    except Exception as e:
        print(f"Error getting all students: {e}")
        return []
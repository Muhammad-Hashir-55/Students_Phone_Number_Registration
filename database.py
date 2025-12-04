import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    """Create connection to PostgreSQL database"""
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "student_phones"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "password"),
        port=os.getenv("DB_PORT", "5432")
    )

def create_table():
    """Create students table if it doesn't exist"""
    conn = get_connection()
    cur = conn.cursor()
    
    # Create table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            reg_number VARCHAR(20) UNIQUE NOT NULL,
            phone_number VARCHAR(20),
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Insert initial student data if table is empty
    cur.execute("SELECT COUNT(*) FROM students")
    if cur.fetchone()[0] == 0:
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
            cur.execute(
                "INSERT INTO students (name, reg_number) VALUES (%s, %s) ON CONFLICT (reg_number) DO NOTHING",
                (name, reg)
            )
    
    conn.commit()
    cur.close()
    conn.close()

def get_student_by_reg(reg_number):
    """Get student by registration number"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students WHERE reg_number = %s", (reg_number,))
    student = cur.fetchone()
    cur.close()
    conn.close()
    return student

def update_phone_number(reg_number, phone_number):
    """Update phone number for a student"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE students SET phone_number = %s, updated_at = CURRENT_TIMESTAMP WHERE reg_number = %s",
        (phone_number, reg_number)
    )
    conn.commit()
    rows_affected = cur.rowcount
    cur.close()
    conn.close()
    return rows_affected > 0

def get_all_students():
    """Get all students with their phone numbers"""
    conn = get_connection()
    cur = conn.cursor()
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
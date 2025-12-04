import sqlite3
import os
from datetime import datetime

def get_connection():
    """Create connection to SQLite database"""
    conn = sqlite3.connect('students.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    """Create students table. Returns (Success, ErrorMessage)"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        # Create table with UNIQUE constraint
        cur.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                reg_number TEXT UNIQUE NOT NULL,
                phone_number TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Check if we need to seed data
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
                    cur.execute("INSERT OR IGNORE INTO students (name, reg_number) VALUES (?, ?)", (name, reg))
                except:
                    pass
        
        conn.commit()
        cur.close()
        conn.close()
        return True, None # Success
        
    except Exception as e:
        return False, str(e) # Failure with error message

def get_student_by_reg(reg_number):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM students WHERE reg_number = ?", (reg_number,))
        student = cur.fetchone()
        cur.close()
        conn.close()
        return tuple(student) if student else None
    except:
        return None

def check_phone_exists(phone_number):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT name, reg_number FROM students WHERE phone_number = ?", (phone_number,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result if result else None
    except:
        return None

def update_phone_number(reg_number, phone_number):
    try:
        conn = get_connection()
        cur = conn.cursor()
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cur.execute("UPDATE students SET phone_number = ?, updated_at = ? WHERE reg_number = ?", 
                   (phone_number, current_time, reg_number))
        conn.commit()
        success = cur.rowcount > 0
        cur.close()
        conn.close()
        return success
    except:
        return False

def get_all_students():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT name, reg_number, phone_number FROM students ORDER BY name")
        students = []
        for row in cur.fetchall():
            status = '✅ Submitted' if row[2] else '❌ Pending'
            students.append((row[0], row[1], row[2], status))
        cur.close()
        conn.close()
        return students
    except:
        return []
import sqlite3
import os
from datetime import datetime

def get_connection():
    """Create connection to SQLite database"""
    # Use a local SQLite database file
    return sqlite3.connect('students.db', check_same_thread=False)

def create_table():
    """Create students table if it doesn't exist"""
    conn = get_connection()
    cur = conn.cursor()
    
    # Create table with SQLite syntax
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            reg_number TEXT UNIQUE NOT NULL,
            phone_number TEXT,
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
                "INSERT OR IGNORE INTO students (name, reg_number) VALUES (?, ?)",
                (name, reg)
            )
    
    conn.commit()
    cur.close()
    conn.close()

def get_student_by_reg(reg_number):
    """Get student by registration number"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students WHERE reg_number = ?", (reg_number,))
    student = cur.fetchone()
    cur.close()
    conn.close()
    return student

def update_phone_number(reg_number, phone_number):
    """Update phone number for a student"""
    conn = get_connection()
    cur = conn.cursor()
    
    # Update with current timestamp
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cur.execute(
        "UPDATE students SET phone_number = ?, updated_at = ? WHERE reg_number = ?",
        (phone_number, current_time, reg_number)
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
    
    # SQLite doesn't support CASE in the same way, so we'll process it in Python
    cur.execute("""
        SELECT name, reg_number, phone_number, updated_at
        FROM students 
        ORDER BY name
    """)
    
    students_raw = cur.fetchall()
    
    # Process the results to add status
    students = []
    for name, reg, phone, updated_at in students_raw:
        if phone:
            status = '✅ Submitted'
        else:
            status = '❌ Pending'
        students.append((name, reg, phone, status))
    
    cur.close()
    conn.close()
    return students

# Optional: Function to get database statistics
def get_stats():
    """Get database statistics"""
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT COUNT(*) FROM students")
    total = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM students WHERE phone_number IS NOT NULL")
    submitted = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM students WHERE phone_number IS NULL")
    pending = cur.fetchone()[0]
    
    cur.execute("SELECT MAX(updated_at) FROM students WHERE phone_number IS NOT NULL")
    last_update = cur.fetchone()[0]
    
    cur.close()
    conn.close()
    
    return {
        'total': total,
        'submitted': submitted,
        'pending': pending,
        'last_update': last_update
    }

# Optional: Function to reset a student's phone number (for admin use)
def reset_phone_number(reg_number):
    """Reset phone number for a student"""
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute(
        "UPDATE students SET phone_number = NULL, updated_at = CURRENT_TIMESTAMP WHERE reg_number = ?",
        (reg_number,)
    )
    
    conn.commit()
    rows_affected = cur.rowcount
    cur.close()
    conn.close()
    return rows_affected > 0

# Optional: Function to export data to CSV
def export_to_csv():
    """Export all student data to CSV format"""
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT name, reg_number, phone_number, updated_at
        FROM students 
        ORDER BY name
    """)
    
    students = cur.fetchall()
    cur.close()
    conn.close()
    
    # Create CSV content
    csv_content = "Name,Registration Number,Phone Number,Last Updated\n"
    for name, reg, phone, updated_at in students:
        phone_display = phone if phone else "Not submitted"
        updated_display = updated_at if updated_at else "Never"
        csv_content += f'"{name}","{reg}","{phone_display}","{updated_display}"\n'
    
    return csv_content
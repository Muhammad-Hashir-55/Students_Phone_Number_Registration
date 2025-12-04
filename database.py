import sqlite3
from datetime import datetime

def get_connection():
    """Create connection to SQLite database"""
    conn = sqlite3.connect('students.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn

def create_table():
    """Create students table if it doesn't exist"""
    conn = get_connection()
    cur = conn.cursor()
    
    # Create table
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
                cur.execute(
                    "INSERT OR IGNORE INTO students (name, reg_number) VALUES (?, ?)",
                    (name, reg)
                )
            except:
                pass
    
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
    
    if student:
        # Convert to tuple for compatibility
        return tuple(student)
    return None

def update_phone_number(reg_number, phone_number):
    """Update phone number for a student"""
    conn = get_connection()
    cur = conn.cursor()
    
    # Get current timestamp
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
    
    cur.execute("""
        SELECT name, reg_number, phone_number 
        FROM students 
        ORDER BY name
    """)
    
    students_raw = cur.fetchall()
    students = []
    
    for row in students_raw:
        name = row[0]
        reg = row[1]
        phone = row[2]
        status = '✅ Submitted' if phone else '❌ Pending'
        students.append((name, reg, phone, status))
    
    cur.close()
    conn.close()
    return students

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


def check_phone_exists(phone_number):
    """Check if phone number already exists for ANY student"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name FROM students WHERE phone_number = ?", (phone_number,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result[0] if result else None
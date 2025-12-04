import streamlit as st
import database
import re
import time
import pandas as pd
import os

# 1. PAGE CONFIG
st.set_page_config(
    page_title="Student Phone Number Registration",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. FILE WATCHER FIX
os.environ['STREAMLIT_SERVER_FILE_WATCHER_TYPE'] = 'none'

# 3. DATABASE INITIALIZATION & SELF-HEALING
success, error_msg = database.create_table()

if not success:
    warning_placeholder = st.empty()
    warning_placeholder.warning(f"⚠️ Database Error: {error_msg}. Attempting Auto-Fix...")
    
    if os.path.exists('students.db'):
        try:
            os.remove('students.db')
            time.sleep(1)
            retry_success, retry_msg = database.create_table()
            if retry_success:
                warning_placeholder.success("✅ Database repaired! Please refresh page.")
                time.sleep(1)
                st.rerun()
            else:
                st.error(f"❌ Critical Error: Could not repair database. {retry_msg}")
                st.stop()
        except Exception as e:
            st.error(f"❌ Permission Error: {e}")
            st.stop()

# 4. CSS STYLES
st.markdown("""
<style>
    .main-header {
        text-align: center; color: white; padding: 1.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px; margin-bottom: 2rem;
    }
    .success-box {
        background: #d4edda; padding: 1.5rem; border-radius: 10px; 
        border-left: 6px solid #28a745; margin: 1rem 0;
    }
    .student-card {
        background: white; padding: 1rem; border-radius: 10px;
        border: 1px solid #ddd; margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .submitted { border-left: 5px solid #28a745; }
    .pending { border-left: 5px solid #dc3545; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

# 5. HEADER
st.markdown("""
<div class="main-header">
    <h1>📱 Student Phone Registration</h1>
    <p>Department of Electrical Engineering</p>
</div>
""", unsafe_allow_html=True)

# 6. SIDEBAR
with st.sidebar:
    st.header("🔍 Find Student")
    reg_input = st.text_input("Enter Reg Number:", placeholder="2023130")
    if reg_input:
        student = database.get_student_by_reg(reg_input.strip())
        if student:
            st.success("Student Found!") if student[3] else st.warning("Student Found (No Phone)")
            st.write(f"**Name:** {student[1]}")
            st.write(f"**Phone:** {student[3] if student[3] else 'Not Submitted'}")
        else:
            st.error("Not found.")

# 7. MAIN FORM
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Submit Number")
    with st.form("entry"):
        reg_num = st.text_input("Registration Number", placeholder="2023XXX", max_chars=7)
        phone_num = st.text_input("Phone Number", placeholder="03XXXXXXXXX", max_chars=11)
        submitted = st.form_submit_button("Submit / Update")
        
        if submitted:
            if not reg_num or not phone_num:
                st.error("Please fill all fields")
            elif not re.match(r'^\d{7}$', reg_num):
                st.error("Invalid Reg Number (Must be 7 digits)")
            elif not re.match(r'^03\d{9}$', phone_num):
                st.error("Invalid Phone (Format: 03XXXXXXXXX)")
            else:
                # DUPLICATE CHECK
                reg_clean = reg_num.strip()
                phone_clean = phone_num.strip()
                
                owner = database.check_phone_exists(phone_clean)
                student = database.get_student_by_reg(reg_clean)
                
                if not student:
                    st.error("Student not found in class list")
                elif owner and owner[1] != reg_clean:
                    st.error(f"❌ This number is already used by {owner[0]}!")
                else:
                    if database.update_phone_number(reg_clean, phone_clean):
                        st.balloons()
                        st.markdown(f"""
                        <div class="success-box">
                            <h4>✅ Success!</h4>
                            <p>Saved for: <strong>{student[1]}</strong></p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error("Database error")

with col2:
    st.subheader("📊 Progress")
    students = database.get_all_students()
    total = 22
    done = sum(1 for s in students if s[2])
    
    st.metric("Submitted", f"{done} / {total}")
    st.progress(done/total)
    st.info("Note: You cannot use a phone number already registered to another student.")

# 8. DIRECTORY & DOWNLOAD
st.markdown("---")
st.subheader("👥 Directory")

# Search and Download Columns
search_col, download_col = st.columns([3, 1])

with search_col:
    search = st.text_input("Filter Directory:", placeholder="Search name...")

with download_col:
    # CSV DOWNLOAD LOGIC
    if students:
        df = pd.DataFrame(students, columns=['Name', 'Registration No', 'Phone Number', 'Status'])
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name='student_records.csv',
            mime='text/csv',
            use_container_width=True
        )

# Grid Layout
cols = st.columns(3)
filtered = [s for s in students if search.lower() in s[0].lower() or search in s[1]]

for i, s in enumerate(filtered):
    with cols[i%3]:
        status = "submitted" if s[2] else "pending"
        icon = "✅" if s[2] else "⏳"
        st.markdown(f"""
        <div class="student-card {status}">
            <b>{icon} {s[0]}</b><br>
            <span style="color:grey">{s[1]}</span><br>
            <span style="color:{'green' if s[2] else 'red'}">{s[2] if s[2] else 'Pending'}</span>
        </div>
        """, unsafe_allow_html=True)


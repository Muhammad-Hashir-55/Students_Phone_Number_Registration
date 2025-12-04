import streamlit as st
import database
import re
import time
import pandas as pd
import os
# Fix for inotify watch limit
os.environ['STREAMLIT_SERVER_FILE_WATCHER_TYPE'] = 'none'
# Page configuration
st.set_page_config(
    page_title="Student Phone Number Registration",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
database.create_table()

# Custom CSS with enhanced color scheme
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        color: #2c3e50;
        padding: 1.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.2);
    }
    
    /* Success box */
    .success-box {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 6px solid #28a745;
        margin: 1.5rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        animation: fadeIn 0.5s ease-in;
    }
    
    /* Info box */
    .info-box {
        background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 6px solid #17a2b8;
        margin: 1.5rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Warning box */
    .warning-box {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 6px solid #ffc107;
        margin: 1.5rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Student cards */
    .student-card {
        background: white;
        padding: 1.2rem;
        border-radius: 12px;
        border: 2px solid #e9ecef;
        margin: 0.8rem 0;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .student-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        border-color: #667eea;
    }
    
    .student-card.submitted {
        border-color: #28a745;
        background: linear-gradient(135deg, #f8fff9 0%, #e8f7ec 100%);
    }
    
    .student-card.pending {
        border-color: #dc3545;
        background: linear-gradient(135deg, #fff9f9 0%, #ffeaea 100%);
    }
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .submitted-badge {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
    }
    
    .pending-badge {
        background: linear-gradient(135deg, #dc3545 0%, #fd7e14 100%);
        color: white;
    }
    
    /* Form styling */
    .stTextInput>div>div>input {
        border-radius: 8px;
        border: 2px solid #dee2e6;
        padding: 0.75rem;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(102, 126, 234, 0.3);
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #28a745 0%, #20c997 100%);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Section headers */
    .section-header {
        color: #2c3e50;
        border-bottom: 3px solid #667eea;
        padding-bottom: 0.5rem;
        margin-bottom: 1.5rem;
        display: inline-block;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #6c757d;
        padding: 1.5rem;
        margin-top: 2rem;
        border-top: 2px solid #e9ecef;
        background: #f8f9fa;
        border-radius: 10px;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .pulse-animation {
        animation: pulse 2s infinite;
    }
    
    /* Stats card */
    .stats-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        text-align: center;
        border-top: 5px solid #667eea;
    }
    
    .stats-number {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0.5rem 0;
    }
    
    /* Grid layout for student cards */
    .student-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 1rem;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Header with enhanced design
st.markdown("""
<div class="main-header">
    <h1 style="margin:0; font-size: 2.5rem;">📱 Student Phone Number Registration</h1>
    <p style="margin:0.5rem 0 0 0; opacity: 0.9;">Department of Electrical Engineering - Batch 2023</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Sidebar with enhanced design
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2 style="color: #2c3e50;">🔍 Student Lookup</h2>
    </div>
    """, unsafe_allow_html=True)
    
    reg_input = st.text_input("**Enter Registration Number:**", placeholder="e.g., 2023130", key="lookup")
    
    if reg_input:
        with st.spinner("Looking up student..."):
            time.sleep(0.5)  # Simulate loading
            student = database.get_student_by_reg(reg_input.strip())
            if student:
                st.markdown(f"""
                <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <h4 style="color: #2c3e50; margin-bottom: 1rem;">Student Details</h4>
                    <p><strong>👤 Name:</strong> {student[1]}</p>
                    <p><strong>🎯 Reg No:</strong> <code>{student[2]}</code></p>
                """, unsafe_allow_html=True)
                
                if student[3]:
                    st.markdown(f"""
                    <p><strong>📱 Phone:</strong> <span style="color: #28a745; font-weight: bold;">{student[3]}</span></p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.success("✅ Phone number submitted")
                else:
                    st.markdown("""
                    <p><strong>📱 Phone:</strong> <span style="color: #dc3545; font-weight: bold;">Not submitted</span></p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.warning("❌ Phone number not submitted yet")
            else:
                st.error("🚫 Student not found in database")

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<h3 class="section-header">📝 Submit / Update Phone Number</h3>', unsafe_allow_html=True)
    
    with st.form("phone_form", clear_on_submit=True):
        reg_number = st.text_input("**Registration Number***", 
                                 placeholder="Enter your 7-digit registration number",
                                 help="Must be exactly 7 digits")
        
        phone_number = st.text_input("**Phone Number***", 
                                   placeholder="03XXXXXXXXX",
                                   help="Format: 03XXXXXXXXX (11 digits total)")
        
        submitted = st.form_submit_button("📤 Submit / Update", use_container_width=True)
        
        if submitted:
            if not reg_number or not phone_number:
                st.error("⚠️ Please fill in all required fields")
            else:
                # Validate registration number (7 digits)
                if not re.match(r'^\d{7}$', reg_number.strip()):
                    st.error("❌ Invalid registration number. Must be exactly 7 digits.")
                # Validate phone number
                elif not re.match(r'^03\d{9}$', phone_number.strip()):
                    st.error("❌ Invalid phone number. Must be in format 03XXXXXXXXX (11 digits)")
                else:
                    student = database.get_student_by_reg(reg_number.strip())
                    if student:
                        # Logic: We allow overwrite now. We check if it was already there just to change the message slightly if we wanted, 
                        # but "Saved/Updated" covers both cases.
                        
                        success = database.update_phone_number(reg_number.strip(), phone_number.strip())
                        
                        if success:
                            action_text = "Updated" if student[3] else "Submitted"
                            st.markdown(f"""
                            <div class="success-box">
                                <h4>🎉 Successfully {action_text}!</h4>
                                <p><strong>👤 Name:</strong> {student[1]}</p>
                                <p><strong>🎯 Registration No:</strong> {student[2]}</p>
                                <p><strong>📱 Phone Number:</strong> <span style="color: #28a745; font-weight: bold;">{phone_number.strip()}</span></p>
                                <p><em>Your record has been saved.</em></p>
                            </div>
                            """, unsafe_allow_html=True)
                            st.balloons()
                        else:
                            st.error("❌ Failed to update phone number. Please try again.")
                    else:
                        st.error("🚫 Registration number not found in our records")

with col2:
    st.markdown('<h3 class="section-header">ℹ️ Instructions</h3>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <h4 style="color: #17a2b8; margin-top: 0;">📋 How to submit:</h4>
        <ol style="color: #495057;">
            <li><strong>Enter your 7-digit registration number</strong> (e.g., 2023130)</li>
            <li><strong>Enter your phone number</strong> in format 03XXXXXXXXX (11 digits total)</li>
            <li><strong>Click "Submit / Update"</strong> button</li>
            <li><strong>Modifications:</strong> You can update your number by submitting the form again.</li>
        </ol>
        <div style="background: #f8f9fa; padding: 0.8rem; border-radius: 6px; margin-top: 1rem;">
            <p style="margin: 0; color: #6c757d;"><strong>Note:</strong> Total students fixed at 22</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Statistics card
    st.markdown('<h3 class="section-header">📊 Submission Statistics</h3>', unsafe_allow_html=True)
    
    students_data = database.get_all_students()
    total_students = 22
    submitted_count = sum(1 for s in students_data if s[2])  # Count with phone numbers
    pending_count = total_students - submitted_count
    
    col_stat1, col_stat2 = st.columns(2)
    
    with col_stat1:
        st.markdown(f"""
        <div class="stats-card">
            <h5 style="color: #28a745;">✅ Submitted</h5>
            <div class="stats-number">{submitted_count}</div>
            <p>Students</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_stat2:
        st.markdown(f"""
        <div class="stats-card">
            <h5 style="color: #dc3545;">⏳ Pending</h5>
            <div class="stats-number">{pending_count}</div>
            <p>Students</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Progress bar with percentage
    progress = submitted_count / total_students
    st.progress(progress)
    
    if progress == 1:
        st.success(f"🎉 **100% Complete!** All {total_students} students have submitted their numbers!")
    else:
        st.markdown(f"**Progress:** {submitted_count} of {total_students} students ({progress:.1%})")

# Display all students section
st.markdown("---")
st.markdown('<h3 class="section-header">👥 Student Directory</h3>', unsafe_allow_html=True)

# Get all students for display and download
students = database.get_all_students()

# Search, Filter, Refresh, and Download
search_col, filter_col, refresh_col, download_col = st.columns([2, 2, 0.6, 0.6])

with search_col:
    search_term = st.text_input("🔍 Search by name or registration:", placeholder="Type to search...")

with filter_col:
    filter_status = st.selectbox("Filter by status:", ["All", "Submitted", "Pending"])

with refresh_col:
    st.markdown("<br>", unsafe_allow_html=True) # Spacer
    if st.button("🔄 Refresh", use_container_width=True):
        st.rerun()

with download_col:
    st.markdown("<br>", unsafe_allow_html=True) # Spacer
    
    if students:
        df = pd.DataFrame(students, columns=['Name', 'Registration No', 'Phone Number', 'Status'])
        csv = df.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="📥 CSV",
            data=csv,
            file_name='student_phone_records.csv',
            mime='text/csv',
            use_container_width=True
        )

# Filter students based on search and filter
filtered_students = []
for student in students:
    name, reg, phone, status = student
    matches_search = (not search_term or 
                     search_term.lower() in name.lower() or 
                     search_term in reg)
    matches_filter = (filter_status == "All" or
                     (filter_status == "Submitted" and phone) or
                     (filter_status == "Pending" and not phone))
    
    if matches_search and matches_filter:
        filtered_students.append(student)

# Display student cards in a grid
st.markdown(f"<p>Showing {len(filtered_students)} of {total_students} students</p>", unsafe_allow_html=True)

# Create responsive grid
cols = st.columns(3)
for idx, student in enumerate(filtered_students):
    name, reg, phone, status = student
    with cols[idx % 3]:
        card_class = "student-card submitted" if phone else "student-card pending"
        badge_class = "submitted-badge" if phone else "pending-badge"
        badge_text = "Submitted" if phone else "Pending"
        emoji = "✅" if phone else "⏳"
        
        st.markdown(f"""
        <div class="{card_class}">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem;">
                <h4 style="margin: 0; color: #2c3e50;">{emoji} {name}</h4>
                <span class="status-badge {badge_class}">{badge_text}</span>
            </div>
            <p style="margin: 0.5rem 0; color: #6c757d;"><strong>🎯 Reg No:</strong> <code>{reg}</code></p>
            {f'<p style="margin: 0.5rem 0; color: #28a745;"><strong>📱 Phone:</strong> {phone}</p>' if phone else 
            '<p style="margin: 0.5rem 0; color: #dc3545;"><strong>📱 Phone:</strong> Not submitted yet</p>'}
            <div style="font-size: 0.8rem; color: #adb5bd; margin-top: 0.8rem;">
                Click to view details
            </div>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div class="footer">
    <div style="display: flex; justify-content: space-around; align-items: center; flex-wrap: wrap;">
        <div>
            <p style="margin: 0;"><strong>📱 Student Phone Registration System</strong></p>
            <p style="margin: 0; font-size: 0.9rem;">Department of Electrical Engineering</p>
        </div>
        <div>
            <p style="margin: 0;">🎯 Fixed at 22 students</p>
            <p style="margin: 0; font-size: 0.9rem;">One submission per student</p>
        </div>
    </div>
    <p style="margin-top: 1rem; font-size: 0.8rem; color: #adb5bd;">
        Last updated: • Auto-saves to PostgreSQL database
    </p>
</div>
""", unsafe_allow_html=True)
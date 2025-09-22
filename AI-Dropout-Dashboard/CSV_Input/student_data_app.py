
import streamlit as st
import pandas as pd
import io

# Configure the page
st.set_page_config(
    page_title="Student Data Management System",
    page_icon="📊",
    layout="wide"
)

# Create sidebar for file uploads
st.sidebar.title("📋 Upload Student Data")
st.sidebar.markdown("---")

# Initialize session state for storing uploaded data
if 'attendance_data' not in st.session_state:
    st.session_state.attendance_data = None
if 'assignments_data' not in st.session_state:
    st.session_state.assignments_data = None
if 'fee_payment_data' not in st.session_state:
    st.session_state.fee_payment_data = None
if 'test_marks_data' not in st.session_state:
    st.session_state.test_marks_data = None

# Function to process uploaded file
def process_uploaded_file(uploaded_file, data_type):
    if uploaded_file is not None:
        try:
            # Read the file based on its extension
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(uploaded_file)
            else:
                st.sidebar.error(f"Unsupported file format for {data_type}")
                return None

            st.sidebar.success(f"✅ {data_type} uploaded successfully!")
            st.sidebar.write(f"📊 Shape: {df.shape[0]} rows, {df.shape[1]} columns")
            return df
        except Exception as e:
            st.sidebar.error(f"Error reading {data_type}: {str(e)}")
            return None
    return None

# Sidebar file upload sections
st.sidebar.subheader("📅 1. Attendance Data")
attendance_file = st.sidebar.file_uploader(
    "Upload attendance spreadsheet",
    type=['csv', 'xlsx', 'xls'],
    key="attendance",
    help="Upload student attendance records"
)
if attendance_file:
    st.session_state.attendance_data = process_uploaded_file(attendance_file, "Attendance")

st.sidebar.markdown("---")

st.sidebar.subheader("📝 2. Assignments Data")
assignments_file = st.sidebar.file_uploader(
    "Upload assignments spreadsheet",
    type=['csv', 'xlsx', 'xls'],
    key="assignments",
    help="Upload student assignment records"
)
if assignments_file:
    st.session_state.assignments_data = process_uploaded_file(assignments_file, "Assignments")

st.sidebar.markdown("---")

st.sidebar.subheader("💰 3. Fee Payment Data")
fee_payment_file = st.sidebar.file_uploader(
    "Upload fee payment spreadsheet",
    type=['csv', 'xlsx', 'xls'],
    key="fee_payment",
    help="Upload student fee payment records"
)
if fee_payment_file:
    st.session_state.fee_payment_data = process_uploaded_file(fee_payment_file, "Fee Payment")

st.sidebar.markdown("---")

st.sidebar.subheader("📊 4. Test Marks Data")
test_marks_file = st.sidebar.file_uploader(
    "Upload test marks spreadsheet",
    type=['csv', 'xlsx', 'xls'],
    key="test_marks",
    help="Upload student test marks records"
)
if test_marks_file:
    st.session_state.test_marks_data = process_uploaded_file(test_marks_file, "Test Marks")

# Main content area
st.title("🎓 Student Data Management System")
st.markdown("### Welcome to the Student Data Management Dashboard")

# Create tabs for different data views
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 Overview", "📅 Attendance", "📝 Assignments", "💰 Fee Payments", "📊 Test Marks"])

with tab1:
    st.header("📋 Data Overview")

    # Status indicators
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.session_state.attendance_data is not None:
            st.success("✅ Attendance Data Loaded")
            st.metric("Records", len(st.session_state.attendance_data))
        else:
            st.warning("⏳ Attendance Data Pending")

    with col2:
        if st.session_state.assignments_data is not None:
            st.success("✅ Assignments Data Loaded")
            st.metric("Records", len(st.session_state.assignments_data))
        else:
            st.warning("⏳ Assignments Data Pending")

    with col3:
        if st.session_state.fee_payment_data is not None:
            st.success("✅ Fee Payment Data Loaded")
            st.metric("Records", len(st.session_state.fee_payment_data))
        else:
            st.warning("⏳ Fee Payment Data Pending")

    with col4:
        if st.session_state.test_marks_data is not None:
            st.success("✅ Test Marks Data Loaded")
            st.metric("Records", len(st.session_state.test_marks_data))
        else:
            st.warning("⏳ Test Marks Data Pending")

    st.markdown("---")
    st.info("👈 Use the sidebar to upload your spreadsheets and navigate through the tabs to view your data.")

with tab2:
    st.header("📅 Attendance Records")
    if st.session_state.attendance_data is not None:
        st.dataframe(st.session_state.attendance_data, use_container_width=True)

        # Download button
        csv = st.session_state.attendance_data.to_csv(index=False)
        st.download_button(
            label="📥 Download Attendance Data",
            data=csv,
            file_name="attendance_data.csv",
            mime="text/csv"
        )
    else:
        st.info("Please upload attendance data using the sidebar.")

with tab3:
    st.header("📝 Assignment Records")
    if st.session_state.assignments_data is not None:
        st.dataframe(st.session_state.assignments_data, use_container_width=True)

        # Download button
        csv = st.session_state.assignments_data.to_csv(index=False)
        st.download_button(
            label="📥 Download Assignments Data",
            data=csv,
            file_name="assignments_data.csv",
            mime="text/csv"
        )
    else:
        st.info("Please upload assignments data using the sidebar.")

with tab4:
    st.header("💰 Fee Payment Records")
    if st.session_state.fee_payment_data is not None:
        st.dataframe(st.session_state.fee_payment_data, use_container_width=True)

        # Download button
        csv = st.session_state.fee_payment_data.to_csv(index=False)
        st.download_button(
            label="📥 Download Fee Payment Data",
            data=csv,
            file_name="fee_payment_data.csv",
            mime="text/csv"
        )
    else:
        st.info("Please upload fee payment data using the sidebar.")

with tab5:
    st.header("📊 Test Marks Records")
    if st.session_state.test_marks_data is not None:
        st.dataframe(st.session_state.test_marks_data, use_container_width=True)

        # Download button
        csv = st.session_state.test_marks_data.to_csv(index=False)
        st.download_button(
            label="📥 Download Test Marks Data",
            data=csv,
            file_name="test_marks_data.csv",
            mime="text/csv"
        )
    else:
        st.info("Please upload test marks data using the sidebar.")

# Footer
st.markdown("---")
st.markdown("**📚 Student Data Management System** | Built with Streamlit")

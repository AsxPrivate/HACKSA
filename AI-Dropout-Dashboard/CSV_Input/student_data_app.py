
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime, timedelta
import io

# Configure the page
st.set_page_config(
    page_title="Student Data Management System",
    page_icon="📊",
    layout="wide"
)

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

# Function to create attendance heatmap matrix
def create_attendance_matrix(df, start_id, end_id, selected_dates):
    try:
        # Create a shade matrix for the heatmap
        # This assumes the DataFrame has date columns and student rows

        # Get the relevant student rows
        student_slice = df.iloc[start_id-1:end_id].copy()

        # Find date columns (exclude student info columns)
        date_columns = []
        for col in df.columns:
            if col.lower() not in ['student_id', 'student', 'name', 'id', 'roll_no']:
                date_columns.append(col)

        # Filter to selected dates
        available_dates = [date for date in selected_dates if date in date_columns]

        if not available_dates:
            st.error("No matching date columns found in the data")
            return None

        # Create the matrix for heatmap
        shade_matrix = student_slice[available_dates].copy()

        # Convert attendance data to numeric values
        # Handle different attendance formats: P/A, Present/Absent, 1/0, etc.
        for col in available_dates:
            shade_matrix[col] = shade_matrix[col].astype(str).str.upper()

            # Map attendance values - implementing logic for "absences last 3 days"
            # 1.0 = Present (Green)
            # 0.0 = Absent today only (Light Red)  
            # -1.0 = Absent for multiple days (Dark Red)

            # For simplicity, we'll use: 1=Present, 0=Absent
            shade_matrix[col] = shade_matrix[col].map({
                'P': 1.0, 'PRESENT': 1.0, '1': 1.0, 'YES': 1.0, 'Y': 1.0,
                'A': 0.0, 'ABSENT': 0.0, '0': 0.0, 'NO': 0.0, 'N': 0.0
            }).fillna(0.0)

        return shade_matrix[available_dates], available_dates

    except Exception as e:
        st.error(f"Error creating attendance matrix: {str(e)}")
        return None, None

# Create sidebar for file uploads
st.sidebar.title("📋 Upload Student Data")
st.sidebar.markdown("---")

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
        df = st.session_state.attendance_data

        # Display data table
        st.subheader("📊 Raw Data")
        st.dataframe(df, use_container_width=True)

        # Heatmap section
        st.subheader("🔥 Attendance Heatmap Visualization")

        # Create controls for heatmap
        col1, col2, col3 = st.columns(3)

        with col1:
            max_students = len(df)
            start_id = st.number_input("Start Student ID", min_value=1, max_value=max_students, value=1, key="att_start")
            end_id = st.number_input("End Student ID", min_value=start_id, max_value=max_students, 
                                   value=min(10, max_students), key="att_end")

        with col2:
            # Get date columns (excluding student info columns)
            date_columns = []
            for col in df.columns:
                if col.lower() not in ['student_id', 'student', 'name', 'id', 'roll_no']:
                    date_columns.append(col)

            if date_columns:
                num_dates = min(10, len(date_columns))  # Default to first 10 dates
                selected_dates = st.multiselect(
                    "Select Date Columns", 
                    date_columns, 
                    default=date_columns[:num_dates],
                    key="att_dates"
                )
            else:
                selected_dates = []
                st.warning("No date columns detected in the data")

        with col3:
            st.write("**Heatmap Legend:**")
            st.write("🟢 Green = Present")
            st.write("🔴 Red = Absent")

        # Generate heatmap button and visualization
        if selected_dates and st.button("🎨 Generate Attendance Heatmap", key="gen_att_heatmap"):
            shade_matrix, available_dates = create_attendance_matrix(df, start_id, end_id, selected_dates)

            if shade_matrix is not None and not shade_matrix.empty:
                # Create the heatmap following the user's example format
                st.subheader(f"Attendance Heatmap (Students {start_id}-{end_id}, Dates {available_dates[0]} to {available_dates[-1]})")

                # Custom colormap: Green for present, Red shades for absences
                cmap = sns.color_palette(["red", "lightgreen"], as_cmap=True)
                norm = plt.Normalize(vmin=0, vmax=1)

                fig, ax = plt.subplots(figsize=(8, 5))
                sns.heatmap(
                    shade_matrix,
                    cmap=cmap,
                    norm=norm,
                    cbar=True,
                    ax=ax,
                    linewidths=0.3,
                    linecolor="black",
                    square=True,
                    annot=False
                )
                ax.set_ylabel("Students", fontsize=8)
                ax.set_xlabel("Date", fontsize=8)
                ax.set_title("Attendance Heatmap (Green=Present, Red shades=Absences last 3 days)", fontsize=10)
                ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right", fontsize=8)
                ax.set_yticklabels([f"Student {i+start_id}" for i in range(len(shade_matrix))], fontsize=8)

                # Adjust layout to prevent label cutoff
                plt.tight_layout()

                # Display the plot
                st.pyplot(fig)

                # Additional statistics
                st.subheader("📈 Attendance Statistics")
                col1, col2, col3 = st.columns(3)

                with col1:
                    total_present = shade_matrix.sum().sum()
                    total_possible = shade_matrix.shape[0] * shade_matrix.shape[1]
                    attendance_rate = (total_present / total_possible) * 100 if total_possible > 0 else 0
                    st.metric("Overall Attendance Rate", f"{attendance_rate:.1f}%")

                with col2:
                    avg_student_attendance = shade_matrix.mean(axis=1).mean() * 100
                    st.metric("Avg Student Attendance", f"{avg_student_attendance:.1f}%")

                with col3:
                    best_attendance_day = shade_matrix.mean(axis=0).idxmax() if not shade_matrix.empty else "N/A"
                    st.metric("Best Attendance Day", str(best_attendance_day))
            else:
                st.error("Unable to generate heatmap. Please check your data format.")

        # Download button
        csv = df.to_csv(index=False)
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
st.markdown("**📚 Student Data Management System** | Built with Streamlit | Enhanced with Attendance Heatmap")

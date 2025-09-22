import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Student Attendance Visualization")

# Load data
df = pd.read_csv("attendance_daily.csv")
attendance_cols = df.columns[2:]

# Calculate attendance percent
df["attendance_percent"] = (df[attendance_cols] == "P").sum(axis=1) / len(attendance_cols) * 100

# 1. Bar Chart: Attendance percentage per student
st.subheader("Bar Chart: Attendance Percentage per Student")
fig, ax = plt.subplots(figsize=(12, 5))
ax.bar(df["Name"], df["attendance_percent"], color='skyblue')
ax.set_ylabel("Attendance %")
ax.set_xlabel("Student Name")
ax.set_title("Attendance Percentage per Student")
plt.xticks(rotation=90)
st.pyplot(fig)

# 2. Histogram: Distribution of attendance percentages
st.subheader("Histogram: Distribution of Attendance Percentages")
fig, ax = plt.subplots()
ax.hist(df["attendance_percent"], bins=10, color='orange', edgecolor='black')
ax.set_xlabel("Attendance %")
ax.set_ylabel("Number of Students")
ax.set_title("Distribution of Attendance Percentages")
st.pyplot(fig)

# 3. Boxplot: Attendance percentage spread
st.subheader("Boxplot: Attendance Percentage Spread")
fig, ax = plt.subplots()
ax.boxplot(df["attendance_percent"], vert=False)
ax.set_xlabel("Attendance %")
ax.set_title("Boxplot of Attendance Percentages")
st.pyplot(fig)

# 4. Heatmap: Daily attendance (students vs dates)
st.subheader("Heatmap: Daily Attendance")
attendance_matrix = df[attendance_cols].replace({"P": 1, "A": 0})
fig, ax = plt.subplots(figsize=(12, 8))
sns.heatmap(attendance_matrix, cmap="YlGnBu", cbar=True, ax=ax)
ax.set_ylabel("Student Index")
ax.set_xlabel("Date")
ax.set_title("Student Daily Attendance Heatmap")
st.pyplot(fig)

# 5. Pie Chart: Attendance status counts (overall)
st.subheader("Pie Chart: Overall Attendance Status")
total_present = (df[attendance_cols] == "P").sum().sum()
total_absent = (df[attendance_cols] == "A").sum().sum()
fig, ax = plt.subplots()
ax.pie([total_present, total_absent], labels=["Present", "Absent"], autopct='%1.1f%%', colors=['green', 'red'])
ax.set_title("Overall Attendance Status")
st.pyplot(fig)

# 6. Line Chart: Average daily attendance over time
st.subheader("Line Chart: Average Daily Attendance Over Time")
avg_daily_attendance = (df[attendance_cols] == "P").mean()
fig, ax = plt.subplots()
ax.plot(attendance_cols, avg_daily_attendance * 100, marker='o')
ax.set_ylabel("Average Attendance %")
ax.set_xlabel("Date")
ax.set_title("Average Daily Attendance Over Time")
plt.xticks(rotation=90)
st.pyplot(fig)
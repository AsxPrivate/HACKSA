import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Data Analysis and Visualization App")

st.header("Attendance Database Preview")

csv_file = "attendance_daily.csv"
try:
    df = pd.read_csv(csv_file)
    st.dataframe(df)
except Exception as e:
    st.error(f"Could not load {csv_file}: {e}")

# Load the daily attendance CSV
df = pd.read_csv("attendance_daily.csv")

# Get attendance columns (excluding ID and Name)
attendance_cols = df.columns[2:]

# Calculate attendance percentage for each student
df["attendance_percent"] = (df[attendance_cols] == "P").sum(axis=1) / len(attendance_cols) * 100

# Select only ID, Name, and attendance_percent
result = df[["ID", "Name", "attendance_percent"]]

# Save to new CSV
result.to_csv("attendance_percent.csv", index=False)
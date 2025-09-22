import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors as mcolors

# Set wide page layout
st.set_page_config(layout="centered")
st.title("Interactive Student Attendance Heatmap")

# Load attendance CSV
df = pd.read_csv("attendance_daily.csv")
attendance_cols = df.columns[2:]  # assuming first 2 columns are ID and Name

# Parameters
window_students = 10   # number of students to display at once
window_dates = 7       # number of dates to display at once
min_id, max_id = int(df["ID"].min()), int(df["ID"].max())
total_dates = len(attendance_cols)

# Initialize session state for navigation
if "student_offset" not in st.session_state:
    st.session_state.student_offset = 0
if "date_offset" not in st.session_state:
    st.session_state.date_offset = max(0, total_dates - window_dates)

# Navigation button callbacks
def move_up(): st.session_state.student_offset = max(0, st.session_state.student_offset - 1)
def move_down(): st.session_state.student_offset = min(max_id - min_id, st.session_state.student_offset + 1)
def move_left(): st.session_state.date_offset = max(0, st.session_state.date_offset - 1)
def move_right(): st.session_state.date_offset = min(total_dates - window_dates, st.session_state.date_offset + 1)

# CSS for floating buttons with custom coordinates
button_css = """
<style>
/* Top-right corner (Up/Down) */
.updown-container {
    position: fixed;
    top: 60px;     /* distance from top */
    right: 30px;   /* distance from right */
    z-index: 1000;
}

/* Bottom-left corner (Left/Right) */
.leftright-container {
    position: fixed;
    bottom: 30px;  /* distance from bottom */
    left: 30px;    /* distance from left */
    z-index: 1000;
}

.arrow-btn {
    font-size: 18px !important;
    padding: 8px 16px;
    margin: 5px;
    border-radius: 10px;
}
</style>
"""
st.markdown(button_css, unsafe_allow_html=True)

# Up/Down buttons
with st.container():
    st.markdown('<div class="updown-container">', unsafe_allow_html=True)
    col_up, col_down = st.columns(2)
    with col_up:
        if st.button("⬆️ Up", key="btn_up"): move_up()
    with col_down:
        if st.button("⬇️ Down", key="btn_down"): move_down()
    st.markdown('</div>', unsafe_allow_html=True)

# Left/Right buttons
with st.container():
    st.markdown('<div class="leftright-container">', unsafe_allow_html=True)
    col_left, col_right = st.columns(2)
    with col_left:
        if st.button("⬅️ Left", key="btn_left"): move_left()
    with col_right:
        if st.button("➡️ Right", key="btn_right"): move_right()
    st.markdown('</div>', unsafe_allow_html=True)

# Calculate current window
start_id = min_id + st.session_state.student_offset
end_id = min(start_id + window_students - 1, max_id)
start_date_idx = st.session_state.date_offset
end_date_idx = min(start_date_idx + window_dates - 1, total_dates - 1)
selected_dates = attendance_cols[start_date_idx:end_date_idx + 1]
df_subset = df[df["ID"].between(start_id, end_id)]

# Convert attendance to numeric: P=1, A=0
attendance_matrix = df_subset[selected_dates].replace({"P": 1, "A": 0}).fillna(1)

# Apply last 3-day absence shading
shade_matrix = attendance_matrix.copy()
for idx, row in attendance_matrix.iterrows():
    for col_idx, col in enumerate(attendance_matrix.columns):
        if col not in selected_dates:
            continue
        # last 3 days including current
        last3_idx = max(0, col_idx - 2)
        last3_values = row[last3_idx:col_idx+1]
        absences = (last3_values == 0).sum()
        if row[col] == 1:
            shade_matrix.at[idx, col] = 0
        else:
            if absences == 1:
                shade_matrix.at[idx, col] = 1  # light red
            elif absences == 2:
                shade_matrix.at[idx, col] = 2  # medium red
            else:
                shade_matrix.at[idx, col] = 3  # dark red

# Use names if available
if "Name" in df.columns:
    shade_matrix.index = df_subset["Name"]
else:
    shade_matrix.index = df_subset["ID"]

# Colormap: Green + 3 reds
cmap = mcolors.ListedColormap(["green", "#ff9999", "#ff4d4d", "#cc0000"])
bounds = [-0.5,0.5,1.5,2.5,3.5]
norm = mcolors.BoundaryNorm(bounds, cmap.N)

# Plot heatmap (compact)
st.subheader(f"Attendance Heatmap (Students {start_id}-{end_id}, Dates {selected_dates[0]} to {selected_dates[-1]})")
fig, ax = plt.subplots(figsize=(8, 5))
sns.heatmap(
    shade_matrix[selected_dates],
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
ax.set_yticklabels(ax.get_yticklabels(), fontsize=8)
st.pyplot(fig)

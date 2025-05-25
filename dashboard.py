import streamlit as st
import pandas as pd

# Load left and right logos properly
col1, col2, col3 = st.columns([1, 4, 1])

with col1:
    st.image("left_logo.png", width=150)

with col3:
    st.image("right_logo.png", width=150)
st.markdown(
    """
    <h1 style="text-align: center;">Don Honorio Ventura State University</h1>
    <h2 style="text-align: center;">College of Business Studies</h2>
    <h3 style="text-align: center;">Automated Class Schedule</h3>
    """,
    unsafe_allow_html=True
)

# Load the generated schedule
df = pd.read_excel("generated_schedulepro.xlsx")

# Define Page Title
st.title("📅 Automated Class Schedule")

# Ensure the DataFrame exists before filtering
filtered_df = df.copy()  # Make a copy of the original data

# Sidebar: Instructor Filter
if "Instructor" in df.columns:
    selected_instructor = st.sidebar.selectbox(
        "🔍 Filter by Instructor", ["None"] + list(df["Instructor"].dropna().unique())
    )

    if selected_instructor != "None":
        filtered_df = filtered_df[filtered_df["Instructor"] == selected_instructor]  # Apply instructor filter

# Sidebar: Section Filter
if "Section" in df.columns:
    selected_section = st.sidebar.selectbox(
        "🔍 Filter by Section", ["None"] + list(df["Section"].dropna().unique())
    )

    if selected_section != "None":
        filtered_df = filtered_df[filtered_df["Section"] == selected_section]  # Apply section filter

# Sidebar: Room Filter
if "Room" in df.columns:
    selected_room = st.sidebar.selectbox(
        "🔍 Filter by Room", ["None"] + list(df["Room"].dropna().unique())
    )

    if selected_room != "None":
        filtered_df = filtered_df[filtered_df["Room"] == selected_room]  # Apply room filter
# Organizing Data into a Timetable Format
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
time_slots = ["7:00 AM- 8:00 AM", "8:00 AM- 9:00 AM", "9:00 AM- 10:00 AM", "10:00 AM- 11:00 AM", "11:00 AM- 12:00 PM", "12:00 PM- 1:00 PM", "1:00 PM- 2:00 PM", "2:00 PM- 3:00 PM", "3:00 PM- 4:00 PM", "4:00 PM- 5:00 PM", "5:00 PM- 6:00 PM"]

# Create a structured timetable
timetable = pd.DataFrame(columns=days, index=time_slots)

for _, row in filtered_df.iterrows():
    entry = f"{row['Subject']} ({row['Instructor']} - {row['Room']})"
    timetable.loc[row["Time Slot"], row["Day"]] = entry

# Display Schedule in Table Format
st.write("📌 **Class Schedule Overview**")
st.table(timetable.fillna(""))

# Add footer details similar to the uploaded schedule
st.write("📌 **Prepared by:** MARIA LIBERTY F. ISIP, MBA (Programmer)")
st.write("📌 **Dean:** LUISITO B. REYES, CBA, MBA")
st.write("📌 **Approved by:** ENRIQUE G. BAKING, Ed.D. (SUC President III)")

subject_colors = {
    "College Algebra": "#FF6666",  # Light Red
    "Business Ethics": "#FFFF99",  # Light Yellow
    "Financial Accounting": "#FF99CC",  # Light Pink
    "Programming 1": "#99FF99",  # Light Green
    "Database Systems": "#FFA500",  # Orange
    "English Communication": "#FF66B2",  # Pink
    "Marketing Principles": "#FFD700",  # Yellow
    "Physics": "#FF4500",  # Red
    "Taxation": "#C6A0DC",  # Light Violet
    "Auditing": "#9933FF",  # Violet
    "Law on Obligations": "#3366FF",  # Blue
    "Rizal's Life": "#99CCFF",  # Light Blue
    "Filipino 1": "#FF8C00",  # Orange
    "Digital Systems": "#F4A261",  # Light Orange
    "Web Development": "#808080",  # Gray
    "Data Structures": "#00FFFF",  # Cyan
    "Managerial Accounting": "#D2B48C",  # Tan
    "Computer Networks": "#008080",  # Teal
    "Operations Management": "#808000",  # Olive
    "Research Methods": "#D3D3D3",  # Light Gray (instead of White)

}
for _, row in filtered_df.iterrows():
    subject = row["Subject"]
    color = subject_colors.get(subject, "#E0E0E0")  # Default gray if not listed
    entry = f'<div style="background-color:{color}; padding:10px; border-radius:5px; text-align:center; font-weight:bold">{subject}<br>({row["Instructor"]} - {row["Room"]})</div>'
    timetable.loc[row["Time Slot"], row["Day"]] = entry
# Remove NaN values before displaying
timetable = timetable.fillna("")

# Display updated color-coded schedule
st.write("📌 **Class Schedule Overview**")
st.markdown(timetable.to_html(escape=False), unsafe_allow_html=True)

# Allow users to edit the schedule dynamically
st.write("✏️ **Update Schedule Dynamically**")

time_slot = st.selectbox("Select Time Slot", timetable.index)
day = st.selectbox("Select Day", timetable.columns)
new_section = st.selectbox("Select Section", df["Section"].unique())  # Added Section Selection
new_subject = st.text_input("Enter New Subject")
new_instructor = st.text_input("Enter Instructor")

if st.button("Update Schedule"):
    # Allow instructor removal (set to an empty string if left blank)
    new_instructor = new_instructor.strip() if new_instructor.strip() else ""

    entry = f'<div style="background-color:#E0E0E0; padding:10px; border-radius:5px; text-align:center; font-weight:bold">{new_subject}<br>{new_instructor}<br>{new_section}</div>'
    
    # Update the schedule dynamically
    timetable.loc[time_slot, day] = entry
    df.loc[(df["Time Slot"] == time_slot) & (df["Day"] == day), ["Section", "Subject", "Instructor"]] = [new_section, new_subject, new_instructor]

    # Save changes back to the Excel file
    df.to_excel("generated_schedulepro.xlsx", index=False)

    st.success("✅ Schedule Updated Successfully!")
if st.button("Remove Schedule"):
    # Remove subject, instructor, and section for the selected time slot and day
    df.loc[(df["Time Slot"] == time_slot) & (df["Day"] == day), ["Subject", "Instructor", "Section"]] = ["", "", ""]

    # Clear the entry in the displayed schedule
    timetable.loc[time_slot, day] = ""

    # Save changes back to the Excel file
    df.to_excel("generated_schedulepro.xlsx", index=False)

    st.success("✅ Schedule Entry Removed Successfully!")
uploaded_files = st.file_uploader("Upload Class Schedule (Excel)", type=["xlsx"], accept_multiple_files=True)


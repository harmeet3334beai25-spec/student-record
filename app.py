
import streamlit as st
import sqlite3
import pandas as pd

# ---------------- DATABASE CONNECTION ----------------

conn = sqlite3.connect("students.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    course TEXT,
    email TEXT,
    phone TEXT
)
""")

conn.commit()

# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="Student Management System",
    page_icon="🎓",
    layout="wide"
)

# ---------------- CUSTOM UI ----------------

st.title("🎓 Student Record Management System")
st.write("Manage student records easily using CRUD operations.")

st.divider()

# ---------------- SIDEBAR ----------------

st.sidebar.title("Navigation")

menu = st.sidebar.radio(
    "Select Operation",
    ["Home", "Add Student", "View Students",
     "Update Student", "Delete Student"]
)

# ---------------- HOME ----------------

if menu == "Home":

    st.header("Dashboard")

    cursor.execute("SELECT COUNT(*) FROM students")
    total = cursor.fetchone()[0]

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Students", total)

    with col2:
        st.metric("Available Operations", 4)

    st.info("Use the sidebar to manage student records.")

    st.subheader("About the System")

    st.write("""
    This application provides the following features:

    - Create: Add new student records.
    - Read: View all student records.
    - Update: Modify existing student details.
    - Delete: Remove student records.
    """)

# ---------------- ADD STUDENT ----------------

elif menu == "Add Student":

    st.header("➕ Add New Student")

    with st.form("add_student_form"):

        name = st.text_input("Student Name")
        age = st.number_input("Age", min_value=1, max_value=100, step=1)
        course = st.selectbox(
            "Select Course",
            ["BCA", "B.Tech", "MCA", "M.Tech", "BBA", "MBA"]
        )
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number")

        submit = st.form_submit_button("Add Student")

        if submit:

            if not name.strip():
                st.error("Student name cannot be empty!")

            elif not email.strip():
                st.error("Email cannot be empty!")

            else:

                cursor.execute("""
                INSERT INTO students (name, age, course, email, phone)
                VALUES (?, ?, ?, ?, ?)
                """, (name, age, course, email, phone))

                conn.commit()

                st.success("Student added successfully!")

# ---------------- VIEW STUDENTS ----------------

elif menu == "View Students":

    st.header("📋 Student Records")

    df = pd.read_sql_query(
        "SELECT * FROM students",
        conn
    )

    if not df.empty:

        st.dataframe(df, use_container_width=True)

        st.subheader("Search Student")

        search = st.text_input("Search by Student Name")

        if search:
            result = df[
                df["name"].str.contains(search, case=False, na=False)
            ]
            st.dataframe(result, use_container_width=True)

    else:
        st.warning("No student records found.")

# ---------------- UPDATE STUDENT ----------------

elif menu == "Update Student":

    st.header("✏️ Update Student Details")

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    if students:

        student_options = {
            f"{s[0]} - {s[1]}": s[0] for s in students
        }

        selected = st.selectbox(
            "Select Student",
            list(student_options.keys())
        )

        student_id = student_options[selected]

        cursor.execute(
            "SELECT * FROM students WHERE id=?",
            (student_id,)
        )

        student = cursor.fetchone()

        with st.form("update_form"):

            name = st.text_input("Student Name", value=student[1])
            age = st.number_input(
                "Age", min_value=1, max_value=100,
                value=student[2]
            )
            course = st.text_input("Course", value=student[3])
            email = st.text_input("Email", value=student[4])
            phone = st.text_input("Phone", value=student[5])

            update = st.form_submit_button("Update Student")

            if update:

                if not name.strip():
                    st.error("Student name cannot be empty!")

                else:
                    cursor.execute("""
                    UPDATE students
                    SET name=?, age=?, course=?, email=?, phone=?
                    WHERE id=?
                    """, (
                        name, age, course, email, phone, student_id
                    ))

                    conn.commit()

                    st.success("Student updated successfully!")

    else:
        st.warning("No students available to update.")

# ---------------- DELETE STUDENT ----------------

elif menu == "Delete Student":

    st.header("🗑️ Delete Student Record")

    cursor.execute("SELECT id, name FROM students")
    students = cursor.fetchall()

    if students:

        student_options = {
            f"{s[0]} - {s[1]}": s[0] for s in students
        }

        selected = st.selectbox(
            "Select Student to Delete",
            list(student_options.keys())
        )

        student_id = student_options[selected]

        st.warning("Are you sure you want to delete this student?")

        if st.button("Delete Student", type="primary"):

            cursor.execute(
                "DELETE FROM students WHERE id=?",
                (student_id,)
            )

            conn.commit()

            st.success("Student deleted successfully!")

    else:
        st.warning("No student records available.")

# ---------------- FOOTER ----------------

st.divider()

st.caption("Student Record Management System | Built with Python & Streamlit")

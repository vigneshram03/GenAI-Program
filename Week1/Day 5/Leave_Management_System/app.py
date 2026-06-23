import streamlit as st
import requests
from datetime import date

API = "http://localhost:8000"

USERS = {
    "employee1": {"password": "emp123", "role": "employee"},
    "employee2": {"password": "emp123", "role": "employee"},
    "manager1": {"password": "mgr123", "role": "manager"},
}

st.set_page_config(page_title="Leave Management", page_icon="🗂")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login(username, password):
    user = USERS.get(username)
    if user and user["password"] == password:
        st.session_state.logged_in = True
        st.session_state.username = username
        st.session_state.role = user["role"]
        return True
    return False

def logout():
    st.session_state.logged_in = False
    st.rerun()

# ---------------- EMPLOYEE FUNCTIONS ----------------

def employee_dashboard():
    st.header("👤 Apply for Leave")

    with st.form("leave_form"):
        start = st.date_input("Start Date", date.today())
        days = st.number_input("Days", min_value=1)
        reason = st.text_area("Reason")
        submit = st.form_submit_button("Submit")

        if submit:
            requests.post(
                f"{API}/apply",
                params={
                    "employee": st.session_state.username,
                    "start_date": start,
                    "days": int(days),
                    "reason": reason,
                },
            )
            st.success("Leave submitted")

def employee_history():
    st.header("📘 Your Leave History")

    r = requests.get(f"{API}/employee/{st.session_state.username}")
    data = r.json()

    if not data:
        st.info("No leave history found")
        return

    st.table(data)

# ---------------- MANAGER FUNCTIONS ----------------

def manager_dashboard():
    st.header("🧑‍💼 Pending Approvals")

    pending = requests.get(f"{API}/pending").json()

    if not pending:
        st.success("No pending requests")
        return

    for leave in pending:
        with st.expander(f"{leave['employee']} | {leave['start_date']} | {leave['days']} days"):
            st.write(f"Reason: {leave['reason']}")
            if st.button("Approve", key=leave["id"]):
                requests.post(f"{API}/approve/{leave['id']}", params={"manager": st.session_state.username})
                st.success("Approved")
                st.rerun()

def manager_team_plan():
    st.header("📅 Team Leave Plan")

    data = requests.get(f"{API}/leave/all").json()

    if not data:
        st.info("No leave records found")
        return

    st.table(data)

# ---------------- LOGIN PAGE ----------------

def login_page():
    st.title("🗂 Leave Management System")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login(username, password):
            st.rerun()
        else:
            st.error("Invalid credentials")

# ---------------- MAIN APP ----------------

if st.session_state.logged_in:
    st.sidebar.write(f"Logged in as: {st.session_state.username}")

    if st.sidebar.button("Logout"):
        logout()

    if st.session_state.role == "employee":
        menu = st.sidebar.radio("Menu", ["Apply Leave", "Leave History"])

        if menu == "Apply Leave":
            employee_dashboard()
        else:
            employee_history()

    else:
        menu = st.sidebar.radio("Menu", ["Pending Approvals", "Team Leave Plan"])

        if menu == "Pending Approvals":
            manager_dashboard()
        else:
            manager_team_plan()

else:
    login_page()

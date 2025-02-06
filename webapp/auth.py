import streamlit as st

USER_CREDENTIALS = {
    "admin": "password123",
    "farmer1": "farmer1",
    "farmer2": "farmer2",
    "rahat":"rahat"
}

def authenticate(username, password):
    return USER_CREDENTIALS.get(username) == password

def login():
    st.title("Farm Monitoring Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        if authenticate(username, password):
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.success("Login successful! Redirecting...")
            st.rerun()
        else:
            st.error("Invalid username or password")

def logout():
    st.session_state["authenticated"] = False
    st.session_state["username"] = None
    st.success("You have been logged out.")

def require_authentication():
    if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
        st.warning("Please log in to continue.")
        login()
        st.stop()

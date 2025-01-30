import streamlit as st
import auth  # Import authentication logic
import dashboard  # Import dashboard logic

# Check authentication
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    auth.login()
else:
    dashboard.show_dashboard()

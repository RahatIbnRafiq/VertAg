import streamlit as st
import auth
import dashboard
import shelf_detail

# Check authentication
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    auth.login()
elif "selected_shelf" in st.session_state:
    shelf_detail.show_shelf_details()
else:
    dashboard.show_dashboard()

import streamlit as st
import auth  # Import authentication logic

def show_dashboard():
    """Main dashboard after successful login."""
    auth.require_authentication()  # Ensure user is logged in

    st.title("Farm Monitoring Dashboard")
    st.write(f"Welcome, {st.session_state['username']}!")

    # Logout button
    if st.button("Logout"):
        auth.logout()
        st.experimental_rerun()  # Refresh the page to go back to login

import streamlit as st
import constants

def show_shelf_details():
    if "selected_shelf" not in st.session_state:
        st.error(constants.ERROR_NO_SHELF_SELECTED)
        st.stop()
        
        
    shelf_id = st.session_state["selected_shelf"]
    st.title(f"Shelf {shelf_id} Details")
    
    
    if st.button("⬅️ Back to Dashboard"):
        del st.session_state["selected_shelf"]
        st.rerun()
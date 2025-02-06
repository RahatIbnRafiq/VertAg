import streamlit as st
import constants
import auth
import os
import pandas as pd
from datetime import datetime


def extract_date_from_filename(filename):
    try:
        date_part = filename.split("_")[0]
        return datetime.strptime(date_part, "%d.%m.%Y")
    except ValueError:
        return datetime.min



# Load health data
@st.cache_data
def load_health_data():
    df = pd.read_csv(constants.DATA_PATH)
    df["health_percentage"] = pd.to_numeric(df["health_percentage"], errors="coerce")
    df["date"] = pd.to_datetime(df["date"])
    df["shelf_id"] = df["shelf_id"].astype(str)
    return df

def show_shelf_details():
    auth.require_authentication()
    
    
    
    if "selected_shelf" not in st.session_state:
        st.error(constants.ERROR_NO_SHELF_SELECTED)
        st.stop()
        
        
    shelf_id = st.session_state["selected_shelf"]
    st.title(f"Shelf {shelf_id} Details")
    
    
    if st.button("⬅️ Back to Dashboard"):
        del st.session_state["selected_shelf"]
        st.rerun()

    shelf_image_path = os.path.join(constants.BASE_DIR, "data", "images", f"shelf_{shelf_id}")
    if not os.path.exists(shelf_image_path):
        st.warning(f"No images found for Shelf {shelf_id}.")
        return
    
    st.warning(f"Images found for Shelf {shelf_id}.")
    cameras = sorted([cam for cam in os.listdir(shelf_image_path) if os.path.isdir(os.path.join(shelf_image_path, cam))])

    df = load_health_data()
    
    
    for camera_id in cameras:
        st.subheader(f"📷 Camera {camera_id}")

        camera_path = os.path.join(shelf_image_path, camera_id)
        images = [img for img in os.listdir(camera_path) if img.lower().endswith((".jpg", ".jpeg", ".png"))]
        images = sorted(images, key=extract_date_from_filename, reverse=True)


        if not images:
            st.warning(f"No images available for Camera {camera_id}.")
            continue
        
        
        with st.container():
            cols = st.columns(len(images))  # Create a column per image
            for idx, img_file in enumerate(images):
                
                img_path = os.path.join(camera_path, img_file)
                with cols[idx]:
                    st.image(img_path, width=100, caption=img_file.split("_")[0])

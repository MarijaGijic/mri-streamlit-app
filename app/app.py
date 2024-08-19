import streamlit as st
import io
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from components.image_loader import load_patient_images
from components.image_filtering import filter_image
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image
import os

default_roi_box = [80, 0, 320, 250]

st.set_page_config(page_title="Mri image viewer", page_icon=":hospital:", initial_sidebar_state="collapsed", layout="wide")

hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)

def plot_image_with_roi(img, roi_box):
        x, y, w, h = roi_box
        fig, ax = plt.subplots()
        ax.imshow(img, cmap='gray')
        rect = Rectangle((x, y), w, h, linewidth =1, edgecolor='r', facecolor='none')
        ax.add_patch(rect)
        plt.axis('off')

        buf = io.BytesIO()
        plt.savefig(buf, format="png", bbox_inches='tight', pad_inches = 0)
        buf.seek(0)
        plt.close(fig)
        return buf

left, right = st.columns(2)

with left:
    # Patient's informations 
    patient_col, _ = st.columns(2)
    with patient_col:
        st.subheader("Informacije o pacijentu")
        patient_id = st.text_input("Unesite ID:")
        load_button = st.button("Ucitaj slike pacijenta")

    # postavljanje slika u session_state 
    if 'images' not in st.session_state:
        st.session_state.images = []

    if load_button:
        try:
            st.session_state.images = load_patient_images(patient_id)
        except Exception as e:
            st.error(f"Error loading images: {e}")

    if st.session_state.images:
            st.markdown("***")
            st.subheader("MRI slike")
            image_display_area = st.columns(len(st.session_state.images))
            for i, img in enumerate(st.session_state.images):
                with image_display_area[i]:
                    st.image(img, use_column_width=True)
                        
with right:
    # postavljanje roi koordinata u session_state
    if 'roi_box' not in st.session_state:
        st.session_state.roi_box = default_roi_box

    st.subheader("Postavi ROI koordinate")
    x, y, w, h = st.columns(4)
    with x:
        roi_x = st.number_input("x", value = st.session_state.roi_box[0], step = 1)
    with y:
        roi_y = st.number_input("y", value = st.session_state.roi_box[1], step = 1)
    with w:
        roi_w = st.number_input("width", value = st.session_state.roi_box[2], step = 1)
    with h:
        roi_h = st.number_input("height", value = st.session_state.roi_box[3], step = 1)

    apply_roi = st.button("Apply ROI")

    if apply_roi:
        st.session_state.roi_box = [roi_x, roi_y, roi_w, roi_h]

    if st.session_state.images and apply_roi:
        st.markdown("***")
        st.subheader("images with applied roi")
        threshold = 50
        roi_box = st.session_state.roi_box
        results = []
        avg_intensities = []

        num_images = len(st.session_state.images)
        image_cols = st.columns(num_images)

        for i, img in enumerate(st.session_state.images):
            img_buf = plot_image_with_roi(img, roi_box)
            with image_cols[i]:
                st.image(img_buf, use_column_width=True)

            x, y, w, h = roi_box
            roi = img[y:y+h, x:x+w]
            avg_intensity = np.mean(roi)
            avg_intensities.append(avg_intensity)
            heart_visible = avg_intensity > threshold
            results.append(heart_visible)

        st.markdown("***")
        st.subheader("Analysis Results")

        container = st.container()
        columns = container.columns(num_images)

        for i, (avg_intensity, heart_visible) in enumerate(zip(avg_intensities, results)):
            with columns[i]:
                st.markdown(f"**Image{i+1}:**")
                st.write(f"- **Average Intensity:** `{avg_intensity:.2f}`" )
                heart_status = ":green_heart: **Heart Visible**" if heart_visible else ":x: **Heart Not Visible**"
                st.write(f"- {heart_status}")
                st.markdown("---")

    # Image processing
    st.subheader("Obrada slike")
    # Odabir slika
    if 'image_selection' not in st.session_state:
        st.session_state.image_selection = 0

    image_select_col, options_col = st.columns(2)

    with image_select_col:
        if st.session_state.images: 
            image_selection = st.selectbox('Odaberite sliku', range(len(st.session_state.images) if 'images' in st.session_state else 0))
            st.session_state.image_selection = image_selection
        else:
            st.selectbox('Odaberite sliku', [])

        if st.session_state.images:
            selected_image = st.session_state.images[st.session_state.image_selection]
            st.subheader("Odabrana slika")
            st.image(selected_image, use_column_width=True)

    with options_col:
        container = st.container(border=True)
        with container:
            apply_filter_button = st.button("Filtriranje")
            enhance_contrast_button = st.button("Podesavanje kontrasta")
    
    # Undo and Redo
    st.subheader("Undo and Redo")
    container = st.container(border=True)
    row1 = container.columns(2, vertical_alignment="center")

    undo_button = row1[0].button("Undo")
    redo_button = row1[1].button("Redo")

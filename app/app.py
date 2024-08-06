import streamlit as st
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from components.image_loader import load_patient_images
from components.image_filtering import filter_image
import numpy as npS
from PIL import Image
import os

st.header("MRI Image Viewer", divider='rainbow')

# Informacije o pacijentu 
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
        st.subheader("MRI slike")
        image_display_area = st.columns(len(st.session_state.images))
        for i, img in enumerate(st.session_state.images):
            with image_display_area[i]:
                st.image(img, use_column_width=True)
                     
# Image processing
st.subheader("Obrada slike")
# Odabir slika
if 'image_selection' not in st.session_state:
    st.session_state.image_selection = 0

image_select_col, image_display_col= st.columns(2)
with image_select_col:
    if st.session_state.images:
        image_selection = st.selectbox('Odaberite sliku', range(len(st.session_state.images) if 'images' in st.session_state else 0))
        st.session_state.image_selection = image_selection
    else:
        st.selectbox('Odaberite sliku', [])

with image_display_col:
    if st.session_state.images:
        selected_image = st.session_state.images[st.session_state.image_selection]
        st.subheader("Odabrana slika")
        st.image(selected_image, use_column_width=True)

    
   

container = st.container(border=True)

apply_filter_button, apply_contrast_button = container.columns(2, vertical_alignment="bottom")
#apply_filter_button.button("Filtriranje")
apply_contrast_button.button("Kontrast")
apply_segmentation_button, morphology_operations_button = container.columns(2, vertical_alignment="center")
apply_segmentation_button.button("Segmentacija")
morphology_operations_button.button("Morfoloske operacije")

# Undo and Redo
st.subheader("Undo and Redo")
container = st.container(border=True)
row1 = container.columns(2, vertical_alignment="center")

undo_button = row1[0].button("Undo")
redo_button = row1[1].button("Redo")

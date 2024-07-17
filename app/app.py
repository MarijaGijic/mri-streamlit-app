import streamlit as st
import numpy as npS
from PIL import Image
import os

st.header("MRI Image Viewer", divider='rainbow')

# Informacije o pacijentu 
col1, col2 = st.columns(2)
with col1:
    st.subheader("Informacije o pacijentu")
    patient_id = st.text_input("Unesite ID:")
    load_button = st.button("Ucitaj slike pacijenta")

with col2:
    st.subheader("MRI slike")
    image_display_area = st.container


# Image processing
st.subheader("Obrada slike")
col11, col22, col33 = st.columns(3)
with col11:
    filter_method = st.selectbox("Filtriranje:", ["Median", "Gauss", "Non-Local Means", "..."])
with col22:
    contrast_slider = st.slider("Podesavanje kontrasta", 0.0, 2.0, 0.2)
with col33:
    segmentation_algorithm = st.selectbox("Segmentacija", ["Thresholding", "Hough Transform", "Klasterizacija"])


container = st.container(border=True)

apply_filter_button, apply_contrast_button = container.columns(2, vertical_alignment="bottom")
apply_filter_button.button("Filtriranje")
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

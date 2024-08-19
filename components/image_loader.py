import os 
from PIL import Image
import numpy as np
from collections import defaultdict
import hashlib
import pickle
import streamlit as st

#----------------Ideja----------------
# pristupanje slikama svakog pojedinacnog pacijenta pomocu id-a
# id je prvi broj koji se pojavljuje u nazivu slika
cache_images_folder = r'C:/Users/marij/Documents/mri_streamlit_app/app/cached_images'
images_path = r'C:/Users/marij/Desktop/images'
image_exensions = ['.jpg', '.png', '.gif', '.jpeg']

@st.cache
def load_patient_images(patient_id):
    cache_key = hashlib.md5(str(patient_id).encode()).hexdigest()
    cache_file = os.path.join(cache_images_folder, f"{cache_key}.pickle")

    if os.path.exists(cache_file):
        with open(cache_file, 'rb') as f:
            patient_images = pickle.load(f)
    
    else:
        patient_images = defaultdict(list) # never raises KeyError
        image_files = [f for f in os.listdir(images_path) if f.endswith(tuple(image_exensions))]


        for image_file in image_files:
            parts = image_file.split('_')
            patient_id_in_file = parts[2]

            if patient_id_in_file == patient_id:
                img = Image.open(os.path.join(images_path, image_file))
                img_array = np.array(img)
                patient_images[patient_id].append(img_array)
        
        with open(cache_file, 'wb') as f:
            pickle.dump(patient_images[patient_id], f)
    
    return patient_images[patient_id]




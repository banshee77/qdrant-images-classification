import os
import streamlit as st
from scripts.image_clasification import classify_new_image
from PIL import Image

with st.form("my-form", clear_on_submit=True):        
    uploaded_files = st.file_uploader("Choose photos to upload", accept_multiple_files=True, type=['png', 'jpeg', 'jpg'])
    submit_button = st.form_submit_button(label='Submit Photos')
    pic_names = [] 
    labels = []

    for uploaded_file in uploaded_files: 
        file = uploaded_file.read() 
        image_result = open(uploaded_file.name, 'wb') 
        image_result.write(file) 
        pic_names.append(uploaded_file.name)
        image_result.close()

    if submit_button:
        for i in range(len(pic_names)):
            name = pic_names[i] 
            labels.append(classify_new_image(name).replace('_', ' '))


        st.success('Image classification completed!') 

for idx, pic_name in enumerate(pic_names):        
    image = Image.open(pic_name)
    thumbnail_size = (300, 300) 
    image.thumbnail(thumbnail_size)
    st.image(image)
    st.info(f'Uploaded "{pic_name}" has been classified as "{labels[idx]}"' ) 
    os.remove(pic_name) 

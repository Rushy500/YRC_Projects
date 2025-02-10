#This is code to convert color images to black and white. I used streamlit function to convert this code to HTML
#After copying the code, in command prompt run "streamlit run c2b.py or whatever name you save in the same IP address as the users command prompt"
import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

st.title("Image Grayscale Converter")

uploaded_file = st.file_uploader("Upload an image file (JPG, PNG, etc.)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)

    if image.mode == 'RGBA':
        image = image.convert('RGB')

    img_array = np.array(image)

    if len(img_array.shape) == 3 and img_array.shape[2] == 3:  
        gry = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)

        st.image(image, caption="Original Image", use_column_width=True)
        st.image(gry, caption="Grayscale Image", use_column_width=True, clamp=True)

        _, buffer = cv2.imencode('.jpg', gry)
        io_buf = io.BytesIO(buffer)

        st.download_button(
            label="Download Grayscale Image",
            data=io_buf,
            file_name="gray_image.jpg",
            mime="image/jpeg"
        )
    else:
        st.error("Uploaded image is not in a valid format. Please try a different image.")
else:
    st.warning("Please upload an image file to continue.")

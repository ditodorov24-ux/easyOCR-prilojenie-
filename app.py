import streamlit as st
from PIL import Image
import pytesseract
import re

st.title("🧾 Food Scanner")

harmful = {
    "e621": "MSG",
    "e250": "Sodium Nitrite",
    "e951": "Aspartame",
    "palmoil": "Palm Oil"
}

uploaded = st.file_uploader(
    "Качи снимка",
    type=["png", "jpg", "jpeg"]
)

if uploaded:

    image = Image.open(uploaded)

    st.image(image)

    # OCR
    text = pytesseract.image_to_string(image)

    st.subheader("OCR Text")
    st.write(text)

    # Clean text
    clean = text.lower()

    clean = re.sub(r'[^a-zA-Z0-9]', '', clean)

    st.subheader("Clean")
    st.write(clean)

    # Search
    found = []

    for item in harmful:

        if item in clean:
            found.append(
                f"{item.upper()} → {harmful[item]}"
            )

    st.subheader("Result")

    if found:

        for f in found:
            st.error(f)

    else:
        st.success("No harmful ingredients")

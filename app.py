import streamlit as st
import easyocr
from PIL import Image
import numpy as np
import re

st.title("🧾 Food Scanner")

# OCR
@st.cache_resource
def load_reader():
    return easyocr.Reader(['en'], gpu=False)

reader = load_reader()

# Вредни съставки
harmful_ingredients = {
    "e621": "MSG",
    "e250": "Sodium Nitrite",
    "e951": "Aspartame",
    "palmoil": "Palm Oil",
    "e102": "Tartrazine",
    "e211": "Sodium Benzoate"
}

# Upload
uploaded_file = st.file_uploader(
    "Качи снимка",
    type=["jpg", "jpeg", "png"]
)

# Само ако има снимка
if uploaded_file is not None:

    # Отваряне на изображението
    image = Image.open(uploaded_file).convert("RGB")

    # Показване
    st.image(image)

    # Convert към numpy
    img_np = np.array(image)

    # OCR
    with st.spinner("Scanning..."):
        results = reader.readtext(img_np)

    # Извличане на текст
    extracted_text = ""

    for r in results:
        extracted_text += r[1] + " "

    # Показване
    st.subheader("OCR Text")
    st.write(extracted_text)

    # Почистване
    clean_text = extracted_text.lower()

    clean_text = re.sub(
        r'[^a-zA-Z0-9]',
        '',
        clean_text
    )

    st.subheader("Clean Text")
    st.write(clean_text)

    # Търсене
    found = []

    for ingredient in harmful_ingredients:

        ingredient_clean = ingredient.lower()

        if ingredient_clean in clean_text:

            found.append(
                ingredient.upper()
                + " → "
                + harmful_ingredients[ingredient]
            )

    # Резултат
    st.subheader("Result")

    if len(found) > 0:

        for item in found:
            st.error(item)

    else:
        st.success("No harmful ingredients found")

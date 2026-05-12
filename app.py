import streamlit as st
import easyocr
from PIL import Image
import numpy as np
import re

# Заглавие
st.title("🧾 Food Scanner")

# OCR loader
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

# Ако има снимка
if uploaded_file is not None:

    # Отваряне
    image = Image.open(uploaded_file).convert("RGB")

    # Показване
    st.image(image, width=300)

    # Convert към numpy
    img_np = np.array(image)

    # OCR
    with st.spinner("Scanning..."):
        results = reader.readtext(img_np)

    # Текст
    extracted_text = " ".join([x[1] for x in results])

    st.subheader("OCR Текст")
    st.write(extracted_text)

    # ------------------------
    # ПОЧИСТВАНЕ НА ТЕКСТА
    # ------------------------
    clean_text = extracted_text.lower()

    clean_text = re.sub(
        r'[\s\-,.:;()]',
        '',
        clean_text
    )

    st.subheader("Почистен текст")
    st.write(clean_text)

    # ------------------------
    # ТЪРСЕНЕ
    # ------------------------
    found = []

    for ingredient, description in harmful_ingredients.items():

        ingredient_clean = ingredient.replace(" ", "").lower()

        if ingredient_clean in clean_text:

            found.append(
                f"{ingredient.upper()} → {description}"
            )

    # ------------------------
    # РЕЗУЛТАТ
    # ------------------------
    st.subheader("Резултат")

    if found:

        for item in found:
            st.error(item)

    else:
        st.success("Няма открити вредни съставки")

import streamlit as st
from PIL import Image
import pytesseract
import re

st.set_page_config(page_title="Food Scanner", layout="centered")

st.title("🧾 Scanner за вредни съставки")

# -----------------------------
# Вредни съставки (regex-safe)
# -----------------------------
HARMFUL_PATTERNS = {
    r"e\s*621": "E621 - MSG",
    r"e\s*250": "E250 - Sodium Nitrite",
    r"e\s*951": "E951 - Aspartame",
    r"e\s*211": "E211 - Sodium Benzoate",
    r"palm\s*oil": "Palm Oil",
}

# -----------------------------
# Upload
# -----------------------------
uploaded_file = st.file_uploader(
    "Качи снимка на етикет",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file:

    image = Image.open(uploaded_file)

    st.image(image, caption="Качена снимка", use_container_width=True)

    # OCR
    text = pytesseract.image_to_string(image)

    st.subheader("🔍 OCR текст")
    st.write(text)

    # ако няма текст
    if not text or text.strip() == "":
        st.error("OCR не разпозна текст. Снимката е лоша или размазана.")
        st.stop()

    # нормализация
    text_lower = text.lower()

    # търсене
    found = []

    for pattern, label in HARMFUL_PATTERNS.items():

        if re.search(pattern, text_lower):
            found.append(label)

    # резултат
    st.subheader("⚠️ Резултат")

    if found:
        for f in found:
            st.error(f)
    else:
        st.success("Не са открити вредни съставки")

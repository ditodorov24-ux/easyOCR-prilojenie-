import streamlit as st
from PIL import Image
import pytesseract
import re

st.title("🧾 Scanner за съставки")

# вредни съставки (по-умно написани)
HARMFUL_PATTERNS = {
    r"e\s*621": "MSG (E621)",
    r"e\s*250": "Sodium Nitrite (E250)",
    r"e\s*951": "Aspartame (E951)",
    r"e\s*211": "Sodium Benzoate (E211)",
    r"palm\s*oil": "Palm Oil",
}

uploaded = st.file_uploader("Качи снимка", type=["png","jpg","jpeg"])

if uploaded:

    image = Image.open(uploaded)

    st.image(image, caption="Снимка")

    # OCR
    text = pytesseract.image_to_string(image)

    st.subheader("OCR резултат")
    st.write(text)

    if not text.strip():
        st.error("OCR не разпозна текст → снимката е лоша или размазана")
        st.stop()

    text_lower = text.lower()

    found = []

    for pattern, name in HARMFUL_PATTERNS.items():

        if re.search(pattern, text_lower):
            found.append(name)

    st.subheader("Резултат")

    if found:
        for f in found:
            st.error("⚠️ " + f)
    else:
        st.success("Не са открити вредни съставки")

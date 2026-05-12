import streamlit as st
import easyocr
import numpy as np
from PIL import Image

# -----------------------------
# Настройки на страницата
# -----------------------------
st.set_page_config(
    page_title="Food Scanner",
    page_icon="🧾",
    layout="centered"
)

st.title("🧾 Проверка за вредни съставки")

# -----------------------------
# OCR модел
# -----------------------------
@st.cache_resource
def load_reader():
    return easyocr.Reader(['bg', 'en'])

reader = load_reader()

# -----------------------------
# Вредни съставки
# -----------------------------
harmful_ingredients = {
    "e621": "Мононатриев глутамат",
    "msg": "Мононатриев глутамат",
    "aspartame": "Аспартам",
    "e951": "Аспартам",
    "sodium nitrite": "Натриев нитрит",
    "e250": "Натриев нитрит",
    "palm oil": "Палмово масло",
    "high fructose corn syrup": "Глюкозо-фруктозен сироп",
    "e102": "Тартразин",
    "e110": "Жълт оцветител",
    "e124": "Понсо 4R",
    "e211": "Натриев бензоат",
}

# -----------------------------
# Качване на изображение
# -----------------------------
uploaded_file = st.file_uploader(
    "Качи снимка на опаковка",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:

    # PIL изображение
    image = Image.open(uploaded_file).convert("RGB")

    st.image(image, caption="Качена снимка", use_container_width=True)

    # Конвертиране към numpy
    image_np = np.array(image)

    # OCR
    with st.spinner("Разчитане на текста..."):
        results = reader.readtext(image_np)

    # Събран текст
    extracted_text = " ".join([res[1] for res in results])

    st.subheader("📄 Разчетен текст")
    st.write(extracted_text)

    # -----------------------------
    # Проверка за вредни съставки
    # -----------------------------
    lower_text = extracted_text.lower()

    found_ingredients = []

    for ingredient, description in harmful_ingredients.items():

        if ingredient in lower_text:
            found_ingredients.append(
                {
                    "ingredient": ingredient.upper(),
                    "description": description
                }
            )

    # -----------------------------
    # Резултати
    # -----------------------------
    st.subheader("⚠️ Анализ")

    if found_ingredients:

        for item in found_ingredients:
            st.error(
                f"{item['ingredient']} → {item['description']}"
            )

    else:
        st.success("Не са открити вредни съставки.")

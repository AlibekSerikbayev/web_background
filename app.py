# app.py
import streamlit as st
from streamlit.components.v1 import html
from PIL import Image
from rembg import remove
import pandas as pd
import requests
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from random import randrange

# Asosiy ilova sozlamalari
st.set_page_config(page_title="Tasvirni qayta ishlash", layout="wide")

# HTML/CSS menyu
menu_html = """
<style>
body {
    margin: 0;
    font-family: Arial, Helvetica, sans-serif;
}
.navbar {
    overflow: hidden;
    background-color: #333;
    position: fixed;
    top: 0;
    width: 100%;
    z-index: 1000;
}
.navbar a {
    float: left;
    display: block;
    color: #f2f2f2;
    text-align: center;
    padding: 14px 16px;
    text-decoration: none;
    font-size: 17px;
}
.navbar a:hover {
    background-color: #ddd;
    color: black;
}
.content {
    padding: 16px;
    margin-top: 50px; /* Adjust based on navbar height */
}
</style>
<div class="navbar">
  <a href="#tasvirlarni_aniqlash" onclick="setPage('Tasvirlarni aniqlash')">Tasvirlarni aniqlash</a>
  <a href="#orqa_fon" onclick="setPage('Orqa fonni olib tashlash')">Orqa fonni olib tashlash</a>
</div>
<script>
    let currentPage = 'Tasvirlarni aniqlash';
    function setPage(page) {
        currentPage = page;
        const pageData = Streamlit.setComponentValue(page);
    }
</script>
"""

# HTML menyuni ko'rsatish
html(menu_html, height=70)

# Foydalanuvchi tanlovini olish
selected_page = st.experimental_get_query_params().get('page', ['Tasvirlarni aniqlash'])[0]

# Har bir sahifa uchun funksiyalar
def tasvirlarni_aniqlash():
    st.markdown("# :rainbow[Tasvirlarni aniqlash]")
    st.markdown("> :green[Rasmni ushbu qismga yuklang]")
    image_file = st.file_uploader("Aniqlanayotgan tasvirni yuklang", type=['jpg', 'png', 'webp', 'jfif'])

    if image_file:
        image = Image.open(image_file)
        if image.size[0] > 2000 or image.size[1] > 2000:
            st.error("Rasm o'lchami 2000x2000 pikseldan kichik bo'lishi kerak.")
        else:
            with st.spinner('Tasvir aniqlanayabdi, iltimos ozgina vaqt kutib turing...'):
                row1, row2 = st.columns(2)
                row1.image(image_file, caption='Dastlabki tasvir')

                def image_detect(image):
                    files = {'image': image}
                    headers = {'X-Api-Key': f"{st.secrets['API_TOKEN']}"}
                    try:
                        response = requests.post(st.secrets['API_URL'], headers=headers, files=files)
                        if response.status_code == 200:
                            st.info("Dastur ishladi! Hammasi joyida.")
                            return response.json()
                        else:
                            return f"Xatolik: {response.status_code}, {response.text}"
                    except Exception as e:
                        return f"Xatolik: {e}"

                detect_result = image_detect(image_file)
                if isinstance(detect_result, str):
                    row2.error(detect_result)
                else:
                    data = [
                        {
                            "labels": item['label'],
                            'confidence': float(item['confidence'])
                        }
                        for item in detect_result
                    ]
                    row2.dataframe(pd.DataFrame(data), use_container_width=True)

                    fig, ax = plt.subplots()
                    ax.imshow(image)
                    ax.axis('off')
                    colors = ['#e14c2c', '#c87765', '#2aad95', '#2dd549', '#24a076', '#cae128', '#ee7b15', '#164bc4',
                              '#6f25cc', '#9832be', '#f12f70', '#d82429', '#ead62d', '#60d41e', '#6aa549', '#16cb97']
                    for item in detect_result:
                        label = item['label']
                        x1 = int(item['bounding_box']['x1'])
                        y1 = int(item['bounding_box']['y1'])
                        x2 = int(item['bounding_box']['x2'])
                        y2 = int(item['bounding_box']['y2'])

                        rect_width = x2 - x1
                        rect_height = y2 - y1
                        rect = patches.Rectangle((x1, y1), rect_width, rect_height, linewidth=1,
                                                  edgecolor=colors[randrange(len(colors))], facecolor='none')

                        ax.add_patch(rect)
                        ax.text(x1, y1 - 10, f'{label.capitalize()} ({x1}, {y1})', color='red', fontsize=8)

                    st.pyplot(fig, use_container_width=True)

def orqa_fonni_olib_tashlash():
    st.markdown("# :sparkles[Orqa fonni olib tashlash]")
    uploaded_file = st.file_uploader("Rasm yuklang", type=['jpg', 'jpeg', 'png'])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Dastlabki tasvir", use_column_width=True)
        with st.spinner("Orqa fon olib tashlanmoqda..."):
            try:
                output = remove(image.tobytes())
                result_image = Image.open(output)
                st.image(result_image, caption="Orqa foni olib tashlangan tasvir", use_column_width=True)
            except Exception as e:
                st.error(f"Xatolik: {e}")

# Tanlangan sahifani yuklash
if selected_page == "Tasvirlarni aniqlash":
    tasvirlarni_aniqlash()
elif selected_page == "Orqa fonni olib tashlash":
    orqa_fonni_olib_tashlash()

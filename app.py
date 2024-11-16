# uzgarish 12
import streamlit as st
from PIL import Image, UnidentifiedImageError
import requests
from rembg import remove
import pandas as pd
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from random import randrange
import io

# Asosiy ilova sozlamalari
st.set_page_config(page_title="Tasvirni qayta ishlash", layout="wide")

# Sidebar menyusi
menu = st.sidebar.radio("Menyu", ["Tasvirlarni aniqlash", "Orqa fonni olib tashlash"])

if menu == "Tasvirlarni aniqlash":
    st.markdown("# :rainbow[Tasvirlarni aniqlash]")
    st.markdown("# :red[Iltimos 2mb gacha fayl yuklang !]")

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

    st.markdown("> :green[Rasmni ushbu qismga yuklang]")
    image_file = st.file_uploader("Aniqlanayotgan tasvirni yuklang", type=['jpg', 'png', 'webp', 'jfif'])

    if image_file:
        try:
            image = Image.open(image_file)
        except UnidentifiedImageError:
            st.error("Fayl tasvir formati sifatida aniqlanmadi. Iltimos, boshqa fayl yuklang.")
        else:
            if image.size[0] > 2000 or image.size[1] > 2000:
                st.error("Rasm o'lchami 2000x2000 pikseldan kichik bo'lishi kerak.")
            else:
                with st.spinner('Tasvir aniqlanayabdi, iltimos ozgina vaqt kutib turing...'):
                    row1, row2 = st.columns(2)
                    row1.image(image_file, caption='Dastlabki tasvir')

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

                        # Rasmni yuklab olish uchun PNG formatida saqlaymiz
                        buf = io.BytesIO()
                        fig.savefig(buf, format='png', bbox_inches='tight')
                        buf.seek(0)

                        st.pyplot(fig, use_container_width=True)
                        st.download_button(
                            label="📥 Aniqlangan rasmni yuklab olish",
                            data=buf,
                            file_name="aniqlangan_rasm.png",
                            mime="image/png"
                        )

elif menu == "Orqa fonni olib tashlash":
    st.markdown("# :rainbow[Orqa fonni olib tashlash]")
    st.markdown("> :green[Rasmni ushbu qismga yuklang]")

    uploaded_file = st.file_uploader("Rasm yuklang", type=['jpg', 'jpeg', 'png', 'jfif', 'webp'])

    # O'lchamlar ro'yxatini qo'shamiz
    aspect_ratio = st.selectbox("Rasm o'lchamini tanlang", ["3x4", "3.5x4.5", "9x6", "6x9"])

    # Yangi fon rangini tanlash
    background_color = st.selectbox("Orqa fon rangini tanlang", ["Oq", "Ko'k"])

    if uploaded_file:
        try:
            image = Image.open(uploaded_file)
        except UnidentifiedImageError:
            st.error("Fayl tasvir sifatida aniqlanmadi. Iltimos, boshqa fayl yuklang.")
        else:
            # Orqa fonni olib tashlash
            with st.spinner("Orqa fon olib tashlanmoqda..."):
                try:
                    # Rasmni PNG formatiga aylantirib yuboramiz
                    byte_stream = io.BytesIO()
                    image.save(byte_stream, format="PNG")
                    byte_stream.seek(0)
                    output = remove(byte_stream.read())
                    result_image = Image.open(io.BytesIO(output))

                    # O'lchamlarni tanlangan qiymatga moslashtiramiz
                    if aspect_ratio == "3x4":
                        result_image = result_image.resize((300, 400))
                    elif aspect_ratio == "3.5x4.5":
                        result_image = result_image.resize((350, 450))
                    elif aspect_ratio == "9x6":
                        result_image = result_image.resize((900, 600))
                    elif aspect_ratio == "6x9":
                        result_image = result_image.resize((600, 900))

                    # Yangi fonni tanlangan rangga to'ldiramiz
                    if background_color == "Oq":
                        background = Image.new("RGBA", result_image.size, (255, 255, 255, 255))  # Oq fon
                    else:
                        background = Image.new("RGB", result_image.size, (64, 224, 208))  # Ko'k fon

                    # Rasmni orqa fon bilan birlashtiramiz
                    background.paste(result_image, (0, 0), result_image.convert("RGBA").split()[3])  # Alfa kanalini qo'llash

                    buf = io.BytesIO()
                    background.save(buf, format="PNG")
                    buf.seek(0)

                    st.image(background, caption="Orqa foni olib tashlangan va yangi fon bilan tasvir", use_column_width=True)

                    # Rasmni yuklab olish
                    st.download_button(
                        label="📥 Orqa foni olib tashlangan va yangi fonli rasmni yuklab olish",
                        data=buf,
                        file_name="orqa_fonsiz_yangi_fonli_rasm.png",
                        mime="image/png"
                    )
                except Exception as e:
                    st.error(f"Xatolik: {e}")

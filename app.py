# File path: app.py

import streamlit as st
import requests
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from PIL import Image
import pandas as pd
from random import randrange
from io import BytesIO
#uzgarish
# API kalitlari
OBJECT_DETECTION_API_URL = "https://api.api-ninjas.com/v1/objectdetection"
# API kalitlari
OBJECT_DETECTION_API_URL = "https://api.api-ninjas.com/v1/objectdetection"
OBJECT_DETECTION_API_TOKEN = "BBmkbdXKOWYZHpDRy76UFw==8UmOG7IHI9XryWjO"
REMOVE_BG_API_URL = "https://api.remove.bg/v1.0/removebg"
REMOVE_BG_API_KEY = "7CtBt2JdDVBZFQfQHgd9qouA"

# Bosh sahifa boshqaruvi
st.sidebar.title("Navigatsiya")
page = st.sidebar.radio("Sahifani tanlang:", ["Tasvirlarni aniqlash", "Orqa fonni olib tashlash"])

# Tasvirlarni aniqlash sahifasi
if page == "Tasvirlarni aniqlash":
    st.markdown("# :rainbow[Tasvirlarni aniqlash]")

    # Tasvirni aniqlash funksiyasi
    def image_detect(image):
        try:
            files = {'image': image}
            headers = {'X-Api-Key': OBJECT_DETECTION_API_TOKEN}
            response = requests.post(OBJECT_DETECTION_API_URL, headers=headers, files=files)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as errh:
            return f"HTTP Error: {errh}"
        except requests.exceptions.ConnectionError as errc:
            return f"Error Connecting: {errc}"
        except requests.exceptions.Timeout as errt:
            return f"Timeout Error: {errt}"
        except requests.exceptions.RequestException as err:
            return f"Something went wrong: {err}"

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

                detect_result = image_detect(image_file)
                if isinstance(detect_result, dict):
                    data = []
                    for i in range(len(detect_result)):
                        data.append({
                            "labels": detect_result[i]['label'],
                            'confidence': float(detect_result[i]['confidence'])
                        })
                    dataFrame = pd.DataFrame(data)
                    row2.dataframe(dataFrame, use_container_width=True)

                    fig, ax = plt.subplots()
                    ax.imshow(image)
                    ax.axis('off')
                    colors = ['#e14c2c', '#c87765', '#2aad95', '#2dd549', '#24a076', '#cae128', '#ee7b15',
                              '#164bc4', '#6f25cc', '#9832be', '#f12f70', '#d82429', '#ead62d', '#60d41e', '#6aa549', '#16cb97']

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
                else:
                    row2.error(detect_result)

# Orqa fonni olib tashlash sahifasi
elif page == "Orqa fonni olib tashlash":
    st.title(" Rasm orqa fonini olib tashlash dasturi")
    st.markdown("API orqali yuklangan rasmning orqa fonini olib tashlash")

    image_file = st.file_uploader("Tasvirni yuklang (jpg, png, webp, yoki jfif formatlar)", type=['jpg', 'png', 'webp', 'jfif'])

    if image_file:
        image = Image.open(image_file)
        st.image(image, caption="Dastlabki tasvir", use_column_width=True)

        st.markdown("###  Orqa fon olib tashlanmoqda...")
        with st.spinner("Iltimos kuting..."):
            try:
                files = {"image_file": image_file}
                headers = {"X-Api-Key": REMOVE_BG_API_KEY}

                response = requests.post(REMOVE_BG_API_URL, files=files, headers=headers)
                response.raise_for_status()
                removed_bg_image = Image.open(BytesIO(response.content))
                st.success(" Orqa fon muvaffaqiyatli olib tashlandi!")
                st.image(removed_bg_image, caption="Orqa fon olib tashlangan tasvir", use_column_width=True)

                buf = BytesIO()
                removed_bg_image.save(buf, format="PNG")
                buf.seek(0)
                st.download_button(
                    label=" Tasvirni yuklab olish",
                    data=buf,
                    file_name="removed_background.png",
                    mime="image/png"
                )
            except requests.exceptions.HTTPError as errh:
                st.error(f"HTTP Error: {errh}")
            except requests.exceptions.ConnectionError as errc:
                st.error(f"Error Connecting: {errc}")
            except requests.exceptions.Timeout as errt:
                st.error(f"Timeout Error: {errt}")
            except requests.exceptions.RequestException as err:
                st.errorREMOVE_BG_API_KEY = "7CtBt2JdDVBZFQfQHgd9qouA"

# Bosh sahifa boshqaruvi
st.sidebar.title("Navigatsiya")
page = st.sidebar.radio("Sahifani tanlang:", ["Tasvirlarni aniqlash", "Orqa fonni olib tashlash"])

# Tasvirlarni aniqlash sahifasi
if page == "Tasvirlarni aniqlash":
    st.markdown("# :rainbow[Tasvirlarni aniqlash]")

    # Tasvirni aniqlash funksiyasi
    def image_detect(image):
        files = {'image': image}
        headers = {'X-Api-Key': OBJECT_DETECTION_API_TOKEN}
        try:
            response = requests.post(OBJECT_DETECTION_API_URL, headers=headers, files=files)
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
        image = Image.open(image_file)
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
                    data = []
                    for i in range(len(detect_result)):
                        data.append({
                            "labels": detect_result[i]['label'],
                            'confidence': float(detect_result[i]['confidence'])
                        })
                    dataFrame = pd.DataFrame(data)
                    row2.dataframe(data, use_container_width=True)

                    fig, ax = plt.subplots()
                    ax.imshow(image)
                    ax.axis('off')
                    colors = ['#e14c2c', '#c87765', '#2aad95', '#2dd549', '#24a076', '#cae128', '#ee7b15',
                              '#164bc4', '#6f25cc', '#9832be', '#f12f70', '#d82429', '#ead62d', '#60d41e', '#6aa549', '#16cb97']

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

# Orqa fonni olib tashlash sahifasi
elif page == "Orqa fonni olib tashlash":
    st.title("🎨 Rasm orqa fonini olib tashlash dasturi")
    st.markdown("API orqali yuklangan rasmning orqa fonini olib tashlash")

    image_file = st.file_uploader("Tasvirni yuklang (jpg, png, webp, yoki jfif formatlar)", type=['jpg', 'png', 'webp', 'jfif'])

    if image_file:
        image = Image.open(image_file)
        st.image(image, caption="Dastlabki tasvir", use_column_width=True)

        st.markdown("### ⏳ Orqa fon olib tashlanmoqda...")
        with st.spinner("Iltimos kuting..."):
            try:
                files = {"image_file": image_file}
                headers = {"X-Api-Key": REMOVE_BG_API_KEY}

                response = requests.post(REMOVE_BG_API_URL, files=files, headers=headers)

                if response.status_code == 200:
                    removed_bg_image = Image.open(BytesIO(response.content))
                    st.success("✅ Orqa fon muvaffaqiyatli olib tashlandi!")
                    st.image(removed_bg_image, caption="Orqa fon olib tashlangan tasvir", use_column_width=True)

                    buf = BytesIO()
                    removed_bg_image.save(buf, format="PNG")
                    buf.seek(0)
                    st.download_button(
                        label="📥 Tasvirni yuklab olish",
                        data=buf,
                        file_name="removed_background.png",
                        mime="image/png"
                    )
                else:
                    st.error(f"Xato: {response.status_code}. {response.text}")
            except Exception as e:
                st.error(f"Xatolik yuz berdi: {e}")

import os
import subprocess
import sys

# --- OTOMATİK KÜTÜPHANE YÜKLEME SİSTEMİ ---
# requirements.txt dosyasına ihtiyaç kalmaması için kütüphaneleri arka planda kurar.
def install_requirements():
    required_packages = {
        "opencv-python-headless": "cv2",
        "pillow": "PIL",
        "numpy": "numpy"
    }
    for package, import_name in required_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Kütüphaneleri otomatik yükle
install_requirements()

import streamlit as st
import cv2
import numpy as np
from PIL import Image

# --- WEB SİTESİ ARAYÜZÜ ---
st.set_page_config(page_title="Tabela En-Boy Ölçer", layout="centered")

st.title("📐 Akıllı Tabela & En-Boy Ölçer")
st.write("Telefonunuzdan kamerayı açıp fotoğraf çekin. Sistem objeleri otomatik tespit edip oranlarını çıkaracaktır.")

# Mobil cihazlarda arka kamerayı öncelikli olarak açması için kamera bileşeni
img_file = st.camera_input("Kamera", label_visibility="collapsed")

if img_file is not None:
    # Fotoğrafı OpenCV formatına dönüştür
    image = Image.open(img_file)
    img_np = np.array(image)
    original_img = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    
    # Görüntü işleme adımları (Sınırları belirginleştirme)
    gray = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 30, 150)
    
    # Sınır çizgilerini (konturları) bul
    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Çok küçük gürültüleri ele (Alanı 1200 pikselden büyük olan gerçek objeleri al)
    valid_contours = [c for c in contours if cv2.contourArea(c) > 1200]
    
    if valid_contours:
        st.success(f"Fotoğrafta {len(valid_contours)} adet potansiyel obje algılandı!")
        
        # Kullanıcının listeden ölçmek istediği objeyi seçmesini sağlayan menü
        options = ["Ölçmek istediğiniz objeyi seçin..."] + [f"Obje #{i+1}" for i in range(len(valid_contours))]
        selected_option = st.selectbox("Hangi objenin en-boy oranını görmek istersiniz?", options)
        
        if selected_option != "Ölçmek istediğiniz objeyi seçin...":
            # Seçilen objenin numarasını al
            idx = int(selected_option.split("#")[1]) - 1
            chosen_contour = valid_contours[idx]
            
            # Objeyi yeşil çerçeveye al
            x, y, w, h = cv2.boundingRect(chosen_contour)
            preview_img = original_img.copy()
            cv2.rectangle(preview_img, (x, y), (x + w, y + h), (0, 255, 0), 4)
            
            # En-boy oranını hesapla (Genişlik / Yükseklik)
            aspect_ratio = w / h if h > 0 else 0
            
            # Sonucu çizilmiş görselle birlikte göster
            st.image(cv2.cvtColor(preview_img, cv2.COLOR_BGR2RGB), use_container_width=True)
            
            # Bilgi paneli ve metrikler
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Genişlik", f"{w} px")
            with col2:
                st.metric("Yükseklik", f"{h} px")
            with col3:
                st.metric("En-Boy Oranı", f"1 : {aspect_ratio:.2f}")
                
            st.info(f"💡 Seçtiğiniz objenin genişliği, yüksekliğinin tam **{aspect_ratio:.2f}** katıdır.")
            
        else:
            # Henüz bir obje seçilmediyse tüm objeleri kırmızı kutu ve numaralarla ekranda göster
            all_objs_img = original_img.copy()
            for i, c in enumerate(valid_contours):
                x, y, w, h = cv2.boundingRect(c)
                cv2.rectangle(all_objs_img, (x, y), (x + w, y + h), (0, 0, 255), 3)
                cv2.putText(all_objs_img, f"#{i+1}", (x + 10, y + 35), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)
                
            st.image(cv2.cvtColor(all_objs_img, cv2.COLOR_BGR2RGB), caption="Algılanan Tüm Objeler", use_container_width=True)
            st.info("Lütfen yukarıdaki listeden ölçmek istediğiniz objenin numarasını seçin.")
            
    else:
        st.warning("Fotoğrafta net bir nesne algılanamadı. Lütfen daha düzgün bir ışıkta veya kontrastı yüksek bir açıda tekrar deneyin.")
        st.image(image, use_container_width=True)

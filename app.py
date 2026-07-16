import streamlit as st
from PIL import Image
import io
import base64
from streamlit_drawable_canvas import st_canvas
import numpy as np
import datetime

st.set_page_config(
    page_title="Tabela Ölçüm",
    page_icon="📏",
    layout="wide",
    initial_sidebar_state="collapsed"  # Mobile dostu
)

# CSS ile mobil tam ekran ve basit UI
st.markdown("""
<style>
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    button {
        width: 100%;
    }
    .stCanvas {
        max-height: 70vh;
    }
</style>
""", unsafe_allow_html=True)

st.title("📏 Tabela Ölçüm Uygulaması")
st.markdown("Telefon kamerası ile tabela fotoğraflayın, çizgilerle ölçüm yapın ve kaydedin.")

# Session state
if 'captured_image' not in st.session_state:
    st.session_state.captured_image = None
if 'canvas_result' not in st.session_state:
    st.session_state.canvas_result = None

col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("📸 Kamera")
    camera_input = st.camera_input("Fotoğraf Çek", key="camera")

    if camera_input is not None:
        st.session_state.captured_image = camera_input
        st.success("Fotoğraf çekildi! Sağ tarafta düzenleyin.")

with col2:
    st.subheader("✏️ Düzenleme ve Ölçüm")
    
    if st.session_state.captured_image is not None:
        # PIL Image'e çevir
        image = Image.open(st.session_state.captured_image)
        
        # Canvas ayarları
        drawing_mode = st.selectbox(
            "Çizim Modu",
            ("line", "freedraw", "rect", "circle", "transform")
        )
        
        stroke_width = st.slider("Çizgi Kalınlığı", 1, 20, 5)
        stroke_color = st.color_picker("Çizgi Rengi", "#FF0000")
        
        # Canvas
        canvas_result = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",
            stroke_width=stroke_width,
            stroke_color=stroke_color,
            background_image=image,
            update_streamlit=True,
            height=int(image.height * 0.8),  # Oranlı
            width=int(image.width * 0.8),
            drawing_mode=drawing_mode,
            key="canvas_key",
        )
        
        st.session_state.canvas_result = canvas_result
        
        # Ölçüm notları
        st.subheader("📝 Ölçüm Bilgileri")
        width_ratio = st.number_input("Genişlik Oranı (ör: 1.5)", value=1.0, step=0.1)
        height_ratio = st.number_input("Yükseklik Oranı (ör: 2.0)", value=1.0, step=0.1)
        notes = st.text_area("Notlar (tabela metni, konum vb.)", "")
        
        # Kaydet
        if st.button("💾 Kaydet ve İndir", type="primary"):
            if canvas_result.image_data is not None:
                # Annotated image
                annotated_img = Image.fromarray(canvas_result.image_data.astype("uint8"))
                
                # Metadata ekle
                draw = ImageDraw.Draw(annotated_img) if 'ImageDraw' in globals() else None
                
                # Bytes olarak kaydet
                buf = io.BytesIO()
                annotated_img.save(buf, format="PNG")
                buf.seek(0)
                
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"tabela_olcumu_{timestamp}.png"
                
                st.download_button(
                    label="📥 İndir (PNG)",
                    data=buf,
                    file_name=filename,
                    mime="image/png",
                )
                
                # JSON verisi (ölçümler)
                if canvas_result.json_data:
                    st.json({
                        "width_ratio": width_ratio,
                        "height_ratio": height_ratio,
                        "notes": notes,
                        "objects": canvas_result.json_data.get("objects", [])
                    })
                
                st.success("Kaydedildi! İndirin.")
            else:
                st.warning("Değişiklik yapın.")
    else:
        st.info("Önce sol taraftan fotoğraf çekin.")

# Ekstra talimatlar
st.markdown("---")
st.markdown("""
### Nasıl Kullanılır?
1. **Mobil tarayıcıda** (Chrome önerilir) tam ekran yapın.
2. Kamera ile tabela fotoğrafı çekin.
3. Sağ tarafta **line** modu ile kenarlara çizgi çekin (ölçüm referansı).
4. Manuel ölçüm oranlarını girin.
5. **Kaydet** ile PNG indirin (telefonunuza kaydedin).
""")

st.caption("GitHub'a yüklemek için app.py olarak kaydedin. requirements.txt: streamlit, streamlit-drawable-canvas, pillow")

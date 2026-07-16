import streamlit as st
from PIL import Image, ImageDraw
import io
import datetime

st.set_page_config(
    page_title="📏",
    page_icon="📸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Agresif tam ekran + temiz görünüm
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {padding: 0 !important;}
    [data-testid="stHeader"], [data-testid="stToolbar"], footer, header {display: none !important;}
    .main {padding: 0 !important; margin: 0;}
    .stCameraInput video, .stCameraInput {width: 100vw !important; height: 82vh !important; object-fit: cover;}
    button {font-size: 1.3rem; padding: 18px !important; margin: 5px 0;}
</style>
""", unsafe_allow_html=True)

# Session State
if 'photo' not in st.session_state:
    st.session_state.photo = None

# ====================== ANA EKRAN ======================
if st.session_state.photo is None:
    # Kamera Ekranı
    st.markdown("<h2 style='text-align:center; margin:8px 0 15px 0; color:white;'>📸 Tabela Çek</h2>", unsafe_allow_html=True)
    
    photo = st.camera_input("", key="camera_key", label_visibility="collapsed")
    
    if photo is not None:
        st.session_state.photo = photo
        st.rerun()

else:
    # Düzenleme + Çizim Ekranı
    img = Image.open(st.session_state.photo)
    
    try:
        from streamlit_drawable_canvas import st_canvas
    except ImportError:
        st.error("Paket yüklenmedi. requirements.txt kontrol et.")
        st.stop()
    
    canvas_result = st_canvas(
        background_image=img,
        height=max(400, int(img.height * 0.78)),
        width=int(img.width * 0.92),
        drawing_mode="line",
        stroke_width=8,
        stroke_color="#FF0000",
        fill_color="rgba(255, 0, 0, 0.15)",
        update_streamlit=True,
        key="full_canvas",
    )

    # Alt Butonlar (Sabit)
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🔄 Yeni Çek", use_container_width=True):
            st.session_state.photo = None
            st.rerun()
    
    with col2:
        if st.button("💾 KAYDET & İNDİR", type="primary", use_container_width=True):
            if canvas_result and canvas_result.image_data is not None:
                annotated_img = Image.fromarray(canvas_result.image_data.astype("uint8"))
                
                # Overlay
                draw = ImageDraw.Draw(annotated_img)
                draw.text((30, 30), "ÖLÇÜM KAYDEDİLDİ", fill=(0, 255, 0), size=45)
                
                buf = io.BytesIO()
                annotated_img.save(buf, format="PNG")
                buf.seek(0)
                
                ts = datetime.datetime.now().strftime("%H%M%S")
                st.download_button(
                    label="📥 PNG İNDİR",
                    data=buf,
                    file_name=f"tabela_{ts}.png",
                    mime="image/png",
                    use_container_width=True
                )
            else:
                st.warning("Lütfen çizgi çekin")

st.markdown("<div style='text-align:center; color:#555; font-size:0.8rem; padding:8px;'>Tabela Ölçüm • Çiz ve Kaydet</div>", unsafe_allow_html=True)

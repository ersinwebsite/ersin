import streamlit as st
from PIL import Image, ImageDraw
import io
import datetime

# Tam ekran + minimal görünüm
st.set_page_config(
    page_title="Ölçüm",
    page_icon="📏",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Tüm gereksiz elementleri gizle
st.markdown("""
<style>
    .main .block-container {padding: 0 !important; margin: 0;}
    header, footer, [data-testid="stToolbar"], [data-testid="stDecoration"] {display: none !important;}
    .stApp {padding: 0;}
    button {width: 100%; font-size: 1.2rem; padding: 15px;}
    .stCameraInput {width: 100vw; height: 85vh;}
</style>
""", unsafe_allow_html=True)

# Session
if 'photo' not in st.session_state:
    st.session_state.photo = None
if 'canvas_result' not in st.session_state:
    st.session_state.canvas_result = None

# Kamera (tam ekran)
if st.session_state.photo is None:
    st.markdown("<h1 style='text-align: center; margin: 10px;'>📸 Tabela Çek</h1>", unsafe_allow_html=True)
    
    photo = st.camera_input("", key="cam", label_visibility="collapsed")
    
    if photo is not None:
        st.session_state.photo = photo
        st.rerun()

else:
    # Düzenleme ekranı
    img = Image.open(st.session_state.photo)
    
    from streamlit_drawable_canvas import st_canvas
    
    canvas_result = st_canvas(
        background_image=img,
        height=int(img.height * 0.82),
        width=int(img.width * 0.95),
        drawing_mode="line",
        stroke_width=6,
        stroke_color="#FF0000",
        fill_color="rgba(255,0,0,0.1)",
        update_streamlit=True,
        key="canvas_full",
    )
    
    st.session_state.canvas_result = canvas_result
    
    # Alt Butonlar
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Yeni Fotoğraf Çek", use_container_width=True):
            st.session_state.photo = None
            st.rerun()
    
    with col2:
        if st.button("💾 KAYDET", type="primary", use_container_width=True):
            if canvas_result and canvas_result.image_data is not None:
                annotated = Image.fromarray(canvas_result.image_data.astype("uint8"))
                
                # Basit ölçü overlay
                draw = ImageDraw.Draw(annotated)
                draw.text((20, 20), "ÖLÇÜM KAYDEDİLDİ", fill="#00FF00", size=50)
                
                buf = io.BytesIO()
                annotated.save(buf, format="PNG")
                buf.seek(0)
                
                ts = datetime.datetime.now().strftime("%H%M%S")
                st.download_button(
                    "📥 İNDİR",
                    data=buf,
                    file_name=f"olcum_{ts}.png",
                    mime="image/png",
                    use_container_width=True
                )
            else:
                st.warning("Çizim yapıp tekrar deneyin.")

# Çok basit footer
st.markdown("<div style='text-align:center; color:#666; font-size:0.8rem; margin-top:5px;'>Tabela Ölçüm • Çiz ve Kaydet</div>", unsafe_allow_html=True)

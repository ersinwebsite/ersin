import streamlit as st
from PIL import Image, ImageDraw
import io
import datetime

st.set_page_config(
    page_title="Tabela Ölçer",
    page_icon="📏",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Mobil tam ekran iyileştirmesi
st.markdown("""
<style>
    .main .block-container {padding-top: 0.5rem; padding-bottom: 0rem;}
    button[kind="primary"] {width: 100% !important;}
</style>
""", unsafe_allow_html=True)

st.title("📏 Tabela Ölçüm Uygulaması")
st.caption("Telefon kamerasıyla tabela ölçümü • Çizgi + Oran")

# Session State
if 'photo' not in st.session_state:
    st.session_state.photo = None
if 'last_canvas' not in st.session_state:
    st.session_state.last_canvas = None

col_camera, col_edit = st.columns([1.8, 1])

with col_camera:
    st.subheader("📸 Kamera")
    photo = st.camera_input("Tabelayı fotoğrafla", key="cam_input")
    
    if photo is not None:
        st.session_state.photo = photo
        st.success("✅ Fotoğraf yüklendi. Sağ tarafta düzenleyin.")

with col_edit:
    st.subheader("✏️ Çizim & Ölçüm")
    
    if st.session_state.photo is not None:
        img = Image.open(st.session_state.photo)
        
        # Çizim ayarları
        mode = st.selectbox("Araç", ["line", "rect", "freedraw", "circle", "transform"], index=0)
        stroke_w = st.slider("Kalınlık", 2, 15, 5)
        color = st.color_picker("Renk", "#FF0000")
        
        from streamlit_drawable_canvas import st_canvas
        
        canvas_result = st_canvas(
            background_image=img,
            height=int(img.height * 0.75),
            width=int(img.width * 0.75),
            drawing_mode=mode,
            stroke_width=stroke_w,
            stroke_color=color,
            fill_color="rgba(255,165,0,0.2)",
            update_streamlit=True,
            key="canvas",
        )
        
        st.session_state.last_canvas = canvas_result
        
        # Ölçüm girdileri
        st.subheader("📐 Ölçümler")
        col_w, col_h = st.columns(2)
        with col_w:
            width_ratio = st.number_input("Genişlik (m)", value=1.5, step=0.1)
        with col_h:
            height_ratio = st.number_input("Yükseklik (m)", value=2.0, step=0.1)
        
        notes = st.text_area("Notlar / Tabela Metni", placeholder="Örn: Cadde adı, tarih...")
        
        if st.button("💾 Kaydet ve İndir", type="primary"):
            if canvas_result and canvas_result.image_data is not None:
                annotated = Image.fromarray(canvas_result.image_data.astype("uint8"))
                
                # Basit metadata overlay
                draw = ImageDraw.Draw(annotated)
                draw.text((10, 10), f"W:{width_ratio}m H:{height_ratio}m", fill="#00FF00")
                
                buf = io.BytesIO()
                annotated.save(buf, format="PNG")
                buf.seek(0)
                
                ts = datetime.datetime.now().strftime("%Y%m%d_%H%M")
                filename = f"tabela_olcumu_{ts}.png"
                
                st.download_button(
                    "📥 PNG İndir",
                    data=buf,
                    file_name=filename,
                    mime="image/png"
                )
                
                st.success("Kaydedildi!")
                st.balloons()
            else:
                st.warning("Önce bir çizim yapın.")
    else:
        st.info("← Sol taraftan fotoğraf çekin")

st.divider()
st.markdown("**İpuçları:**\n- Line/Rect ile tabela kenarlarını işaretleyin\n- Ölçümleri manuel girin\n- Chrome'da tam ekran kullanın")

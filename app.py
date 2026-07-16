import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Tabela Ölçer PRO",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Güçlü Temizleme + Buton Görünürlüğü
st.markdown("""
    <style>
        #MainMenu, header, footer, [data-testid="stToolbar"], 
        [data-testid="stDecoration"], [data-testid="stStatusWidget"], 
        [data-testid="stViewerBadge"], .stAppDeployButton {display: none !important;}

        html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
            overflow: hidden !important;
            height: 100vh !important;
            height: 100dvh !important;
        }

        div[data-testid="stHtml"] iframe {
            width: 100vw !important;
            height: 100vh !important;
            height: 100dvh !important;
            border: none !important;
            background: #000 !important;
            position: fixed;
            top: 0;
            left: 0;
            z-index: 999999 !important;
        }
    </style>
""", unsafe_allow_html=True)

html_code = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Tabela Ölçer PRO</title>
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        
        html, body {
            height: 100vh;
            height: 100dvh;
            width: 100vw;
            background: #000;
            overflow: hidden;
            color: white;
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
        }

        .screen {
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 100%;
            display: none;
        }
        .screen.active { display: block; }

        /* ====================== BUTONLAR ====================== */
        .camera-overlay {
            position: absolute;
            bottom: 8%;
            left: 0;
            width: 100%;
            display: flex;
            justify-content: center;
            z-index: 9999 !important;
            pointer-events: none;
        }

        .shutter-btn {
            width: 90px;
            height: 90px;
            background: rgba(255,255,255,0.25);
            border: 6px solid white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 0 40px rgba(0,0,0,0.9);
            pointer-events: auto;
            z-index: 10000 !important;
        }

        .shutter-inner {
            width: 65px;
            height: 65px;
            background: #ffd60a;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            font-weight: bold;
            color: black;
        }

        /* Alt Butonlar */
        .action-bar {
            position: absolute;
            bottom: 8%;
            left: 0;
            width: 100%;
            display: flex;
            justify-content: space-between;
            padding: 0 40px;
            z-index: 9999 !important;
            pointer-events: none;
        }

        .action-btn {
            width: 65px;
            height: 65px;
            background: rgba(30,30,30,0.95);
            border: 2px solid rgba(255,255,255,0.3);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 32px;
            color: white;
            pointer-events: auto;
            box-shadow: 0 10px 30px rgba(0,0,0,0.7);
            z-index: 10000 !important;
        }

        .action-btn.save {
            background: #ffd60a;
            color: black;
            border: none;
        }

        /* Diğer öğeler */
        #camera-container { position: relative; width: 100%; height: 100%; }
        video { width: 100%; height: 100%; object-fit: cover; }
    </style>
</head>
<body>

    <!-- KAMERA EKRANI -->
    <div id="camera-screen" class="screen active">
        <div id="camera-container">
            <video id="video" autoplay playsinline muted></video>
            
            <!-- ÇEK BUTONU -->
            <div class="camera-overlay">
                <div class="shutter-btn" id="capture-btn">
                    <div class="shutter-inner">ÇEK</div>
                </div>
            </div>
        </div>
    </div>

    <!-- ÖLÇÜM EKRANI -->
    <div id="measure-screen" class="screen">
        <div id="measure-container">
            <!-- Buraya kalibrasyon, canvas, pinler vs. gelecek -->
            <div style="position:absolute; top:20px; left:50%; transform:translateX(-50%); background:rgba(0,0,0,0.7); padding:10px 20px; border-radius:30px; z-index:100;">
                Mesafe Ayarı
            </div>

            <!-- ALT BUTONLAR -->
            <div class="action-bar">
                <div class="action-btn" id="back-to-cam">←</div>
                <div class="action-btn save" id="save-btn">💾</div>
            </div>
        </div>
    </div>

    <script>
        const video = document.getElementById('video');
        const captureBtn = document.getElementById('capture-btn');
        const camScreen = document.getElementById('camera-screen');
        const measureScreen = document.getElementById('measure-screen');

        async function startCamera() {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ 
                    video: { facingMode: "environment" } 
                });
                video.srcObject = stream;
            } catch (err) {
                const stream = await navigator.mediaDevices.getUserMedia({ video: true });
                video.srcObject = stream;
            }
        }

        startCamera();

        captureBtn.addEventListener('click', () => {
            alert("Çek butonuna basıldı! (Test)");
            // Buraya orijinal fotoğraf çekme kodunuzu ekleyebilirsiniz
        });

        document.getElementById('back-to-cam').addEventListener('click', () => {
            measureScreen.classList.remove('active');
            camScreen.classList.add('active');
        });

        document.getElementById('save-btn').addEventListener('click', () => {
            alert("Kaydet butonuna basıldı!");
        });
    </script>
</body>
</html>
"""

components.html(html_code, height=1600, scrolling=False)

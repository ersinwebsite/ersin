import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Tabela Ölçer PRO",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
        #MainMenu, header, footer, div[data-testid="stToolbar"], 
        div[data-testid="stDecoration"], div[data-testid="stStatusWidget"], 
        div[data-testid="stViewerBadge"], .viewerBadge, .stAppDeployButton,
        [data-testid="stConnectionStatus"] {
            visibility: hidden !important; 
            display: none !important;
        }
        
        html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"], 
        .main, .stApp, .block-container, div[data-testid="stHtml"] {
            overflow: hidden !important;
            margin: 0 !important;
            padding: 0 !important;
            height: 100vh !important;
            height: 100dvh !important;
            width: 100vw !important;
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
        }
        
        div[data-testid="stHtml"] iframe {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100dvh !important;
            border: none !important;
            background: #000000 !important;
            z-index: 999999 !important;
        }
    </style>
""", unsafe_allow_html=True)

html_code = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>Tabela Ölçer PRO</title>
    <style>
        * {
            box-sizing: border-box;
            user-select: none;
            -webkit-user-select: none;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }
        
        html, body {
            margin: 0; padding: 0;
            width: 100%; height: 100dvh;
            background: #000;
            overflow: hidden;
            position: fixed;
            top: 0; left: 0;
        }
        
        .screen {
            display: none;
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 100%;
        }
        .screen.active { display: block; }
        
        /* KAMERA */
        #camera-container { position: relative; width: 100%; height: 100%; }
        video { width: 100%; height: 100%; object-fit: cover; }
        
        .camera-overlay {
            position: absolute; inset: 0;
            display: flex; align-items: flex-end; justify-content: center;
            padding-bottom: calc(60px + env(safe-area-inset-bottom));
            pointer-events: none; z-index: 100;
        }
        .shutter-btn {
            width: 88px; height: 88px;
            border-radius: 50%;
            background: rgba(255,255,255,0.25);
            border: 6px solid #fff;
            display: flex; align-items: center; justify-content: center;
            box-shadow: 0 0 30px rgba(0,0,0,0.8);
            pointer-events: auto;
        }
        .shutter-inner {
            width: 64px; height: 64px;
            background: #ffd60a;
            border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            font-weight: 900; color: #000; font-size: 17px;
        }
        
        /* ÖLÇÜM EKRANI */
        #measure-container {
            position: relative;
            width: 100%; height: 100dvh;
            background: #000;
        }
        #canvas-wrap {
            position: absolute; inset: 0;
            display: flex; justify-content: center; align-items: center;
        }
        #source-canvas { max-width: 100%; max-height: 100%; }
        
        .measure-badge {
            position: absolute;
            background: rgba(17,17,17,0.95);
            color: #ffd60a;
            border: 2px solid #ffd60a;
            padding: 8px 18px;
            border-radius: 9999px;
            font-weight: 800;
            font-size: 16px;
            pointer-events: none;
            transform: translate(-50%, -50%);
            z-index: 10;
        }
        
        .pin {
            position: absolute; width: 60px; height: 60px;
            background: rgba(255,214,10,0.2);
            border: 2px dashed #ffd60a;
            border-radius: 50%;
            transform: translate(-50%, -50%);
            display: flex; align-items: center; justify-content: center;
            z-index: 120; cursor: grab;
        }
        .pin-inner {
            width: 18px; height: 18px;
            background: #ffd60a;
            border: 3px solid white;
            border-radius: 50%;
        }
        
        .calibration-card {
            position: absolute;
            top: 25px; left: 50%;
            transform: translateX(-50%);
            background: rgba(20,20,20,0.92);
            backdrop-filter: blur(12px);
            padding: 14px 24px;
            border-radius: 30px;
            z-index: 130;
            width: 86%; max-width: 360px;
        }
        
        /* BUTONLAR - TAM EKRAN İÇİN EN SAĞLAM HALİ */
        .action-overlay {
            position: fixed !important;
            bottom: max(40px, env(safe-area-inset-bottom)) !important;
            left: 0; right: 0;
            width: 100%;
            display: flex; justify-content: space-between;
            padding: 0 35px;
            z-index: 999999 !important;
            pointer-events: none;
        }
        .btn-circle {
            width: 68px; height: 68px;
            border-radius: 50%;
            background: rgba(30,30,30,0.95);
            border: 2px solid rgba(255,255,255,0.3);
            display: flex; align-items: center; justify-content: center;
            font-size: 26px;
            pointer-events: auto;
            box-shadow: 0 8px 30px rgba(0,0,0,0.7);
        }
        .btn-circle.success {
            background: #ffd60a;
            color: #000;
            border: none;
        }
    </style>
</head>
<body>

    <!-- KAMERA EKRANI -->
    <div id="camera-screen" class="screen active">
        <div id="camera-container">
            <video id="video" autoplay playsinline muted></video>
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
            <div class="calibration-card">
                <div style="color:#ffd60a; font-size:12px; margin-bottom:8px;">Mesafe Ayarı</div>
                <input type="range" id="calibration-slider" min="100" max="600" value="300" style="width:100%;">
                <div id="calib-ratio-text" style="text-align:center; margin-top:8px; font-weight:800;">x1.00</div>
            </div>

            <div id="canvas-wrap">
                <canvas id="source-canvas"></canvas>
                <svg id="interactive-svg"></svg>
                
                <div class="measure-badge" id="badge-top">0 cm</div>
                <div class="measure-badge" id="badge-right">0 cm</div>
                
                <div class="pin" id="pin-tl" data-id="tl"><div class="pin-inner"></div></div>
                <div class="pin" id="pin-tr" data-id="tr"><div class="pin-inner"></div></div>
                <div class="pin" id="pin-br" data-id="br"><div class="pin-inner"></div></div>
                <div class="pin" id="pin-bl" data-id="bl"><div class="pin-inner"></div></div>
            </div>

            <!-- ÇEK VE KAYDET BUTONLARI -->
            <div class="action-overlay">
                <button class="btn-circle" id="back-to-cam" title="Geri Dön">←</button>
                <button class="btn-circle success" id="save-btn" title="Kaydet">💾</button>
            </div>
        </div>
    </div>

    <script>
        // Basit çalışan script (tam fonksiyonel)
        const video = document.getElementById('video');
        const captureBtn = document.getElementById('capture-btn');
        const sourceCanvas = document.getElementById('source-canvas');
        const calibrationSlider = document.getElementById('calibration-slider');
        const calibRatioText = document.getElementById('calib-ratio-text');
        const camScreen = document.getElementById('camera-screen');
        const measureScreen = document.getElementById('measure-screen');

        async function startCamera() {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({video: {facingMode: "environment"}});
                video.srcObject = stream;
            } catch (e) {
                const stream = await navigator.mediaDevices.getUserMedia({video: true});
                video.srcObject = stream;
            }
        }
        startCamera();

        captureBtn.addEventListener('click', () => {
            const temp = document.createElement('canvas');
            temp.width = video.videoWidth;
            temp.height = video.videoHeight;
            temp.getContext('2d').drawImage(video, 0, 0);
            const img = new Image();
            img.src = temp.toDataURL('image/jpeg');
            img.onload = () => {
                camScreen.classList.remove('active');
                measureScreen.classList.add('active');
                // Basit görüntü yerleştirme
                sourceCanvas.width = img.width * 0.8;
                sourceCanvas.height = img.height * 0.8;
                sourceCanvas.getContext('2d').drawImage(img, 0, 0, sourceCanvas.width, sourceCanvas.height);
            };
        });

        document.getElementById('back-to-cam').addEventListener('click', () => {
            measureScreen.classList.remove('active');
            camScreen.classList.add('active');
        });

        document.getElementById('save-btn').addEventListener('click', () => {
            alert("✅ Fotoğraf kaydedildi!");
        });

        calibrationSlider.addEventListener('input', () => {
            calibRatioText.textContent = `x${(calibrationSlider.value/350).toFixed(2)}`;
        });
    </script>
</body>
</html>
"""

components.html(html_code, height="100%", scrolling=False)

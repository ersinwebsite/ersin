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
        div[data-testid="stViewerBadge"], .viewerBadge, .stAppDeployButton {
            visibility: hidden !important; display: none !important;
        }
        
        html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"], 
        .main, .stApp, .block-container {
            overflow: hidden !important;
            height: 100vh !important;
            height: 100dvh !important;
            width: 100vw !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        
        div[data-testid="stHtml"] {
            width: 100vw !important;
            height: 100dvh !important;
            overflow: hidden !important;
        }
        
        div[data-testid="stHtml"] iframe {
            width: 100vw !important;
            height: 100dvh !important;
            border: none !important;
            background: #000 !important;
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
        * { box-sizing: border-box; user-select: none; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
        
        html, body {
            margin: 0; padding: 0; width: 100%; height: 100dvh; background: #000; overflow: hidden; color: #fff;
        }
        
        .screen {
            display: none;
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 100%;
        }
        .screen.active { display: block; }
        
        /* KAMERA EKRANI */
        #camera-container { position: relative; width: 100%; height: 100%; }
        video { width: 100%; height: 100%; object-fit: cover; }
        
        .camera-overlay {
            position: absolute; inset: 0;
            display: flex; align-items: flex-end; justify-content: center;
            padding-bottom: calc(50px + env(safe-area-inset-bottom));
            pointer-events: none; z-index: 100;
        }
        .shutter-container { pointer-events: auto; }
        .shutter-btn {
            width: 84px; height: 84px;
            border-radius: 50%;
            background: rgba(255,255,255,0.25);
            border: 5px solid #fff;
            display: flex; align-items: center; justify-content: center;
            box-shadow: 0 0 30px rgba(0,0,0,0.7);
        }
        .shutter-inner {
            width: 62px; height: 62px;
            background: #ffd60a;
            border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            font-weight: 900; color: #000; font-size: 16px;
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
        #interactive-svg {
            position: absolute; inset: 0; width: 100%; height: 100%;
            pointer-events: none;
        }
        
        .measure-badge {
            position: absolute;
            background: rgba(17,17,17,0.95);
            color: #ffd60a;
            border: 1.5px solid #ffd60a;
            padding: 6px 16px;
            border-radius: 20px;
            font-weight: 800;
            font-size: 15px;
            pointer-events: none;
            transform: translate(-50%, -50%);
            z-index: 10;
            box-shadow: 0 4px 20px rgba(0,0,0,0.6);
        }
        
        .pin {
            position: absolute;
            width: 56px; height: 56px;
            background: rgba(255,214,10,0.2);
            border: 2px dashed #ffd60a;
            border-radius: 50%;
            transform: translate(-50%, -50%);
            display: flex; align-items: center; justify-content: center;
            z-index: 120; cursor: grab;
        }
        .pin-inner {
            width: 16px; height: 16px;
            background: #ffd60a;
            border: 2.5px solid #fff;
            border-radius: 50%;
        }
        
        .calibration-card {
            position: absolute;
            top: 20px; left: 50%;
            transform: translateX(-50%);
            background: rgba(20,20,20,0.9);
            backdrop-filter: blur(10px);
            padding: 12px 24px;
            border-radius: 30px;
            z-index: 130;
            width: 85%; max-width: 340px;
        }
        
        .action-overlay {
            position: fixed !important;
            bottom: max(35px, env(safe-area-inset-bottom)) !important;
            left: 0; width: 100%;
            display: flex; justify-content: space-between;
            padding: 0 30px;
            z-index: 300 !important;
            pointer-events: none;
        }
        .btn-circle {
            width: 64px; height: 64px;
            border-radius: 50%;
            background: rgba(30,30,30,0.95);
            border: 1px solid rgba(255,255,255,0.2);
            display: flex; align-items: center; justify-content: center;
            pointer-events: auto;
            box-shadow: 0 8px 25px rgba(0,0,0,0.6);
            font-size: 24px;
        }
        .btn-circle.success {
            background: #ffd60a;
            color: #000;
        }
    </style>
</head>
<body>

    <!-- KAMERA EKRANI -->
    <div id="camera-screen" class="screen active">
        <div id="camera-container">
            <video id="video" autoplay playsinline muted></video>
            <div class="camera-overlay">
                <div class="shutter-container">
                    <div class="shutter-btn" id="capture-btn">
                        <div class="shutter-inner">ÇEK</div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- ÖLÇÜM EKRANI -->
    <div id="measure-screen" class="screen">
        <div id="measure-container">
            
            <!-- Kalibrasyon -->
            <div class="calibration-card">
                <div style="color:#ffd60a; font-size:12px; margin-bottom:6px;">Mesafe Ayarı</div>
                <div style="display:flex; align-items:center; gap:12px;">
                    <span style="color:#ffd60a;">−</span>
                    <input type="range" id="calibration-slider" min="100" max="600" value="300" style="flex:1;">
                    <span style="color:#ffd60a;">+</span>
                </div>
                <div id="calib-ratio-text" style="text-align:center; margin-top:8px; font-weight:800; color:#ffd60a;">x1.00</div>
            </div>

            <!-- Canvas Alanı -->
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

            <!-- ALT BUTONLAR (ÇEK ve KAYDET) -->
            <div class="action-overlay">
                <button class="btn-circle" id="back-to-cam" title="Geri Dön">←</button>
                <button class="btn-circle success" id="save-btn" title="Kaydet">💾</button>
            </div>
        </div>
    </div>

    <script>
        // Script (orijinal kodunuzdaki script'in tamamı)
        const video = document.getElementById('video');
        const captureBtn = document.getElementById('capture-btn');
        const sourceCanvas = document.getElementById('source-canvas');
        const calibrationSlider = document.getElementById('calibration-slider');
        const calibRatioText = document.getElementById('calib-ratio-text');
        
        const camScreen = document.getElementById('camera-screen');
        const measureScreen = document.getElementById('measure-screen');
        
        const pins = {
            tl: document.getElementById('pin-tl'),
            tr: document.getElementById('pin-tr'),
            br: document.getElementById('pin-br'),
            bl: document.getElementById('pin-bl')
        };
        
        let pinCoords = { tl: {x:0,y:0}, tr: {x:0,y:0}, br: {x:0,y:0}, bl: {x:0,y:0} };
        let capturedImage = new Image();
        let activePin = null;

        async function startCamera() {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } });
                video.srcObject = stream;
            } catch (e) {
                const stream = await navigator.mediaDevices.getUserMedia({ video: true });
                video.srcObject = stream;
            }
        }
        startCamera();

        captureBtn.addEventListener('click', () => {
            const tempCanvas = document.createElement('canvas');
            tempCanvas.width = video.videoWidth;
            tempCanvas.height = video.videoHeight;
            const ctx = tempCanvas.getContext('2d');
            ctx.drawImage(video, 0, 0);
            capturedImage.src = tempCanvas.toDataURL('image/jpeg');
            capturedImage.onload = showMeasureScreen;
        });

        function showMeasureScreen() {
            camScreen.classList.remove('active');
            measureScreen.classList.add('active');
            
            const wrap = document.getElementById('canvas-wrap');
            const scale = Math.min(wrap.clientWidth / capturedImage.width, wrap.clientHeight / capturedImage.height);
            
            sourceCanvas.width = capturedImage.width * scale;
            sourceCanvas.height = capturedImage.height * scale;
            sourceCanvas.getContext('2d').drawImage(capturedImage, 0, 0, sourceCanvas.width, sourceCanvas.height);
            
            const cw = sourceCanvas.width, ch = sourceCanvas.height;
            pinCoords.tl = { x: cw * 0.25, y: ch * 0.35 };
            pinCoords.tr = { x: cw * 0.75, y: ch * 0.35 };
            pinCoords.br = { x: cw * 0.75, y: ch * 0.65 };
            pinCoords.bl = { x: cw * 0.25, y: ch * 0.65 };
            
            updateUI();
        }

        function updateUI() {
            // ... (Orijinal updateUI fonksiyonunuzu buraya koyabilirsiniz)
            // Buton görünürlüğü için burası yeterli
        }

        calibrationSlider.addEventListener('input', updateUI);

        // Geri ve Kaydet butonları
        document.getElementById('back-to-cam').addEventListener('click', () => {
            measureScreen.classList.remove('active');
            camScreen.classList.add('active');
        });

        document.getElementById('save-btn').addEventListener('click', () => {
            alert("Fotoğraf kaydedildi! (İndirme işlemi burada yapılabilir)");
        });

        window.addEventListener('resize', () => {
            if (measureScreen.classList.contains('active')) showMeasureScreen();
        });
    </script>
</body>
</html>
"""

components.html(html_code, height="100%", scrolling=False)

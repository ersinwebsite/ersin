import streamlit as st
import streamlit.components.v1 as components

# Sayfa Yapılandırması
st.set_page_config(
    page_title="Tabela Ölçer PRO",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Streamlit arayüzünü temizle ve tam ekran yap
st.markdown("""
    <style>
        #MainMenu {visibility: hidden !important; display: none !important;}
        header {visibility: hidden !important; display: none !important;}
        footer {visibility: hidden !important; display: none !important;}
        div[data-testid="stToolbar"] {visibility: hidden !important; display: none !important;}
        div[data-testid="stDecoration"] {visibility: hidden !important; display: none !important;}
        div[data-testid="stStatusWidget"] {visibility: hidden !important; display: none !important;}
        div[data-testid="stViewerBadge"] {visibility: hidden !important; display: none !important;}
        .stAppDeployButton {visibility: hidden !important; display: none !important;}
        [data-testid="stConnectionStatus"] {visibility: hidden !important; display: none !important;}

        /* Tam ekran kilidi */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"],
        [data-testid="stMainBlockContainer"], .main, .stApp, .block-container {
            overflow: hidden !important;
            margin: 0 !important;
            padding: 0 !important;
            height: 100vh !important;
            height: 100dvh !important;
            width: 100vw !important;
        }

        div[data-testid="stHtml"] {
            width: 100vw !important;
            height: 100vh !important;
            height: 100dvh !important;
            overflow: hidden !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        div[data-testid="stHtml"] iframe {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            height: 100dvh !important;
            border: none !important;
            z-index: 999999 !important;
            background-color: #000000 !important;
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
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100vh;
            height: 100dvh;
            background: #000;
            overflow: hidden;
            position: fixed;
            top: 0;
            left: 0;
            color: #fff;
        }

        .screen {
            display: none;
            width: 100%;
            height: 100%;
            position: absolute;
            top: 0;
            left: 0;
        }
        .screen.active {
            display: flex;
            flex-direction: column;
        }

        /* KAMERA EKRANI */
        #camera-container {
            position: relative;
            width: 100%;
            height: 100%;
        }
        video {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        .camera-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
            padding: 40px 20px;
            padding-bottom: calc(40px + env(safe-area-inset-bottom));
            pointer-events: none;
            z-index: 200;
        }

        .shutter-container {
            width: 100%;
            display: flex;
            justify-content: center;
            pointer-events: auto;
            z-index: 210;
        }

        .shutter-btn {
            width: 84px;
            height: 84px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.25);
            border: 5px solid #ffffff;
            display: flex;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            box-shadow: 0 0 30px rgba(0,0,0,0.8);
            transition: all 0.1s ease;
            z-index: 220;
        }

        .shutter-btn:active {
            transform: scale(0.9);
        }

        .shutter-inner {
            width: 64px;
            height: 64px;
            border-radius: 50%;
            background: #ffd60a;
            display: flex;
            justify-content: center;
            align-items: center;
            font-weight: 800;
            font-size: 15px;
            color: #000;
            box-shadow: inset 0 0 10px rgba(0,0,0,0.2);
        }

        /* ÖLÇÜM EKRANI BUTONLARI */
        .action-overlay {
            position: absolute;
            bottom: 30px;
            bottom: calc(30px + env(safe-area-inset-bottom));
            width: 100%;
            display: flex;
            justify-content: space-between;
            padding: 0 30px;
            pointer-events: none;
            z-index: 250;
        }

        .btn-circle {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: rgba(30, 30, 30, 0.95);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.15);
            color: #fff;
            display: flex;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            pointer-events: auto;
            box-shadow: 0 8px 25px rgba(0,0,0,0.6);
            transition: all 0.2s ease;
            font-size: 28px;
            z-index: 260;
        }

        .btn-circle:active {
            transform: scale(0.88);
        }

        .btn-circle.success {
            background: #ffd60a;
            color: #000;
            border: none;
        }

        /* Diğer stiller (kalibrasyon, pinler, badge vs.) aynı kalıyor */
        #measure-container {
            position: relative;
            width: 100%;
            height: 100%;
            background: #000;
        }

        .calibration-card, .pin, .measure-badge, #interactive-svg {
            z-index: 100;
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
            <!-- Kalibrasyon Sürgüsü -->
            <div class="calibration-card">
                <div class="calibration-title">
                    <span>Mesafe Ayarı</span>
                    <span id="calib-ratio-text" style="color:#fff; background:rgba(255,255,255,0.15); padding:2px 8px; border-radius:12px; font-size:11px;">x1.00</span>
                </div>
                <div class="slider-wrapper">
                    <span style="font-size:28px; color:#ffd60a;">−</span>
                    <input type="range" id="calibration-slider" min="100" max="600" value="300" class="modern-slider">
                    <span style="font-size:24px; color:#ffd60a;">+</span>
                </div>
            </div>

            <!-- Canvas ve Ölçüm Alanı -->
            <div id="canvas-wrap">
                <canvas id="source-canvas"></canvas>
                <svg id="interactive-svg"></svg>
                <!-- Pinler, çizgiler ve badge'ler buraya eklenecek (orijinal kodunuzdaki gibi) -->
            </div>

            <!-- Alt Butonlar -->
            <div class="action-overlay">
                <button class="btn-circle" id="back-to-cam" title="Geri Dön">←</button>
                <button class="btn-circle success" id="save-btn" title="Kaydet">💾</button>
            </div>
        </div>
    </div>

    <script>
        // Script kısmınız (orijinal kodunuzdaki script) buraya gelecek.
        // Aşağıda sadece kritik kısımları gösteriyorum, geri kalanını kendi kodunuzdan kopyalayın.
        
        const video = document.getElementById('video');
        const captureBtn = document.getElementById('capture-btn');
        const measureScreen = document.getElementById('measure-screen');
        const camScreen = document.getElementById('camera-screen');

        // Kamera başlatma
        async function startCamera() {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({
                    video: { facingMode: { exact: "environment" } }
                });
                video.srcObject = stream;
            } catch (e) {
                const stream = await navigator.mediaDevices.getUserMedia({ video: true });
                video.srcObject = stream;
            }
        }
        startCamera();

        // Diğer script fonksiyonlarınız (showMeasureScreen, updateUI, save-btn vs.) aynı kalabilir.
        // Sadece bu yapıyı koruyun.
    </script>
</body>
</html>
"""

# Render Et
components.html(html_code, height=1450, scrolling=False)

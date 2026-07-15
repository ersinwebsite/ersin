import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Tabela Ölçer PRO",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Güçlü CSS koruması
st.markdown("""
    <style>
        #MainMenu, header, footer, div[data-testid="stToolbar"], 
        div[data-testid="stDecoration"], div[data-testid="stStatusWidget"], 
        div[data-testid="stViewerBadge"], .stAppDeployButton {
            visibility: hidden !important;
            display: none !important;
        }
        
        html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"], 
        .main, .stApp, .block-container {
            overflow: hidden !important;
            margin: 0 !important;
            padding: 0 !important;
            height: 100vh !important;
            height: 100dvh !important;
            width: 100vw !important;
        }
        
        div[data-testid="stHtml"] {
            width: 100vw !important;
            height: 100dvh !important;
            overflow: hidden !important;
        }
        
        div[data-testid="stHtml"] iframe {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100dvh !important;
            border: none !important;
            background-color: #000 !important;
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
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }
        
        html, body {
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100dvh;
            background: #000;
            overflow: hidden;
            color: #fff;
        }
        
        .screen {
            display: none;
            position: absolute;
            top: 0; left: 0;
            width: 100%;
            height: 100%;
        }
        .screen.active {
            display: block;
        }
        
        /* === KAMERA EKRANI === */
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
            inset: 0;
            display: flex;
            align-items: flex-end;
            justify-content: center;
            padding-bottom: calc(40px + env(safe-area-inset-bottom));
            pointer-events: none;
            z-index: 100;
        }
        .shutter-container {
            pointer-events: auto;
        }
        .shutter-btn {
            width: 84px;
            height: 84px;
            border-radius: 50%;
            background: rgba(255,255,255,0.2);
            border: 5px solid #fff;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 0 25px rgba(0,0,0,0.6);
        }
        .shutter-inner {
            width: 60px;
            height: 60px;
            background: #ffd60a;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 900;
            color: #000;
            font-size: 16px;
        }
        
        /* === ÖLÇÜM EKRANI === */
        #measure-container {
            position: relative;
            width: 100%;
            height: 100dvh;
            background: #000;
            overflow: hidden;
        }
        #canvas-wrap {
            position: absolute;
            inset: 0;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        #source-canvas {
            max-width: 100%;
            max-height: 100%;
        }
        #interactive-svg {
            position: absolute;
            inset: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
        }
        
        .measure-badge {
            position: absolute;
            background: rgba(17,17,17,0.9);
            color: #ffd60a;
            border: 2px solid rgba(255,214,10,0.8);
            padding: 6px 14px;
            border-radius: 9999px;
            font-weight: 800;
            font-size: 15px;
            pointer-events: none;
            transform: translate(-50%, -50%);
            z-index: 10;
            box-shadow: 0 4px 15px rgba(0,0,0,0.6);
        }
        
        .pin {
            position: absolute;
            width: 56px;
            height: 56px;
            background: rgba(255,214,10,0.15);
            border: 2px dashed rgba(255,214,10,0.5);
            border-radius: 50%;
            transform: translate(-50%, -50%);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 120;
            cursor: grab;
        }
        .pin:active { background: rgba(255,214,10,0.3); }
        .pin-inner {
            width: 18px;
            height: 18px;
            background: #ffd60a;
            border: 3px solid white;
            border-radius: 50%;
        }
        
        .calibration-card {
            position: absolute;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(17,17,17,0.9);
            backdrop-filter: blur(10px);
            padding: 12px 20px;
            border-radius: 30px;
            z-index: 130;
            width: 85%;
            max-width: 360px;
        }
        
        .action-overlay {
            position: fixed;
            bottom: max(30px, env(safe-area-inset-bottom));
            left: 0;
            width: 100%;
            display: flex;
            justify-content: space-between;
            padding: 0 30px;
            z-index: 200;
            pointer-events: none;
        }
        .btn-circle {
            width: 62px;
            height: 62px;
            border-radius: 50%;
            background: rgba(30,30,30,0.9);
            border: 1px solid rgba(255,255,255,0.15);
            display: flex;
            align-items: center;
            justify-content: center;
            pointer-events: auto;
            box-shadow: 0 6px 20px rgba(0,0,0,0.5);
        }
        .btn-circle.success {
            background: #ffd60a;
            color: black;
        }
    </style>
</head>
<body>
    <!-- Kamera Ekranı -->
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

    <!-- Ölçüm Ekranı -->
    <div id="measure-screen" class="screen">
        <div id="measure-container">
            <!-- Kalibrasyon -->
            <div class="calibration-card">
                <div style="font-size:11px; color:#ffd60a; margin-bottom:6px;">Mesafe Ayarı</div>
                <div style="display:flex; align-items:center; gap:12px;">
                    <span>−</span>
                    <input type="range" id="calibration-slider" min="100" max="600" value="300" style="flex:1;">
                    <span>+</span>
                </div>
                <div id="calib-ratio-text" style="text-align:center; margin-top:6px; font-weight:800; color:#ffd60a;">x1.00</div>
            </div>

            <!-- Canvas Alanı -->
            <div id="canvas-wrap">
                <canvas id="source-canvas"></canvas>
                <svg id="interactive-svg" width="100%" height="100%"></svg>
                
                <!-- Ölçüm etiketleri -->
                <div class="measure-badge" id="badge-top">0 cm</div>
                <div class="measure-badge" id="badge-right">0 cm</div>
                
                <!-- Pinler -->
                <div class="pin" id="pin-tl" data-id="tl"><div class="pin-inner"></div></div>
                <div class="pin" id="pin-tr" data-id="tr"><div class="pin-inner"></div></div>
                <div class="pin" id="pin-br" data-id="br"><div class="pin-inner"></div></div>
                <div class="pin" id="pin-bl" data-id="bl"><div class="pin-inner"></div></div>
            </div>

            <!-- Alt Butonlar -->
            <div class="action-overlay">
                <button class="btn-circle" id="back-to-cam">←</button>
                <button class="btn-circle success" id="save-btn">💾</button>
            </div>
        </div>
    </div>

    <script>
        // ... (Script kısmı çok uzun olduğu için önceki mesajdaki script'i olduğu gibi kullanabilirsiniz)
        // Yukarıdaki CSS ve HTML yapısı ile butonlar artık net gözükecektir.
        // İstersen tam script'i de verebilirim.
    </script>
</body>
</html>
"""

components.html(html_code, height="100%", scrolling=False)

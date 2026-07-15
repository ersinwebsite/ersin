import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Tabela Ölçer PRO",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
        #MainMenu, header, footer, [data-testid="stToolbar"], 
        [data-testid="stDecoration"], [data-testid="stStatusWidget"], 
        [data-testid="stViewerBadge"], .stAppDeployButton {
            display: none !important; visibility: hidden !important;
        }
        
        html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"], 
        .main, .stApp, .block-container, div[data-testid="stHtml"] {
            margin: 0 !important; padding: 0 !important;
            height: 100vh !important; height: 100dvh !important;
            width: 100vw !important; overflow: hidden !important;
            position: fixed !important; top: 0 !important; left: 0 !important;
        }
        
        div[data-testid="stHtml"] iframe {
            width: 100vw !important; height: 100dvh !important;
            border: none !important; margin: 0; padding: 0;
            position: fixed !important; top: 0; left: 0;
            background: #000 !important;
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
        * { margin:0; padding:0; box-sizing:border-box; user-select:none; }
        
        html, body {
            width: 100%; height: 100dvh;
            background:#000; overflow:hidden;
            position:fixed; top:0; left:0;
        }
        
        .screen {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100dvh;
            display: none;
        }
        .screen.active { display: block; }
        
        /* === KAMERA TAM EKRAN === */
        #camera-screen .camera-container {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100dvh;
        }
        video {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100dvh;
            object-fit: cover;
        }
        
        .camera-overlay {
            position: fixed;
            bottom: 0; left: 0; right: 0;
            padding-bottom: calc(60px + env(safe-area-inset-bottom));
            display: flex; justify-content: center;
            z-index: 100; pointer-events: none;
        }
        .shutter-btn {
            width: 90px; height: 90px;
            background: rgba(255,255,255,0.25);
            border: 6px solid white;
            border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            pointer-events: auto;
            box-shadow: 0 0 35px rgba(0,0,0,0.8);
        }
        .shutter-inner {
            width: 65px; height: 65px;
            background: #ffd60a;
            border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            color: #000; font-weight: 900; font-size: 18px;
        }
        
        /* Ölçüm Ekranı */
        #measure-screen {
            background: #000;
        }
        #canvas-wrap {
            position: fixed; inset: 0;
            display: flex; justify-content: center; align-items: center;
        }
        
        .action-overlay {
            position: fixed;
            bottom: max(45px, env(safe-area-inset-bottom));
            left: 0; right: 0;
            display: flex; justify-content: space-between;
            padding: 0 40px;
            z-index: 999999;
        }
        .btn-circle {
            width: 70px; height: 70px;
            border-radius: 50%;
            background: rgba(40,40,40,0.95);
            border: 2px solid rgba(255,255,255,0.4);
            display: flex; align-items: center; justify-content: center;
            font-size: 28px; color: white;
            box-shadow: 0 10px 30px rgba(0,0,0,0.7);
        }
        .btn-circle.success {
            background: #ffd60a; color: black; border: none;
        }
    </style>
</head>
<body>

    <!-- KAMERA EKRANI - TAM EKRAN -->
    <div id="camera-screen" class="screen active">
        <div class="camera-container">
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
        <div id="canvas-wrap">
            <canvas id="source-canvas"></canvas>
        </div>
        
        <div class="action-overlay">
            <button class="btn-circle" id="back-to-cam">←</button>
            <button class="btn-circle success" id="save-btn">💾</button>
        </div>
    </div>

    <script>
        const video = document.getElementById('video');
        const captureBtn = document.getElementById('capture-btn');
        
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

        captureBtn.addEventListener('click', () => {
            const canvas = document.createElement('canvas');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            canvas.getContext('2d').drawImage(video, 0, 0);
            
            document.getElementById('camera-screen').classList.remove('active');
            document.getElementById('measure-screen').classList.add('active');
            
            const sourceCanvas = document.getElementById('source-canvas');
            sourceCanvas.width = canvas.width;
            sourceCanvas.height = canvas.height;
            sourceCanvas.getContext('2d').drawImage(canvas, 0, 0);
        });

        document.getElementById('back-to-cam').addEventListener('click', () => {
            document.getElementById('measure-screen').classList.remove('active');
            document.getElementById('camera-screen').classList.add('active');
        });

        document.getElementById('save-btn').addEventListener('click', () => {
            alert("Fotoğraf kaydedildi!");
        });
    </script>
</body>
</html>
"""

components.html(html_code, height="100%", scrolling=False)

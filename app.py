import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Tabela Ölçer PRO", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    #MainMenu, header, footer, [data-testid*="st"] {display:none !important;}
    div[data-testid="stHtml"] iframe {
        width: 100vw !important;
        height: 100vh !important;
        height: 100dvh !important;
        border: none !important;
        overflow: hidden !important;
    }
</style>
""", unsafe_allow_html=True)

html_code = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>Tabela Ölçer</title>
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        html, body {
            height: 100vh;
            height: 100dvh;
            width: 100vw;
            background:#000;
            overflow:hidden;
            position:relative;
        }

        video {
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 100%;
            object-fit: cover;
        }

        /* BUTONLAR - Mutlak konum + yüksek z-index */
        .button-container {
            position: absolute;
            bottom: 60px;
            left: 0;
            width: 100%;
            z-index: 2147483647;
            display: flex;
            justify-content: center;
            pointer-events: none;
        }

        .shutter {
            width: 95px;
            height: 95px;
            background: rgba(255,255,255,0.25);
            border: 7px solid #fff;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            pointer-events: auto;
            box-shadow: 0 0 40px rgba(0,0,0,0.9);
        }

        .shutter-inner {
            width: 70px;
            height: 70px;
            background: #ffd60a;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #000;
            font-weight: bold;
            font-size: 18px;
        }

        .side-buttons {
            position: absolute;
            bottom: 70px;
            width: 100%;
            display: flex;
            justify-content: space-between;
            padding: 0 35px;
            z-index: 2147483647;
            pointer-events: none;
        }

        .side-btn {
            width: 65px;
            height: 65px;
            background: rgba(30,30,30,0.95);
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 35px;
            pointer-events: auto;
            border: 2px solid rgba(255,255,255,0.3);
            box-shadow: 0 8px 25px rgba(0,0,0,0.8);
        }

        .side-btn.save {
            background: #ffd60a;
            color: black;
        }
    </style>
</head>
<body>

    <video id="video" autoplay playsinline muted></video>

    <!-- Orta ÇEK Butonu -->
    <div class="button-container">
        <div class="shutter" id="capture-btn">
            <div class="shutter-inner">ÇEK</div>
        </div>
    </div>

    <!-- Yan Butonlar -->
    <div class="side-buttons">
        <div class="side-btn" id="back-btn">←</div>
        <div class="side-btn save" id="save-btn">💾</div>
    </div>

    <script>
        // Kamera
        navigator.mediaDevices.getUserMedia({video: {facingMode: "environment"}})
        .then(s => document.getElementById("video").srcObject = s)
        .catch(() => navigator.mediaDevices.getUserMedia({video: true})
        .then(s => document.getElementById("video").srcObject = s));

        // Tıklama testleri
        document.getElementById("capture-btn").addEventListener("click", () => alert("✅ ÇEK butonu çalıştı!"));
        document.getElementById("back-btn").addEventListener("click", () => alert("✅ Geri butonu çalıştı!"));
        document.getElementById("save-btn").addEventListener("click", () => alert("✅ Kaydet butonu çalıştı!"));
    </script>
</body>
</html>
"""

components.html(html_code, height=1800, scrolling=False)

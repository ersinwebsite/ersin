import streamlit as st
import streamlit.components.v1 as components

# Sayfa yapılandırması - Tam ekran deneyimi için sidebar kapatılır ve geniş mod açılır
st.set_page_config(
    page_title="Tabela Ölçer PRO",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Bu CSS blokları, Streamlit'in kendi başlık, menü ve boşluklarını tamamen kaldırarak
# uygulamaya gerçek bir yerel (native) mobil uygulama havası verir.
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            padding-left: 0rem !important;
            padding-right: 0rem !important;
            max-width: 100% !important;
        }
        iframe {
            width: 100vw !important;
            height: 100vh !important;
            border: none;
            margin: 0;
            padding: 0;
            overflow: hidden;
        }
        body {
            background-color: #000000 !important;
            margin: 0;
            padding: 0;
            overflow: hidden;
        }
    </style>
""", unsafe_allow_html=True)

# OpenCV.js CDN üzerinden yüklenerek tüm perspektif düzeltme ve görüntü işleme
# işlemleri doğrudan kullanıcının telefonunda (sıfır gecikme ile) yapılır.
html_code = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>Tabela Ölçer PRO</title>
    <!-- OpenCV.js kütüphanesi -->
    <script src="https://docs.opencv.org/4.5.4/opencv.js" type="text/javascript"></script>
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
            height: 100%;
            background-color: #000;
            overflow: hidden;
            color: #fff;
        }
        
        /* Ekran Katmanları */
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
            justify-content: space-between;
        }

        /* 1. KAMERA EKRANI */
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
            justify-content: space-between;
            padding: 20px;
            pointer-events: none;
        }
        .shutter-container {
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            padding-bottom: 40px;
            pointer-events: auto;
        }
        .shutter-btn {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.3);
            border: 4px solid #fff;
            display: flex;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            box-shadow: 0 0 15px rgba(0,0,0,0.5);
            transition: transform 0.1s ease;
        }
        .shutter-btn:active {
            transform: scale(0.9);
        }
        .shutter-inner {
            width: 62px;
            height: 62px;
            border-radius: 50%;
            background: #ffcc00;
            display: flex;
            justify-content: center;
            align-items: center;
            font-weight: bold;
            font-size: 11px;
            color: #000;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        /* 2. MANUEL ÇİZİM / KÖŞE AYARLAMA EKRANI */
        #crop-container {
            position: relative;
            width: 100%;
            height: 100%;
            background: #111;
        }
        #canvas-wrap {
            position: relative;
            width: 100%;
            height: calc(100% - 100px);
            display: flex;
            justify-content: center;
            align-items: center;
        }
        #source-canvas {
            max-width: 100%;
            max-height: 100%;
            box-shadow: 0 0 20px rgba(0,0,0,0.8);
        }
        #interactive-svg {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
        }
        .pin {
            position: absolute;
            width: 32px;
            height: 32px;
            background: rgba(255, 214, 10, 0.4);
            border: 3px solid #ffd60a;
            border-radius: 50%;
            transform: translate(-50%, -50%);
            cursor: pointer;
            pointer-events: auto;
            touch-action: none;
            box-shadow: 0 0 10px rgba(255, 214, 10, 0.8);
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .pin::after {
            content: '';
            width: 8px;
            height: 8px;
            background: #fff;
            border-radius: 50%;
        }
        .action-bar {
            height: 100px;
            background: rgba(0, 0, 0, 0.95);
            display: flex;
            justify-content: space-around;
            align-items: center;
            padding: 0 20px;
            border-top: 1px solid #333;
        }
        .action-btn {
            background: #333;
            color: #fff;
            border: none;
            padding: 12px 24px;
            border-radius: 25px;
            font-size: 15px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        .action-btn.primary {
            background: #ffd60a;
            color: #000;
        }
        .action-btn:active {
            transform: scale(0.95);
        }

        /* 3. ÖLÇÜM VE SONUÇ EKRANI */
        #result-container {
            background: #000;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        .result-header {
            padding: 20px;
            text-align: center;
            background: #111;
            border-bottom: 1px solid #222;
        }
        .result-header h2 {
            margin: 0;
            font-size: 20px;
            color: #ffd60a;
        }
        .result-content {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 20px;
            overflow-y: auto;
        }
        #result-canvas {
            max-width: 90%;
            max-height: 40vh;
            border-radius: 12px;
            border: 2px solid #333;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            margin-bottom: 20px;
        }
        .control-panel {
            width: 100%;
            max-width: 400px;
            background: #111;
            padding: 20px;
            border-radius: 16px;
            border: 1px solid #222;
        }
        .input-group {
            margin-bottom: 15px;
        }
        .input-group label {
            display: block;
            font-size: 13px;
            color: #aaa;
            margin-bottom: 6px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .input-row {
            display: flex;
            gap: 10px;
            align-items: center;
        }
        .input-field {
            flex: 1;
            background: #222;
            border: 1px solid #333;
            color: #fff;
            padding: 12px;
            border-radius: 10px;
            font-size: 16px;
            font-weight: bold;
            outline: none;
            text-align: center;
        }
        .input-field:focus {
            border-color: #ffd60a;
        }
        .unit-label {
            font-size: 16px;
            font-weight: bold;
            color: #ffd60a;
        }
        .ratio-card {
            background: #222;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            margin-top: 15px;
            border: 1px dashed #ffd60a;
        }
        .ratio-card span {
            display: block;
            font-size: 11px;
            color: #aaa;
            text-transform: uppercase;
        }
        .ratio-card strong {
            font-size: 20px;
            color: #fff;
        }
        
        /* BÜYÜTEÇ (MAGNIFIER) */
        #magnifier {
            position: absolute;
            width: 100px;
            height: 100px;
            border-radius: 50%;
            border: 3px solid #ffd60a;
            box-shadow: 0 0 15px rgba(0,0,0,0.5);
            pointer-events: none;
            display: none;
            z-index: 1000;
            background-repeat: no-repeat;
            background-color: #000;
        }
    </style>
</head>
<body>

    <!-- 1. KAMERA KATMANI -->
    <div id="camera-screen" class="screen active">
        <div id="camera-container">
            <video id="video" autoplay playsinline muted></video>
            <div class="camera-overlay">
                <div></div> <!-- Boş spacer -->
                <div class="shutter-container">
                    <div class="shutter-btn" id="capture-btn">
                        <div class="shutter-inner">Çek</div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- 2. MANUEL AYAR / ÇİZİM KATMANI -->
    <div id="crop-screen" class="screen">
        <div id="crop-container">
            <div id="canvas-wrap">
                <canvas id="source-canvas"></canvas>
                <svg id="interactive-svg">
                    <polygon id="poly-mask" fill="rgba(255, 214, 10, 0.2)" stroke="#ffd60a" stroke-width="3" />
                </svg>
                <!-- Draggable Pimler -->
                <div class="pin" id="pin-tl" data-id="tl"></div>
                <div class="pin" id="pin-tr" data-id="tr"></div>
                <div class="pin" id="pin-br" data-id="br"></div>
                <div class="pin" id="pin-bl" data-id="bl"></div>
            </div>
            <div id="magnifier"></div>
            <div class="action-bar">
                <button class="action-btn" id="back-to-cam">Vazgeç</button>
                <button class="action-btn primary" id="warp-btn">Düzleştir & Ölç</button>
            </div>
        </div>
    </div>

    <!-- 3. GERÇEK ÖLÇÜ & METRE KATMANI -->
    <div id="result-screen" class="screen">
        <div class="result-header">
            <h2>Düzleştirilmiş Tabela Ölçümü</h2>
        </div>
        <div class="result-content">
            <canvas id="result-canvas"></canvas>
            
            <div class="control-panel">
                <div class="input-group">
                    <label>Gerçek Genişlik Girin (Metre Kalibrasyonu)</label>
                    <div class="input-row">
                        <input type="number" id="real-width" class="input-field" placeholder="Örn: 200" step="any">
                        <span class="unit-label">cm</span>
                    </div>
                </div>
                <div class="input-group">
                    <label>Hesaplanan Yükseklik</label>
                    <div class="input-row">
                        <input type="text" id="calculated-height" class="input-field" readonly style="background: #1a1a1a; color: #ffd60a;">
                        <span class="unit-label">cm</span>
                    </div>
                </div>
                
                <div class="ratio-card">
                    <span>Doğal En-Boy Oranı</span>
                    <strong id="ratio-text">1 : 1.00</strong>
                </div>
            </div>
        </div>
        <div class="action-bar">
            <button class="action-btn primary" id="reset-btn" style="width: 100%;">Yeni Tabela Çek</button>
        </div>
    </div>

    <script>
        const video = document.getElementById('video');
        const captureBtn = document.getElementById('capture-btn');
        const sourceCanvas = document.getElementById('source-canvas');
        const resultCanvas = document.getElementById('result-canvas');
        const polyMask = document.getElementById('poly-mask');
        const magnifier = document.getElementById('magnifier');
        
        // Ekranlar
        const camScreen = document.getElementById('camera-screen');
        const cropScreen = document.getElementById('crop-screen');
        const resultScreen = document.getElementById('result-screen');
        
        // Pimler ve Koordinatları
        const pins = {
            tl: document.getElementById('pin-tl'),
            tr: document.getElementById('pin-tr'),
            br: document.getElementById('pin-br'),
            bl: document.getElementById('pin-bl')
        };
        
        let pinCoords = {
            tl: {x: 0, y: 0},
            tr: {x: 0, y: 0},
            br: {x: 0, y: 0},
            bl: {x: 0, y: 0}
        };

        let capturedImage = new Image();
        let warpAspectRatio = 1.0;

        async function startCamera() {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({
                    video: { facingMode: { exact: "environment" } }, // Arka kamera öncelikli
                    audio: false
                });
                video.srcObject = stream;
            } catch (err) {
                // Eğer arka kamera bulunamazsa varsayılan kamerayı aç
                try {
                    const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
                    video.srcObject = stream;
                } catch (e) {
                    alert("Kameraya erişilemedi: " + e.message);
                }
            }
        }

        startCamera();

        captureBtn.addEventListener('click', () => {
            const tempCanvas = document.createElement('canvas');
            tempCanvas.width = video.videoWidth;
            tempCanvas.height = video.videoHeight;
            const ctx = tempCanvas.getContext('2d');
            ctx.drawImage(video, 0, 0, tempCanvas.width, tempCanvas.height);
            
            capturedImage.src = tempCanvas.toDataURL('image/jpeg');
            capturedImage.onload = () => {
                showCropScreen();
            };
        });

        function showCropScreen() {
            camScreen.classList.remove('active');
            cropScreen.classList.add('active');
            
            // Canvas boyutlarını belirle
            const wrap = document.getElementById('canvas-wrap');
            const maxWidth = wrap.clientWidth;
            const maxHeight = wrap.clientHeight;
            
            let w = capturedImage.width;
            let h = capturedImage.height;
            
            const scale = Math.min(maxWidth / w, maxHeight / h);
            sourceCanvas.width = w * scale;
            sourceCanvas.height = h * scale;
            
            const ctx = sourceCanvas.getContext('2d');
            ctx.drawImage(capturedImage, 0, 0, sourceCanvas.width, sourceCanvas.height);
            
            // Başlangıç pim koordinatlarını ata (Ortada bir dikdörtgen)
            const cw = sourceCanvas.width;
            const ch = sourceCanvas.height;
            
            pinCoords.tl = { x: cw * 0.2, y: ch * 0.2 };
            pinCoords.tr = { x: cw * 0.8, y: ch * 0.2 };
            pinCoords.br = { x: cw * 0.8, y: ch * 0.8 };
            pinCoords.bl = { x: cw * 0.2, y: ch * 0.8 };
            
            updateUI();
        }

        function updateUI() {
            // Pim konumlarını güncelle
            for (let key in pins) {
                pins[key].style.left = `${pinCoords[key].x + sourceCanvas.offsetLeft}px`;
                pins[key].style.top = `${pinCoords[key].y + sourceCanvas.offsetTop}px`;
            }
            
            // Maske poligonunu güncelle
            const pointsStr = `
                ${pinCoords.tl.x + sourceCanvas.offsetLeft},${pinCoords.tl.y + sourceCanvas.offsetTop}
                ${pinCoords.tr.x + sourceCanvas.offsetLeft},${pinCoords.tr.y + sourceCanvas.offsetTop}
                ${pinCoords.br.x + sourceCanvas.offsetLeft},${pinCoords.br.y + sourceCanvas.offsetTop}
                ${pinCoords.bl.x + sourceCanvas.offsetLeft},${pinCoords.bl.y + sourceCanvas.offsetTop}
            `;
            polyMask.setAttribute('points', pointsStr);
        }

        let activePin = null;
        
        document.querySelectorAll('.pin').forEach(pin => {
            pin.addEventListener('pointerdown', (e) => {
                activePin = pin.getAttribute('data-id');
                pin.setPointerCapture(e.pointerId);
                magnifier.style.display = 'block';
                updateMagnifier(e);
            });
            
            pin.addEventListener('pointermove', (e) => {
                if (!activePin) return;
                
                const wrap = document.getElementById('canvas-wrap');
                const rect = sourceCanvas.getBoundingClientRect();
                
                let x = e.clientX - rect.left;
                let y = e.clientY - rect.top;
                
                // Sınırlar dışına taşmayı engelle
                x = Math.max(0, Math.min(x, sourceCanvas.width));
                y = Math.max(0, Math.min(y, sourceCanvas.height));
                
                pinCoords[activePin] = { x, y };
                updateUI();
                updateMagnifier(e);
            });
            
            const stopDrag = (e) => {
                if (activePin) {
                    pins[activePin].releasePointerCapture(e.pointerId);
                    activePin = null;
                    magnifier.style.display = 'none';
                }
            };
            
            pin.addEventListener('pointerup', stopDrag);
            pin.addEventListener('pointercancel', stopDrag);
        });

        function updateMagnifier(e) {
            if (!activePin) return;
            const rect = sourceCanvas.getBoundingClientRect();
            const px = pinCoords[activePin].x;
            const py = pinCoords[activePin].y;
            
            // Büyüteç konumunu parmağın biraz üstünde konumlandır
            magnifier.style.left = `${e.clientX - 50}px`;
            magnifier.style.top = `${e.clientY - 120}px`;
            
            // Canvas üzerindeki kesiti büyütece yansıt
            const zoom = 2.5;
            magnifier.style.backgroundImage = `url(${sourceCanvas.toDataURL()})`;
            magnifier.style.backgroundSize = `${sourceCanvas.width * zoom}px ${sourceCanvas.height * zoom}px`;
            magnifier.style.backgroundPosition = `-${(px * zoom) - 50}px -${(py * zoom) - 50}px`;
        }

        document.getElementById('warp-btn').addEventListener('click', () => {
            if (typeof cv === 'undefined' || !cv.Mat) {
                alert("Ölçüm sistemi yükleniyor, lütfen 1 saniye sonra tekrar deneyin.");
                return;
            }
            
            // Kaynak görsel yükleme
            let src = cv.imread(sourceCanvas);
            let dst = new cv.Mat();
            
            // Orijinal görsel üzerindeki gerçek koordinatları hesaplama (Ölçek çarpanına göre)
            const scaleX = capturedImage.width / sourceCanvas.width;
            const scaleY = capturedImage.height / sourceCanvas.height;
            
            let srcCoords = [
                pinCoords.tl.x * scaleX, pinCoords.tl.y * scaleY,
                pinCoords.tr.x * scaleX, pinCoords.tr.y * scaleY,
                pinCoords.br.x * scaleX, pinCoords.br.y * scaleY,
                pinCoords.bl.x * scaleX, pinCoords.bl.y * scaleY
            ];
            
            // En-boy hesaplama ve gerçekçi hedef alan belirleme
            let w1 = Math.hypot(srcCoords[2] - srcCoords[0], srcCoords[3] - srcCoords[1]);
            let w2 = Math.hypot(srcCoords[6] - srcCoords[4], srcCoords[7] - srcCoords[5]);
            let maxW = Math.max(w1, w2);
            
            let h1 = Math.hypot(srcCoords[4] - srcCoords[2], srcCoords[5] - srcCoords[3]);
            let h2 = Math.hypot(srcCoords[6] - srcCoords[0], srcCoords[7] - srcCoords[1]);
            let maxH = Math.max(h1, h2);
            
            // Doğal en-boy oranı
            warpAspectRatio = maxW / maxH;
            
            let dstCoords = [
                0, 0,
                maxW, 0,
                maxW, maxH,
                0, maxH
            ];
            
            let srcPts = cv.matFromArray(4, 1, cv.CV_32FC2, srcCoords);
            let dstPts = cv.matFromArray(4, 1, cv.CV_32FC2, dstCoords);
            
            // Perspektif dönüşüm matrisi
            let M = cv.getPerspectiveTransform(srcPts, dstPts);
            let dsize = new cv.Size(maxW, maxH);
            
            // Dönüşümü uygulama
            cv.warpPerspective(src, dst, M, dsize, cv.INTER_LINEAR, cv.BORDER_CONSTANT, new cv.Scalar());
            
            // Sonucu ekrana basma
            cv.imshow(resultCanvas, dst);
            
            // Belleği temizleme
            src.delete(); dst.delete(); srcPts.delete(); dstPts.delete(); M.delete();
            
            // UI Güncelleme ve Sonuç Ekranına Geçiş
            document.getElementById('ratio-text').innerText = `1 : ${warpAspectRatio.toFixed(2)}`;
            document.getElementById('real-width').value = '';
            document.getElementById('calculated-height').value = '';
            
            cropScreen.classList.remove('active');
            resultScreen.classList.add('active');
        });

        document.getElementById('real-width').addEventListener('input', (e) => {
            const val = parseFloat(e.target.value);
            if (val > 0 && warpAspectRatio > 0) {
                const calcHeight = val / warpAspectRatio;
                document.getElementById('calculated-height').value = calcHeight.toFixed(1);
            } else {
                document.getElementById('calculated-height').value = '';
            }
        });

        // Vazgeç / Geri Dön Butonları
        document.getElementById('back-to-cam').addEventListener('click', () => {
            cropScreen.classList.remove('active');
            camScreen.classList.add('active');
        });

        document.getElementById('reset-btn').addEventListener('click', () => {
            resultScreen.classList.remove('active');
            camScreen.classList.add('active');
        });
        
        window.addEventListener('resize', () => {
            if (cropScreen.classList.contains('active')) {
                showCropScreen();
            }
        });
    </script>
</body>
</html>
"""

components.html(html_code, height=900, scrolling=False)

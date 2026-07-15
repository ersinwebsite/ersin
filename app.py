import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Tabela Ölçer PRO",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Tüm Streamlit logolarını, menülerini, alt bilgileri ve boşlukları tamamen sıfırlayan CSS
st.markdown("""
    <style>
        #MainMenu {visibility: hidden; display: none !important;}
        header {visibility: hidden; display: none !important;}
        footer {visibility: hidden; display: none !important;}
        div[data-testid="stToolbar"] {visibility: hidden; display: none !important;}
        div[data-testid="stDecoration"] {visibility: hidden; display: none !important;}
        div[data-testid="stStatusWidget"] {visibility: hidden; display: none !important;}
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

html_code = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>Tabela Ölçer</title>
    <script src="https://unpkg.com/lucide@latest"></script>
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

        /* KAMERA TASARIMI */
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
            pointer-events: none;
        }
        .shutter-container {
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            pointer-events: auto;
        }
        .shutter-btn {
            width: 84px;
            height: 84px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.2);
            border: 4px solid #fff;
            display: flex;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            box-shadow: 0 0 20px rgba(0,0,0,0.6);
            transition: transform 0.1s ease;
        }
        .shutter-btn:active {
            transform: scale(0.9);
        }
        .shutter-inner {
            width: 64px;
            height: 64px;
            border-radius: 50%;
            background: #ffcc00;
            display: flex;
            justify-content: center;
            align-items: center;
            font-weight: 800;
            font-size: 14px;
            color: #000;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            box-shadow: inset 0 0 10px rgba(0,0,0,0.2);
        }

        /* ÖLÇÜM / PİM EKRANI */
        #measure-container {
            position: relative;
            width: 100%;
            height: 100%;
            background: #000;
        }
        #canvas-wrap {
            position: relative;
            width: 100%;
            height: 100%;
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
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
        }
        
        /* Ölçü Balonları */
        .measure-badge {
            position: absolute;
            background: rgba(17, 17, 17, 0.9);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            color: #ffd60a;
            border: 1.5px solid rgba(255, 214, 10, 0.6);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 15px;
            font-weight: 800;
            pointer-events: none;
            transform: translate(-50%, -50%);
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);
            white-space: nowrap;
            z-index: 10;
        }

        /* Şık Pimler */
        .pin {
            position: absolute;
            width: 40px;
            height: 40px;
            background: rgba(255, 214, 10, 0.4);
            border: 3px solid #ffd60a;
            border-radius: 50%;
            transform: translate(-50%, -50%);
            cursor: pointer;
            pointer-events: auto;
            touch-action: none;
            box-shadow: 0 0 15px rgba(255, 214, 10, 0.8);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 20;
        }
        .pin::after {
            content: '';
            width: 12px;
            height: 12px;
            background: #fff;
            border-radius: 50%;
        }

        /* Akıllı Kalibrasyon Sürgüsü */
        .calibration-card {
            position: absolute;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(17, 17, 17, 0.85);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
            padding: 10px 20px;
            border-radius: 30px;
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 85%;
            max-width: 340px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            z-index: 30;
            pointer-events: auto;
        }
        .calibration-title {
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #ffd60a;
            font-weight: 700;
            margin-bottom: 5px;
        }
        .slider-wrapper {
            width: 100%;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .modern-slider {
            -webkit-appearance: none;
            width: 100%;
            height: 6px;
            border-radius: 3px;
            background: rgba(255,255,255,0.2);
            outline: none;
        }
        .modern-slider::-webkit-slider-thumb {
            -webkit-appearance: none;
            appearance: none;
            width: 22px;
            height: 22px;
            border-radius: 50%;
            background: #ffd60a;
            cursor: pointer;
            box-shadow: 0 0 10px rgba(0,0,0,0.5);
        }

        /* Alt Aksiyon Butonları */
        .action-overlay {
            position: absolute;
            bottom: 30px;
            width: 100%;
            display: flex;
            justify-content: space-between;
            padding: 0 30px;
            pointer-events: none;
            z-index: 30;
        }
        .btn-circle {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: rgba(20, 20, 20, 0.85);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            border: 1px solid rgba(255,255,255,0.1);
            color: #fff;
            display: flex;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            pointer-events: auto;
            box-shadow: 0 6px 20px rgba(0,0,0,0.5);
            transition: all 0.2s ease;
        }
        .btn-circle:active {
            transform: scale(0.9);
        }
        .btn-circle.success {
            background: #ffd60a;
            color: #000;
            border: none;
        }
    </style>
</head>
<body>

    <!-- 1. KAMERA EKRANI -->
    <div id="camera-screen" class="screen active">
        <div id="camera-container">
            <video id="video" autoplay playsinline muted></video>
            <div class="camera-overlay">
                <div class="shutter-container">
                    <div class="shutter-btn" id="capture-btn">
                        <div class="shutter-inner">Çek</div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- 2. ÖLÇÜM / AYAR EKRANI -->
    <div id="measure-screen" class="screen">
        <div id="measure-container">
            
            <!-- Hassas Kalibrasyon / Mesafe Sürgüsü -->
            <div class="calibration-card">
                <div class="calibration-title">Mesafe / Hassas Ölçü Ayarı</div>
                <div class="slider-wrapper">
                    <i data-lucide="minus" style="width: 16px; height: 16px; color: #fff;"></i>
                    <input type="range" id="calibration-slider" min="100" max="600" value="300" class="modern-slider">
                    <i data-lucide="plus" style="width: 16px; height: 16px; color: #fff;"></i>
                </div>
            </div>

            <div id="canvas-wrap">
                <canvas id="source-canvas"></canvas>
                <svg id="interactive-svg">
                    <!-- Bağlantı Çizgileri - 4 Tarafı da Aynı Belirginlikte Sarı -->
                    <line id="line-top" stroke="#ffd60a" stroke-width="3" stroke-dasharray="6,6" />
                    <line id="line-right" stroke="#ffd60a" stroke-width="3" stroke-dasharray="6,6" />
                    <line id="line-bottom" stroke="#ffd60a" stroke-width="3" stroke-dasharray="6,6" />
                    <line id="line-left" stroke="#ffd60a" stroke-width="3" stroke-dasharray="6,6" />
                </svg>
                
                <!-- Ölçüm Etiketleri (Sadece Üst ve Sağ Kenar İçin) -->
                <div class="measure-badge" id="badge-top">0 cm</div>
                <div class="measure-badge" id="badge-right">0 cm</div>

                <!-- 2 Adet Sürüklenebilir Pim (Sol-Üst ve Sağ-Alt) -->
                <div class="pin" id="pin-tl" data-id="tl"></div>
                <div class="pin" id="pin-br" data-id="br"></div>
            </div>
            
            <!-- Alt Aksiyon Butonları -->
            <div class="action-overlay">
                <button class="btn-circle" id="back-to-cam" title="Geri Dön">
                    <i data-lucide="arrow-left" style="width: 26px; height: 26px;"></i>
                </button>
                <button class="btn-circle success" id="save-btn" title="Kaydet">
                    <i data-lucide="download" style="width: 26px; height: 26px;"></i>
                </button>
            </div>
        </div>
    </div>

    <script>
        const video = document.getElementById('video');
        const captureBtn = document.getElementById('capture-btn');
        const sourceCanvas = document.getElementById('source-canvas');
        const calibrationSlider = document.getElementById('calibration-slider');
        
        // Ekran Katmanları
        const camScreen = document.getElementById('camera-screen');
        const measureScreen = document.getElementById('measure-screen');
        
        // Pimler ve Çizgiler
        const pins = {
            tl: document.getElementById('pin-tl'),
            br: document.getElementById('pin-br')
        };
        
        const lineTop = document.getElementById('line-top');
        const lineRight = document.getElementById('line-right');
        const lineBottom = document.getElementById('line-bottom');
        const lineLeft = document.getElementById('line-left');
        
        const badgeTop = document.getElementById('badge-top');
        const badgeRight = document.getElementById('badge-right');
        
        let pinCoords = {
            tl: { x: 0, y: 0 },
            br: { x: 0, y: 0 }
        };

        let capturedImage = new Image();

        // Kamerayı Başlat (Arka Kamera Öncelikli)
        async function startCamera() {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({
                    video: { facingMode: { exact: "environment" } },
                    audio: false
                });
                video.srcObject = stream;
            } catch (err) {
                try {
                    const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
                    video.srcObject = stream;
                } catch (e) {
                    console.error("Kameraya erişilemedi: " + e.message);
                }
            }
        }

        startCamera();

        // Fotoğrafı Çek
        captureBtn.addEventListener('click', () => {
            const tempCanvas = document.createElement('canvas');
            tempCanvas.width = video.videoWidth;
            tempCanvas.height = video.videoHeight;
            const ctx = tempCanvas.getContext('2d');
            ctx.drawImage(video, 0, 0, tempCanvas.width, tempCanvas.height);
            
            capturedImage.src = tempCanvas.toDataURL('image/jpeg');
            capturedImage.onload = () => {
                showMeasureScreen();
            };
        });

        // Ölçüm Ekranını ve Pim Başlangıç Konumlarını Kur
        function showMeasureScreen() {
            camScreen.classList.remove('active');
            measureScreen.classList.add('active');
            
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
            
            const cw = sourceCanvas.width;
            const ch = sourceCanvas.height;
            
            // Başlangıçta ekranın ortasında dikey/yatay dengeli pimler
            pinCoords.tl = { x: cw * 0.25, y: ch * 0.35 };
            pinCoords.br = { x: cw * 0.75, y: ch * 0.65 };
            
            updateUI();
        }

        // Pimlerin Konumlarına Göre Çizgileri ve Ölçüleri Hesapla
        function updateUI() {
            const canvasOffsetLeft = sourceCanvas.offsetLeft;
            const canvasOffsetTop = sourceCanvas.offsetTop;

            // Pimleri yerleştir
            pins.tl.style.left = `${pinCoords.tl.x + canvasOffsetLeft}px`;
            pins.tl.style.top = `${pinCoords.tl.y + canvasOffsetTop}px`;
            
            pins.br.style.left = `${pinCoords.br.x + canvasOffsetLeft}px`;
            pins.br.style.top = `${pinCoords.br.y + canvasOffsetTop}px`;

            // Diğer iki sanal köşeyi hesapla (Mükemmel dikdörtgen için)
            const tr = { x: pinCoords.br.x + canvasOffsetLeft, y: pinCoords.tl.y + canvasOffsetTop };
            const bl = { x: pinCoords.tl.x + canvasOffsetLeft, y: pinCoords.br.y + canvasOffsetTop };
            const tl = { x: pinCoords.tl.x + canvasOffsetLeft, y: pinCoords.tl.y + canvasOffsetTop };
            const br = { x: pinCoords.br.x + canvasOffsetLeft, y: pinCoords.br.y + canvasOffsetTop };

            // Çizgileri güncelle - Hepsi Sarı ve Net
            lineTop.setAttribute('x1', tl.x); lineTop.setAttribute('y1', tl.y);
            lineTop.setAttribute('x2', tr.x); lineTop.setAttribute('y2', tr.y);

            lineRight.setAttribute('x1', tr.x); lineRight.setAttribute('y1', tr.y);
            lineRight.setAttribute('x2', br.x); lineRight.setAttribute('y2', br.y);

            lineBottom.setAttribute('x1', br.x); lineBottom.setAttribute('y1', br.y);
            lineBottom.setAttribute('x2', bl.x); lineBottom.setAttribute('y2', bl.y);

            lineLeft.setAttribute('x1', bl.x); lineLeft.setAttribute('y1', bl.y);
            lineLeft.setAttribute('x2', tl.x); lineLeft.setAttribute('y2', tl.y);

            // Akıllı Fiziksel Mesafe/cm Hesaplama Formülü
            // Kullanıcı alttaki slider ile mesafesini (kalibrasyonunu) anlık olarak ayarlar.
            const calibrationFactor = calibrationSlider.value / 350; // Standart referans katsayısı
            const scaleFactor = (sourceCanvas.width / 100) * calibrationFactor;

            const widthPx = Math.abs(pinCoords.br.x - pinCoords.tl.x);
            const heightPx = Math.abs(pinCoords.br.y - pinCoords.tl.y);

            // Pikselden gerçek santimetreye dönüştürme
            const widthCm = Math.round(widthPx / scaleFactor);
            const heightCm = Math.round(heightPx / scaleFactor);

            // Ölçü Balonlarını Konumlandır ve cm Yaz
            badgeTop.style.left = `${(tl.x + tr.x) / 2}px`;
            badgeTop.style.top = `${tl.y - 25}px`;
            badgeTop.innerText = `${widthCm} cm`;

            badgeRight.style.left = `${tr.x + 40}px`;
            badgeRight.style.top = `${(tr.y + br.y) / 2}px`;
            badgeRight.innerText = `${heightCm} cm`;
        }

        // Kalibrasyon Sürgüsü Değiştiğinde Ölçüleri Anlık Güncelle
        calibrationSlider.addEventListener('input', updateUI);

        // Sürükleme ve Dokunma Kontrolleri
        let activePin = null;
        
        document.querySelectorAll('.pin').forEach(pin => {
            pin.addEventListener('pointerdown', (e) => {
                activePin = pin.getAttribute('data-id');
                pin.setPointerCapture(e.pointerId);
            });
            
            pin.addEventListener('pointermove', (e) => {
                if (!activePin) return;
                
                const rect = sourceCanvas.getBoundingClientRect();
                let x = e.clientX - rect.left;
                let y = e.clientY - rect.top;
                
                // Canvas dışına taşmayı engelle
                x = Math.max(0, Math.min(x, sourceCanvas.width));
                y = Math.max(0, Math.min(y, sourceCanvas.height));
                
        document.getElementById('save-btn').addEventListener('click', async () => {
            const outCanvas = document.createElement('canvas');
            outCanvas.width = capturedImage.width;
            outCanvas.height = capturedImage.height;
            const ctx = outCanvas.getContext('2d');
            
            // 1. Orijinal fotoğrafı çiz
            ctx.drawImage(capturedImage, 0, 0);
            
            // Ölçek katsayıları
            const scaleX = capturedImage.width / sourceCanvas.width;
            const scaleY = capturedImage.height / sourceCanvas.height;
            
            const tl = { x: pinCoords.tl.x * scaleX, y: pinCoords.tl.y * scaleY };
            const br = { x: pinCoords.br.x * scaleX, y: pinCoords.br.y * scaleY };
            const tr = { x: br.x, y: tl.y };
            const bl = { x: tl.x, y: br.y };

            // 2. Ölçü Çizgilerini Çiz
            ctx.strokeStyle = '#ffd60a';
            ctx.lineWidth = Math.max(5, capturedImage.width * 0.006);
            
            // 4 tarafı da belirgin sarı olarak çiz
            ctx.beginPath();
            ctx.moveTo(tl.x, tl.y);
            ctx.lineTo(tr.x, tr.y);
            ctx.lineTo(br.x, br.y);
            ctx.lineTo(bl.x, bl.y);
            ctx.closePath();
            ctx.stroke();

            // Ölçülerin Hesabı
            const calibrationFactor = calibrationSlider.value / 350;
            const finalScale = (capturedImage.width / 100) * calibrationFactor;

            const wCm = Math.round(Math.abs(br.x - tl.x) / finalScale);
            const hCm = Math.round(Math.abs(br.y - tl.y) / finalScale);

            // 3. Ölçü Etiketlerini Çiz
            const fontSize = Math.max(22, Math.round(capturedImage.width * 0.026));
            ctx.font = `bold ${fontSize}px -apple-system, sans-serif`;
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';

            // Üst Etiket
            drawBadge(ctx, `${wCm} cm`, (tl.x + tr.x) / 2, tl.y - (fontSize * 1.3), fontSize);
            // Sağ Etiket
            drawBadge(ctx, `${hCm} cm`, tr.x + (fontSize * 1.9), (tr.y + br.y) / 2, fontSize);

            const dataUrl = outCanvas.toDataURL('image/jpeg', 0.95);

            try {
                // iPhone (iOS) için yerleşik paylaşım sistemini tetikler
                const response = await fetch(dataUrl);
                const blob = await response.blob();
                const file = new File([blob], `tabela_olcum_${Date.now()}.jpg`, { type: 'image/jpeg' });
                
                if (navigator.canShare && navigator.canShare({ files: [file] })) {
                    await navigator.share({
                        files: [file],
                        title: 'Tabela Ölçümü',
                    });
                    return; // İşlem başarılı, doğrudan indirme adımını atla
                }
            } catch (err) {
                console.log("Paylaşım desteklenmiyor, standart indirmeye geçiliyor.", err);
            }

            // Android veya Desteklemeyen Cihazlar İçin Doğrudan İndirme
            const downloadLink = document.createElement('a');
            downloadLink.download = `tabela_olcum_${Date.now()}.jpg`;
            downloadLink.href = dataUrl;
            
            document.body.appendChild(downloadLink);
            downloadLink.click();
            document.body.removeChild(downloadLink);
        });

        // Şık Balon Çizme Yardımcı Fonksiyonu
        function drawBadge(ctx, text, x, y, fontSize) {
            const paddingH = fontSize * 0.8;
            const paddingV = fontSize * 0.4;
            const textWidth = ctx.measureText(text).width;
            const rectW = textWidth + (paddingH * 2);
            const rectH = fontSize + (paddingV * 2);
            
            ctx.fillStyle = 'rgba(17, 17, 17, 0.95)';
            roundRect(ctx, x - (rectW / 2), y - (rectH / 2), rectW, rectH, rectH / 2);
            ctx.fill();
            
            ctx.strokeStyle = '#ffd60a';
            ctx.lineWidth = 3;
            ctx.stroke();
            
            ctx.fillStyle = '#ffd60a';
            ctx.fillText(text, x, y);
        }

        function roundRect(ctx, x, y, width, height, radius) {
            ctx.beginPath();
            ctx.moveTo(x + radius, y);
            ctx.lineTo(x + width - radius, y);
            ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
            ctx.lineTo(x + width, y + height - radius);
            ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
            ctx.lineTo(x + radius, y + height);
            ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
            ctx.lineTo(x, y + radius);
            ctx.quadraticCurveTo(x, y, x + radius, y);
            ctx.closePath();
        }

        // Geri Dön / Vazgeç Butonu
        document.getElementById('back-to-cam').addEventListener('click', () => {
            measureScreen.classList.remove('active');
            camScreen.classList.add('active');
        });
        
        window.addEventListener('resize', () => {
            if (measureScreen.classList.contains('active')) {
                showMeasureScreen();
            }
        });

        // İkonları Yükle
        lucide.createIcons();
    </script>
</body>
</html>
"""

components.html(html_code, height=900, scrolling=False)

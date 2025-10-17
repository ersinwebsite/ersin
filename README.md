<html lang="tr" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ErsinTeknik - Teknik Analiz Platformu</title>
    
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <!-- Lightweight Charts by TradingView -->
    <script src="https://unpkg.com/lightweight-charts@4.1.3/dist/lightweight-charts.standalone.production.js"></script>

    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>

    <!-- html2canvas for screenshots -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>


    <!-- Google Fonts: Inter -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">

    <style>
        html, body {
            height: 100%;
            margin: 0;
            padding: 0;
            overflow: hidden;
        }
        body {
            font-family: 'Inter', sans-serif;
            background-color: #131722;
            color: #d1d4dc;
        }
        .right-panel-tab.active { background-color: #2962FF; color: white; }
        .tool-button.active { color: #2962FF; } /* Sadece ikon rengini değiştirir, arka planı değil */
        .timeframe-item.active-timeframe { background-color: #2962FF; color: white; }
        .crosshair-style-btn {
            color: #9ca3af; /* gray-400 */
            transition: background-color 0.2s;
        }
        .crosshair-style-btn svg {
            pointer-events: none;
        }
        .crosshair-style-btn:hover {
            background-color: #374151; /* gray-700 */
        }
        .crosshair-style-btn.active {
            background-color: #2563EB; /* blue-600 */
            color: white;
        }
        .bg-color-swatch.active {
            box-shadow: 0 0 0 2px #2563EB;
        }
        .custom-color-label.active {
            border-color: #2563EB;
        }
        ::-webkit-scrollbar { width: 8px; height: 8px; }
        ::-webkit-scrollbar-track { background: #1e222d; }
        ::-webkit-scrollbar-thumb { background: #4a4e59; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #5a5e69; }
        
        .chart-instance-container, .indicator-pane-container, .main-chart-pane {
            position: relative;
        }
        .indicator-labels-container {
            position: absolute;
            top: 8px;
            left: 8px;
            z-index: 10;
            display: flex;
            flex-direction: column;
            gap: 4px;
            pointer-events: none;
        }
        .indicator-labels-container > div {
            pointer-events: all;
        }
        .chart-instance-container.active-chart {
            border: 2px solid transparent; /* Mavi çerçeve kalıcı olarak kaldırıldı */
        }
        .resizer-v {
            width: 8px;
            cursor: col-resize;
            background-color: #1f2937; /* gray-800 */
            flex-shrink: 0;
            transition: background-color: 0.2s;
        }
        .resizer-h {
            height: 8px;
            cursor: row-resize;
            background-color: #1f2937; /* gray-800 */
            flex-shrink: 0;
            transition: background-color: 0.2s;
        }
        .resizer-v:hover, .resizer-h:hover {
            background-color: #2563EB; /* blue-600 */
        }
        .note-color-picker {
            -webkit-appearance: none;
            -moz-appearance: none;
            appearance: none;
            width: 20px;
            height: 20px;
            background-color: transparent;
            border: none;
            cursor: pointer;
        }
        .note-color-picker::-webkit-color-swatch {
            border-radius: 50%;
            border: 1px solid #6b7280;
        }
        .note-color-picker::-moz-color-swatch {
            border-radius: 50%;
            border: 1px solid #6b7280;
        }
        .modal-resizer {
            position: absolute;
            bottom: 5px;
            right: 5px;
            width: 20px;
            height: 20px;
            cursor: se-resize;
            background: repeating-linear-gradient(
                -45deg,
                rgba(255, 255, 255, 0.2),
                rgba(255, 255, 255, 0.2) 2px,
                transparent 2px,
                transparent 4px
            );
        }
    </style>
</head>
<body class="flex flex-col h-screen">

    <!-- Main Content -->
    <div class="flex flex-1 overflow-hidden">
        
        <!-- Sol Araç Çubuğu -->
        <nav id="left-toolbar" class="flex flex-col items-center gap-1 p-2 border-r border-gray-700 bg-gray-900/30 flex-shrink-0 transition-all duration-300 w-14 overflow-hidden">
            <div id="toolbar-content" class="flex flex-col items-center gap-1 flex-1 w-full">
                <button class="tool-button p-2 rounded-md hover:bg-gray-700 active" title="İmleç"><i data-lucide="mouse-pointer-2" class="w-5 h-5"></i></button>
                <button class="tool-button p-2 rounded-md hover:bg-gray-700" title="Trend Çizgisi"><i data-lucide="trending-up" class="w-5 h-5"></i></button>
                <button class="tool-button p-2 rounded-md hover:bg-gray-700" title="Fibonacci Düzeltmesi"><i data-lucide="git-merge" class="w-5 h-5"></i></button>
                <button class="tool-button p-2 rounded-md hover:bg-gray-700" title="Yatay Çizgi"><i data-lucide="minus" class="w-5 h-5"></i></button>
                <div class="flex-1"></div>
            </div>
        </nav>

        <!-- Grafik ve Kontroller -->
        <main class="flex-1 flex flex-col min-w-0 relative">
             <button id="left-toolbar-toggle" class="absolute top-1/2 left-14 z-30 p-1 bg-gray-700 hover:bg-blue-600 rounded-full focus:outline-none transition-all duration-300 -translate-y-1/2">
                 <i data-lucide="chevron-left" class="w-5 h-5 transition-transform duration-300"></i>
            </button>
            <!-- Üst Kontrol Çubuğu -->
            <div class="flex items-center justify-between gap-2 p-2 border-b border-gray-700">
                <div class="flex items-center gap-2 min-w-0 flex-shrink">
                    <span id="symbol-name" class="font-bold text-lg whitespace-nowrap">BTCUSDT</span>
                    <div class="h-6 border-l border-gray-700 mx-2"></div>
                    <div class="relative">
                        <button id="time-menu-button" class="flex items-center gap-1.5 px-2.5 py-1 text-sm rounded-md hover:bg-gray-700">
                           <span>Zaman</span>
                           <i data-lucide="chevron-down" class="w-4 h-4"></i>
                        </button>
                        <div id="time-menu-dropdown" class="absolute left-0 mt-2 w-auto bg-gray-800 border border-gray-700 rounded-md shadow-lg z-20 hidden p-2">
                            <div class="flex items-center space-x-1 flex-wrap gap-1">
                                <button class="timeframe-item px-3 py-1 text-sm rounded-md hover:bg-gray-700" data-timeframe="5m">5dk</button>
                                <button class="timeframe-item px-3 py-1 text-sm rounded-md hover:bg-gray-700" data-timeframe="15m">15dk</button>
                                <button class="timeframe-item px-3 py-1 text-sm rounded-md hover:bg-gray-700" data-timeframe="30m">30dk</button>
                                <button class="timeframe-item px-3 py-1 text-sm rounded-md hover:bg-gray-700" data-timeframe="1h">1s</button>
                                <button class="timeframe-item px-3 py-1 text-sm rounded-md hover:bg-gray-700" data-timeframe="4h">4s</button>
                                <button class="timeframe-item px-3 py-1 text-sm rounded-md hover:bg-gray-700 active-timeframe" data-timeframe="1d">1g</button>
                                <button class="timeframe-item px-3 py-1 text-sm rounded-md hover:bg-gray-700" data-timeframe="1M">1ay</button>
                                <!-- Custom timeframes will be added here -->
                            </div>
                            <div class="border-t border-gray-700 my-2"></div>
                            <div class="px-1 pb-1">
                                <label class="text-xs text-gray-400">Özel</label>
                                <div class="flex items-center gap-2 mt-1">
                                    <input type="number" id="custom-timeframe-value" min="1" value="12" class="w-16 bg-gray-900 border border-gray-700 rounded-md px-2 py-1 text-sm focus:outline-none focus:ring-1 focus:ring-blue-500">
                                    <select id="custom-timeframe-unit" class="bg-gray-900 border border-gray-700 rounded-md px-1 py-1 text-sm focus:outline-none focus:ring-1 focus:ring-blue-500">
                                        <option value="m">Dakika</option>
                                        <option value="h" selected>Saat</option>
                                        <option value="d">Gün</option>
                                    </select>
                                    <button id="save-custom-timeframe" class="p-1.5 bg-blue-600 hover:bg-blue-700 rounded-md flex-1 text-sm text-white">Ekle</button>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="relative">
                        <button id="indicators-button" class="flex items-center gap-1.5 px-2.5 py-1 text-sm rounded-md hover:bg-gray-700" title="Göstergeler">
                           Gösterge
                        </button>
                        <div id="indicators-dropdown" class="absolute left-0 mt-2 w-64 bg-gray-800 border border-gray-700 rounded-md shadow-lg z-20 hidden p-2">
                            <input type="text" id="indicator-search" placeholder="Gösterge ara..." class="w-full bg-gray-900 border border-gray-700 rounded-md px-2 py-1.5 mb-2 focus:outline-none focus:ring-1 focus:ring-blue-500">
                            <div id="indicator-list" class="max-h-60 overflow-y-auto"></div>
                        </div>
                    </div>
                    <button id="replay-button" class="flex items-center gap-1.5 px-2.5 py-1 text-sm rounded-md hover:bg-gray-700" title="Tekrar Oynat">
                        Tekrar
                    </button>
                     <div class="relative">
                        <button id="layout-button" class="flex items-center gap-1.5 px-2.5 py-1 text-sm rounded-md hover:bg-gray-700" title="Ekranı bölme">
                            Bölme
                        </button>
                        <div id="layout-dropdown" class="absolute left-0 mt-2 w-48 bg-gray-800 border border-gray-700 rounded-md shadow-lg z-20 hidden p-1">
                            <div class="grid grid-cols-4 gap-1">
                                <a href="#" class="layout-item flex items-center justify-center p-2 rounded hover:bg-gray-700" title="1 Grafik" data-layout="1x1"><i data-lucide="square" class="w-5 h-5"></i></a>
                                <a href="#" class="layout-item flex items-center justify-center p-2 rounded hover:bg-gray-700" title="2 Dikey" data-layout="2x1"><i data-lucide="columns" class="w-5 h-5"></i></a>
                                <a href="#" class="layout-item flex items-center justify-center p-2 rounded hover:bg-gray-700" title="2 Yatay" data-layout="1x2"><i data-lucide="rows" class="w-5 h-5"></i></a>
                                <a href="#" class="layout-item flex items-center justify-center p-2 rounded hover:bg-gray-700" title="3 Dikey" data-layout="3x1"><i data-lucide="columns-3" class="w-5 h-5"></i></a>
                                <a href="#" class="layout-item flex items-center justify-center p-2 rounded hover:bg-gray-700" title="3 Yatay" data-layout="1x3"><i data-lucide="rows-3" class="w-5 h-5"></i></a>
                                 <a href="#" class="layout-item flex items-center justify-center p-2 rounded hover:bg-gray-700" title="1 Dikey, 2 Yatay" data-layout="1v2h">
                                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                        <rect x="3" y="3" width="8" height="18"></rect>
                                        <rect x="13" y="3" width="8" height="8"></rect>
                                        <rect x="13" y="13" width="8" height="8"></rect>
                                    </svg>
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="flex items-center flex-shrink-0">
                     <button id="settings-button" class="p-2 hover:bg-gray-700 rounded-md" title="Ayarlar">
                        <i data-lucide="settings-2" class="w-5 h-5"></i>
                    </button>
                </div>
            </div>
            <!-- Chart Container Wrapper -->
            <div id="chart-wrapper" class="flex-1 w-full h-full flex flex-col">
                <!-- Dinamik olarak doldurulacak -->
            </div>
            <!-- Replay Controls -->
            <div id="replay-controls" class="absolute bottom-4 left-1/2 -translate-x-1/2 bg-gray-900 bg-opacity-80 backdrop-blur-sm p-2 rounded-lg shadow-lg flex items-center gap-2 z-20 hidden">
                <button id="replay-play-pause" data-state="paused" class="p-2 hover:bg-gray-700 rounded-md" title="Oynat"><i data-lucide="play" class="w-5 h-5"></i></button>
                <button id="replay-step-forward" class="p-2 hover:bg-gray-700 rounded-md" title="Sonraki Mum"><i data-lucide="skip-forward" class="w-5 h-5"></i></button>
                <div class="relative">
                    <button id="replay-speed-button" class="px-3 py-2 text-sm hover:bg-gray-700 rounded-md">1x</button>
                    <div id="replay-speed-dropdown" class="absolute bottom-full mb-2 w-20 bg-gray-800 border border-gray-700 rounded-md shadow-lg z-10 hidden">
                        <a href="#" class="block px-3 py-1 text-sm text-center hover:bg-gray-700" data-speed="1000">0.5x</a>
                        <a href="#" class="block px-3 py-1 text-sm text-center hover:bg-gray-700" data-speed="500">1x</a>
                        <a href="#" class="block px-3 py-1 text-sm text-center hover:bg-gray-700" data-speed="250">2x</a>
                        <a href="#" class="block px-3 py-1 text-sm text-center hover:bg-gray-700" data-speed="100">5x</a>
                    </div>
                </div>
                 <div class="h-6 border-l border-gray-700 mx-1"></div>
                <button id="replay-exit" class="p-2 hover:bg-gray-700 rounded-md text-red-500" title="Tekrar Oynatmadan Çık"><i data-lucide="x-circle" class="w-5 h-5"></i></button>
            </div>
        </main>

        <!-- Sağ Paneller Konteyneri -->
        <div id="right-panel-container" class="flex flex-shrink-0">
            <aside id="right-panel-content" class="w-48 flex-col bg-gray-900/30 border-l border-gray-700 hidden"></aside>
            <nav class="flex flex-col items-center gap-2 p-2 border-l border-gray-700 bg-gray-800">
                <button data-panel="watchlist" class="right-panel-tab p-2 rounded-md hover:bg-gray-700" title="İzleme Listesi"><i data-lucide="search" class="w-5 h-5"></i></button>
                <button data-panel="notes" class="right-panel-tab p-2 rounded-md hover:bg-gray-700" title="Notlar"><i data-lucide="notebook" class="w-5 h-5"></i></button>
                <button data-panel="alarms" class="right-panel-tab p-2 rounded-md hover:bg-gray-700" title="Alarmlar"><i data-lucide="bell" class="w-5 h-5"></i></button>
                <button data-panel="chat" class="right-panel-tab p-2 rounded-md hover:bg-gray-700" title="Sohbet"><i data-lucide="message-square" class="w-5 h-5"></i></button>
                <button data-panel="sharing" class="right-panel-tab p-2 rounded-md hover:bg-gray-700" title="Paylaşım"><i data-lucide="share-2" class="w-5 h-5"></i></button>
                <button data-panel="following" class="right-panel-tab p-2 rounded-md hover:bg-gray-700" title="Takip Edilenler"><i data-lucide="users" class="w-5 h-5"></i></button>
            </nav>
        </div>
    </div>
    
    <!-- Modals -->
     <div id="indicator-settings-modal" class="fixed inset-0 bg-black bg-opacity-70 items-center justify-center z-50 hidden">
        <div class="bg-gray-800 rounded-lg shadow-xl w-full max-w-sm p-6">
            <h3 id="indicator-settings-title" class="text-xl font-semibold mb-4">Gösterge Ayarları</h3>
            <div id="indicator-settings-fields" class="space-y-4">
                <!-- Ayar alanları dinamik olarak buraya eklenecek -->
            </div>
            <div class="flex justify-end gap-3 mt-6">
                <button type="button" id="cancel-indicator-settings-button" class="px-4 py-2 text-sm rounded-md hover:bg-gray-700">İptal</button>
                <button type="button" id="save-indicator-settings-button" class="px-4 py-2 text-sm bg-blue-600 hover:bg-blue-700 text-white rounded-md">Kaydet</button>
            </div>
        </div>
    </div>

     <div id="settings-modal" class="fixed inset-0 bg-black bg-opacity-70 items-center justify-center z-50 hidden">
        <div class="bg-gray-800 rounded-lg shadow-xl w-full max-w-sm p-6">
            <div class="mb-4">
                <label class="block text-sm font-medium text-gray-400 mb-2">Arka Plan Rengi</label>
                <div id="bg-color-swatches" class="flex items-center gap-3">
                    <button class="bg-color-swatch w-8 h-8 rounded-full border-2 border-gray-600" data-color="#131722" style="background-color: #131722;" title="Koyu Gri"></button>
                    <button class="bg-color-swatch w-8 h-8 rounded-full border-2 border-gray-600" data-color="#1e222d" style="background-color: #1e222d;" title="Açık Koyu"></button>
                    <button class="bg-color-swatch w-8 h-8 rounded-full border-2 border-gray-600" data-color="#f9fafb" style="background-color: #f9fafb;" title="Açık"></button>
                    <label for="bg-color-picker" class="custom-color-label w-8 h-8 rounded-full border-2 border-dashed border-gray-500 flex items-center justify-center cursor-pointer hover:border-blue-500 transition-colors" title="Özel Renk">
                        <i data-lucide="palette" class="w-4 h-4 text-gray-400"></i>
                    </label>
                    <input type="color" id="bg-color-picker" class="absolute opacity-0 w-0 h-0">
                </div>
            </div>
            <div class="border-t border-gray-700 my-4"></div>
            <h4 class="text-lg font-semibold mb-3">Mause İmleci</h4>
            <div class="flex items-end gap-4">
                <div class="flex-shrink-0">
                    <label for="crosshair-color-picker" class="block text-xs font-medium text-gray-400 mb-1">Renk</label>
                    <input type="color" id="crosshair-color-picker" class="w-12 h-9 p-1 bg-gray-700 border border-gray-600 rounded-md cursor-pointer">
                </div>
                <div class="flex-shrink-0">
                    <label class="block text-xs font-medium text-gray-400 mb-1">Stil</label>
                    <div id="crosshair-style-buttons" class="flex items-center border border-gray-600 rounded-md h-9 p-0.5 bg-gray-900/50 space-x-0.5">
                        <button data-style="0" class="crosshair-style-btn h-full rounded-md px-2" title="Düz Çizgi">
                            <svg viewBox="0 0 24 24" class="w-5 h-5"><line x1="0" y1="12" x2="24" y2="12" stroke="currentColor" stroke-width="2"></line></svg>
                        </button>
                        <button data-style="1" class="crosshair-style-btn h-full rounded-md px-2" title="Noktalı Çizgi">
                            <svg viewBox="0 0 24 24" class="w-5 h-5"><line x1="0" y1="12" x2="24" y2="12" stroke="currentColor" stroke-width="2" stroke-dasharray="1 4" stroke-linecap="round"></line></svg>
                        </button>
                        <button data-style="2" class="crosshair-style-btn h-full rounded-md px-2" title="Kesikli Çizgi">
                            <svg viewBox="0 0 24 24" class="w-5 h-5"><line x1="0" y1="12" x2="24" y2="12" stroke="currentColor" stroke-width="2" stroke-dasharray="6 4"></line></svg>
                        </button>
                    </div>
                </div>
                <div class="flex-1 min-w-0">
                    <label for="crosshair-width-slider" class="block text-xs font-medium text-gray-400 mb-1">Kalınlık (<span id="crosshair-width-value">1</span>px)</label>
                    <input type="range" id="crosshair-width-slider" min="1" max="5" step="1" class="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer">
                </div>
            </div>
            <div class="flex justify-end gap-3 mt-6">
                <button type="button" id="cancel-settings-button" class="px-4 py-2 text-sm rounded-md hover:bg-gray-700">Kapat</button>
                <button type="button" id="save-settings-button" class="px-4 py-2 text-sm bg-blue-600 hover:bg-blue-700 text-white rounded-md">Kaydet</button>
            </div>
        </div>
    </div>

    <div id="create-alarm-modal" class="fixed inset-0 bg-black bg-opacity-70 items-center justify-center z-50 hidden">
        <div class="bg-gray-800 rounded-lg shadow-xl w-full max-w-sm p-6">
            <h3 class="text-xl font-semibold mb-4">Alarm Kur: <span id="alarm-modal-symbol"></span></h3>
            <form id="alarm-form">
                <div class="mb-4">
                    <label for="alarm-price" class="block text-sm font-medium text-gray-400 mb-1">Fiyat</label>
                    <input type="number" id="alarm-price" step="any" required class="w-full bg-gray-900 border border-gray-700 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
                </div>
                <div class="flex justify-end gap-3">
                    <button type="button" id="cancel-alarm-button" class="px-4 py-2 text-sm rounded-md hover:bg-gray-700">İptal</button>
                    <button type="submit" class="px-4 py-2 text-sm bg-blue-600 hover:bg-blue-700 text-white rounded-md">Kur</button>
                </div>
            </form>
        </div>
    </div>

    <div id="add-symbol-modal" class="fixed inset-0 bg-black bg-opacity-70 items-center justify-center z-50 hidden">
        <div class="bg-gray-800 rounded-lg shadow-xl w-full max-w-md p-6">
            <div class="flex justify-between items-center mb-4">
                <h3 class="text-xl font-semibold">Sembol Ekle</h3>
                <button id="close-modal-button" class="p-1 rounded-full hover:bg-gray-700"><i data-lucide="x" class="w-5 h-5"></i></button>
            </div>
            <div>
                <div class="relative mb-4">
                     <i data-lucide="search" class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400"></i>
                    <input type="text" id="search-symbol-input" placeholder="Arama yap..." class="w-full bg-gray-900 border border-gray-700 rounded-md pl-9 pr-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
                </div>
                <div id="symbol-results-list" class="max-h-80 overflow-y-auto"></div>
            </div>
        </div>
    </div>

     <div id="private-chat-modal" class="fixed inset-0 bg-black bg-opacity-70 items-center justify-center z-50 hidden">
        <div class="bg-gray-800 rounded-lg shadow-xl w-full max-w-md flex flex-col" style="height: 500px;">
            <div class="flex justify-between items-center p-3 border-b border-gray-700 flex-shrink-0">
                <h3 class="text-lg font-semibold">Özel Sohbet: <span id="private-chat-recipient-name"></span></h3>
                <button id="close-private-chat-button" class="p-1 rounded-full hover:bg-gray-700"><i data-lucide="x" class="w-5 h-5"></i></button>
            </div>
            <div id="private-chat-messages" class="flex-1 p-2 overflow-y-auto flex flex-col">
                <!-- Private messages here -->
            </div>
            <form id="private-chat-form" class="p-2 border-t border-gray-700 flex-shrink-0">
                 <div class="relative flex items-center">
                    <input type="text" id="private-chat-input" placeholder="Özel mesaj yaz..." class="w-full bg-gray-900 border border-gray-700 rounded-md px-3 py-1.5 pr-10 focus:outline-none focus:ring-1 focus:ring-blue-500">
                    <button type="submit" class="absolute right-2 p-1.5 rounded-md text-gray-400 hover:text-white hover:bg-blue-600">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-send"><path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/></svg>
                    </button>
                </div>
            </form>
        </div>
    </div>
    
    <div id="share-idea-modal" class="fixed inset-0 bg-black bg-opacity-70 items-center justify-center z-50 hidden">
        <div class="bg-gray-800 rounded-lg shadow-xl w-full max-w-3xl flex flex-col h-[80vh] relative resize overflow-hidden">
            <div class="flex justify-between items-center p-3 border-b border-gray-700">
                <h3 class="text-xl font-semibold">Fikir Paylaş</h3>
                <button id="close-share-modal-button" class="p-1 rounded-full hover:bg-gray-700"><i data-lucide="x" class="w-5 h-5"></i></button>
            </div>
            <div class="p-4 space-y-4 flex-1 overflow-y-auto">
                 <div id="share-image-container" class="border border-gray-700 rounded-md p-2 space-y-2">
                    <div id="share-image-viewport" class="w-full h-80 bg-black rounded-md overflow-hidden cursor-grab active:cursor-grabbing relative">
                        <img id="share-image-preview" src="" alt="Grafik Görüntüsü" class="w-full h-full object-contain transition-transform duration-200">
                    </div>
                    <div class="flex items-center justify-center gap-2">
                        <button id="zoom-in-btn" class="p-2 hover:bg-gray-700 rounded-md" title="Yakınlaş"><i data-lucide="zoom-in" class="w-5 h-5"></i></button>
                        <button id="zoom-out-btn" class="p-2 hover:bg-gray-700 rounded-md" title="Uzaklaş"><i data-lucide="zoom-out" class="w-5 h-5"></i></button>
                        <button id="reset-zoom-btn" class="p-2 hover:bg-gray-700 rounded-md" title="Sıfırla"><i data-lucide="rotate-cw" class="w-5 h-5"></i></button>
                    </div>
                </div>
                <div>
                    <label for="share-title" class="block text-sm font-medium text-gray-400 mb-1">Başlık</label>
                    <input type="text" id="share-title" required class="w-full bg-gray-900 border border-gray-700 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
                </div>
                 <div>
                    <label for="share-description" class="block text-sm font-medium text-gray-400 mb-1">Açıklama</label>
                    <textarea id="share-description" rows="4" class="w-full bg-gray-900 border border-gray-700 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-y"></textarea>
                </div>
                 <div>
                    <label for="share-video-url" class="block text-sm font-medium text-gray-400 mb-1">Video Linki (Opsiyonel)</label>
                    <input type="url" id="share-video-url" placeholder="https://www.youtube.com/..." class="w-full bg-gray-900 border border-gray-700 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
                </div>
            </div>
            <div class="flex justify-end gap-3 p-4 border-t border-gray-700">
                <button type="button" id="cancel-share-button" class="px-4 py-2 text-sm rounded-md hover:bg-gray-700">İptal</button>
                <button type="button" id="publish-share-button" class="px-4 py-2 text-sm bg-blue-600 hover:bg-blue-700 text-white rounded-md">Paylaş</button>
            </div>
             <div class="modal-resizer"></div>
        </div>
    </div>
    
    <div id="confirmation-modal" class="fixed inset-0 bg-black bg-opacity-70 items-center justify-center z-50 hidden">
        <div class="bg-gray-800 rounded-lg shadow-xl w-full max-w-sm p-6">
            <h3 id="confirmation-title" class="text-lg font-semibold mb-4">Onay</h3>
            <p id="confirmation-message" class="text-gray-300 mb-6"></p>
            <div class="flex justify-end gap-3">
                <button type="button" id="confirm-cancel-button" class="px-4 py-2 text-sm rounded-md hover:bg-gray-700">İptal</button>
                <button type="button" id="confirm-ok-button" class="px-4 py-2 text-sm bg-red-600 hover:bg-red-700 text-white rounded-md">Sil</button>
            </div>
        </div>
    </div>

    <div id="idea-view-modal" class="fixed inset-0 bg-black bg-opacity-80 items-center justify-center z-50 hidden">
        <div class="bg-gray-800 rounded-lg shadow-xl w-full max-w-4xl flex flex-col h-[90vh] relative">
            <div class="flex justify-between items-center p-3 border-b border-gray-700">
                <h3 id="idea-view-title" class="text-xl font-semibold">Fikir Detayı</h3>
                <button id="close-idea-view-modal-button" class="p-1 rounded-full hover:bg-gray-700"><i data-lucide="x" class="w-5 h-5"></i></button>
            </div>
            <div class="flex-1 flex overflow-hidden">
                <div class="w-2/3 p-4 overflow-y-auto">
                    <img id="idea-view-image" src="" alt="Grafik Fikri" class="w-full h-auto rounded-md">
                    <div id="idea-view-video-container" class="mt-4 aspect-video hidden"></div>
                </div>
                <div class="w-1/3 border-l border-gray-700 flex flex-col">
                    <div class="p-3 border-b border-gray-700">
                        <p class="text-sm text-gray-400">Paylaşan: <span id="idea-view-author" class="font-semibold text-gray-200"></span></p>
                        <p id="idea-view-description" class="text-sm mt-2"></p>
                    </div>
                    <div id="idea-view-comments" class="flex-1 p-3 overflow-y-auto">
                        <!-- Yorumlar buraya gelecek -->
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Toast Notification -->
    <div id="toast-container" class="fixed top-5 right-5 z-50"></div>

    <!-- Firebase SDK -->
    <script type="module">
        import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
        import { getAuth, signInAnonymously, signInWithCustomToken } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-auth.js";
        import { getFirestore, collection, addDoc, query, where, orderBy, onSnapshot, serverTimestamp, doc, setDoc, updateDoc, deleteDoc, arrayUnion, arrayRemove, increment } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";
        
        const appId = typeof __app_id !== 'undefined' ? __app_id : 'default-app-id';
        const firebaseConfig = typeof __firebase_config !== 'undefined' ? JSON.parse(__firebase_config) : {};
        const initialAuthToken = typeof __initial_auth_token !== 'undefined' ? __initial_auth_token : null;

        try {
            const app = initializeApp(firebaseConfig);
            const auth = getAuth(app);
            const db = getFirestore(app);

            window.firebaseTools = { auth, db, collection, addDoc, query, where, orderBy, onSnapshot, serverTimestamp, doc, setDoc, updateDoc, deleteDoc, arrayUnion, arrayRemove, increment };
            window.appId = appId;

            if (initialAuthToken) {
                await signInWithCustomToken(auth, initialAuthToken);
            } else {
                await signInAnonymously(auth);
            }
        } catch(error) {
            console.error("Firebase init error:", error);
            window.firebaseTools = {};
        }
    </script>
    
    <script>
        window.addEventListener('load', () => {
             setTimeout(() => {
                lucide.createIcons();
            }, 50);

            // --- GLOBAL DEĞİŞKENLER ---
            const appId = window.appId || 'default-app-id';
            let chartInstances = [];
            let activeChartInstance = null;
            let watchlistData = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'XRPUSDT'];
            let allSymbols = [];
            let liveTickerData = new Map();
            let binanceSocket;
            let lastPrices = {};
            let chartBackgroundColor = '#131722';
            let chartTextColor = '#d1d4dc';
            let crosshairColor = '#9598a1';
            let crosshairWidth = 1;
            let crosshairStyle = 0; // LightweightCharts.LineStyle.Solid
            let chatListeners = { publicUnsub: null, usersUnsub: null, privateUnsub: null, ideasUnsub: null, commentsUnsub: {}, statusInterval: null };
            
            const BlockedUsersManager = {
                users: [],
                load() {
                    const saved = localStorage.getItem('ersinTeknikBlockedUsers');
                    this.users = saved ? JSON.parse(saved) : [];
                },
                save() {
                    localStorage.setItem('ersinTeknikBlockedUsers', JSON.stringify(this.users));
                },
                isBlocked(userId) {
                    return this.users.includes(userId);
                },
                toggleBlock(userId, username) {
                    if (this.isBlocked(userId)) {
                        this.users = this.users.filter(id => id !== userId);
                        AlarmManager.showNotification(`${username} adlı kullanıcının engeli kaldırıldı.`);
                    } else {
                        this.users.push(userId);
                        AlarmManager.showNotification(`${username} adlı kullanıcı engellendi.`);
                    }
                    this.save();
                }
            };
            BlockedUsersManager.load();

            // --- MERKEZİ GRAFİK SENKRONİZASYON SERVİSİ ---
            const ChartSyncService = {
                charts: new Set(),
                _isSyncing: false,

                add(chart) {
                    if (!chart || this.charts.has(chart)) return;
                    this.charts.add(chart);
                    this._subscribeToEvents(chart);
                },

                remove(chart) {
                    this.charts.delete(chart);
                },
                
                clear() {
                    this.charts.clear();
                },

                _subscribeToEvents(chart) {
                    chart.timeScale().subscribeVisibleLogicalRangeChange(range => {
                        if (this._isSyncing || !range) return;
                        this._isSyncing = true;
                        this.charts.forEach(otherChart => {
                            if (otherChart !== chart) {
                                otherChart.timeScale().setVisibleLogicalRange(range);
                            }
                        });
                        this._isSyncing = false;
                    });
                    
                    chart.subscribeCrosshairMove(param => {
                        if (this._isSyncing || !param.point) {
                            return;
                        }
                        this._isSyncing = true;
                        
                        const timeToSync = param.time;

                        this.charts.forEach(otherChart => {
                            if (otherChart !== chart) {
                                otherChart.applyOptions({
                                    crosshair: {
                                        time: timeToSync,
                                    },
                                });
                            }
                        });
                        
                        this._isSyncing = false;
                    });
                }
            };

            let userStatusCache = new Map();
            // Replay Modu Değişkenleri
            let isInReplayMode = false;
            let isReplaySelectionActive = false;
            let fullReplayData = [];
            let replayCurrentIndex = 0;
            let replayIntervalId = null;
            let replaySpeed = 500;
            let replayStartLine = null;
            let replayOriginalVisibleRange = null;

            // --- TEKRAR OYNATMA (REPLAY) FONKSİYONLARI ---
            function enterReplaySelectionMode() {
                if (!activeChartInstance) return;
                if (isInReplayMode) {
                    AlarmManager.showNotification("Lütfen önce mevcut tekrar oynatmayı sonlandırın.");
                    return;
                }
                isReplaySelectionActive = true;
                AlarmManager.showNotification("Tekrar oynatmayı başlatmak için grafik üzerinde bir başlangıç noktası seçin.");
                activeChartInstance.chart.applyOptions({
                    crosshair: {
                        vertLine: { style: LightweightCharts.LineStyle.Dotted, color: '#2563EB' },
                        horzLine: { style: LightweightCharts.LineStyle.Dotted, color: '#2563EB' },
                    }
                });
                activeChartInstance.container.style.cursor = 'crosshair';
            }

            function startReplay(startTime) {
                if (!activeChartInstance) return;

                isReplaySelectionActive = false;
                activeChartInstance.container.style.cursor = 'default';
                applyCrosshairSettings(crosshairColor, crosshairWidth, crosshairStyle);

                const startIndex = activeChartInstance.candleData.findIndex(d => d.time === startTime);
                if (startIndex < 10) {
                    AlarmManager.showNotification("Lütfen daha ileri bir başlangıç noktası seçin.");
                    return;
                }

                isInReplayMode = true;
                fullReplayData = [...activeChartInstance.candleData];
                replayCurrentIndex = startIndex;

                const replayData = fullReplayData.slice(0, replayCurrentIndex + 1);
                activeChartInstance.series.setData(replayData);

                replayOriginalVisibleRange = activeChartInstance.chart.timeScale().getVisibleLogicalRange();
                
                const timeScale = activeChartInstance.chart.timeScale();
                timeScale.scrollToPosition(replayCurrentIndex - 5, false);

                if (replayStartLine) {
                    try { activeChartInstance.series.removePriceLine(replayStartLine); } catch (e) {}
                }
                replayStartLine = activeChartInstance.series.createPriceLine({
                    price: fullReplayData[replayCurrentIndex].close,
                    color: '#2563EB',
                    lineWidth: 2,
                    lineStyle: LightweightCharts.LineStyle.Dotted,
                    axisLabelVisible: true,
                    title: 'Başlangıç',
                });

                document.getElementById('replay-controls').classList.remove('hidden');
                document.getElementById('replay-button').classList.add('text-blue-500');
                pauseReplay();
            }

            function stepForwardReplay() {
                if (!isInReplayMode || !activeChartInstance) return;
                if (replayCurrentIndex >= fullReplayData.length - 1) {
                    pauseReplay();
                    AlarmManager.showNotification("Veri sonuna ulaşıldı.");
                    return;
                }

                replayCurrentIndex++;
                const nextCandle = fullReplayData[replayCurrentIndex];
                activeChartInstance.series.update(nextCandle);
                activeChartInstance.indicatorManager.updateAllActive(fullReplayData.slice(0, replayCurrentIndex + 1));


                const timeScale = activeChartInstance.chart.timeScale();
                const visibleRange = timeScale.getVisibleLogicalRange();
                if (visibleRange && visibleRange.to < replayCurrentIndex + 10) {
                    timeScale.scrollToPosition(replayCurrentIndex - 5, true);
                }
            }

            function playReplay() {
                if (replayIntervalId) clearInterval(replayIntervalId);
                replayIntervalId = setInterval(stepForwardReplay, replaySpeed);
                const btn = document.getElementById('replay-play-pause');
                btn.dataset.state = 'playing';
                btn.title = 'Duraklat';
                btn.innerHTML = '<i data-lucide="pause" class="w-5 h-5"></i>';
                lucide.createIcons();
            }

            function pauseReplay() {
                if (replayIntervalId) clearInterval(replayIntervalId);
                replayIntervalId = null;
                const btn = document.getElementById('replay-play-pause');
                btn.dataset.state = 'paused';
                btn.title = 'Oynat';
                btn.innerHTML = '<i data-lucide="play" class="w-5 h-5"></i>';
                lucide.createIcons();
            }

            function exitReplayMode() {
                if (!isInReplayMode && !isReplaySelectionActive) return;

                pauseReplay();
                isInReplayMode = false;
                isReplaySelectionActive = false;

                if (activeChartInstance) {
                    activeChartInstance.series.setData(fullReplayData);
                    if (replayStartLine) {
                        try { activeChartInstance.series.removePriceLine(replayStartLine); } catch (e) {}
                        replayStartLine = null;
                    }

                    if (replayOriginalVisibleRange) {
                        activeChartInstance.chart.timeScale().setVisibleLogicalRange(replayOriginalVisibleRange);
                    }

                    activeChartInstance.container.style.cursor = 'default';
                    applyCrosshairSettings(crosshairColor, crosshairWidth, crosshairStyle);
                    activeChartInstance.indicatorManager.updateAllActive(fullReplayData);
                }
                
                fullReplayData = [];
                replayCurrentIndex = 0;

                document.getElementById('replay-controls').classList.add('hidden');
                document.getElementById('replay-button').classList.remove('text-blue-500');
            }

            // --- ZAMAN DİLİMİ YÖNETİCİSİ ---
            const TimeframeManager = {
                timeframes: [],
                
                load() {
                    const saved = localStorage.getItem('ersinTeknikCustomTimeframes');
                    this.timeframes = saved ? JSON.parse(saved) : [];
                    this.render();
                },
                save() {
                    localStorage.setItem('ersinTeknikCustomTimeframes', JSON.stringify(this.timeframes));
                },
                add(value, unit) {
                    const defaultTimeframes = ['5m', '15m', '30m', '1h', '4h', '1d', '1M'];
                    const newTimeframeId = `${value}${unit}`;
                    const newTimeframeText = unit === 'd' ? `${value}D` : `${value}${unit}`;

                    if (defaultTimeframes.includes(newTimeframeId)) {
                        const defaultButton = document.querySelector(`#time-menu-dropdown button[data-timeframe="${newTimeframeId}"]`);
                        if (defaultButton) defaultButton.click();
                        return;
                    }

                    if (this.timeframes.some(tf => tf.id === newTimeframeId)) {
                        const existingButton = document.querySelector(`.custom-timeframe-wrapper button[data-timeframe="${newTimeframeId}"]`);
                        if(existingButton) existingButton.click();
                        return;
                    }
                    
                    this.timeframes.push({ id: newTimeframeId, text: newTimeframeText });
                    this.save();
                    const newButtonWrapper = this.createButtonElement({ id: newTimeframeId, text: newTimeframeText });
                    const container = document.querySelector('#time-menu-dropdown .flex.items-center.space-x-1');
                    container.appendChild(newButtonWrapper);
                    
                    newButtonWrapper.querySelector('button.timeframe-item').click();
                },
                remove(timeframeId) {
                    this.timeframes = this.timeframes.filter(tf => tf.id !== timeframeId);
                    this.save();
                    const buttonWrapperToRemove = document.querySelector(`.custom-timeframe-wrapper[data-timeframe-id="${timeframeId}"]`);
                    if (buttonWrapperToRemove) buttonWrapperToRemove.remove();
                },
                createButtonElement(tf) {
                    const wrapper = document.createElement('div');
                    wrapper.className = 'custom-timeframe-wrapper group relative';
                    wrapper.dataset.timeframeId = tf.id;

                    const button = document.createElement('button');
                    button.className = 'timeframe-item px-3 py-1 text-sm rounded-md hover:bg-gray-700';
                    button.dataset.timeframe = tf.id;
                    button.textContent = tf.text;
                    
                    button.addEventListener('click', (event) => {
                        event.preventDefault();
                        document.querySelectorAll('.timeframe-item').forEach(i => i.classList.remove('active-timeframe'));
                        button.classList.add('active-timeframe');
                        document.querySelector('#time-menu-button span').textContent = button.textContent;
                        document.getElementById('time-menu-dropdown').classList.add('hidden');
                        updateAllCharts(activeChartInstance.symbol, button.dataset.timeframe);
                    });
                    
                    const deleteBtn = document.createElement('button');
                    deleteBtn.className = 'absolute -top-1.5 -right-1.5 p-0.5 bg-red-600 rounded-full text-white opacity-0 group-hover:opacity-100 transition-opacity z-10 hover:bg-red-700';
                    deleteBtn.title = 'Kısayolu kaldır';
                    deleteBtn.innerHTML = '<i data-lucide="x" class="w-3 h-3"></i>';
                    
                    deleteBtn.addEventListener('click', (e) => {
                        e.stopPropagation();
                        this.remove(tf.id);
                    });
                    
                    wrapper.appendChild(button);
                    wrapper.appendChild(deleteBtn);
                    lucide.createIcons();
                    return wrapper;
                },
                render() {
                    const container = document.querySelector('#time-menu-dropdown .flex.items-center.space-x-1');
                    container.querySelectorAll('.custom-timeframe-wrapper').forEach(wrapper => wrapper.remove());
                    
                    this.timeframes.forEach(tf => {
                        const buttonWrapper = this.createButtonElement(tf);
                        container.appendChild(buttonWrapper);
                    });
                }
            };

            // --- ALARM YÖNETİCİSİ ---
            const AlarmManager = {
                alarms: [],
                add(symbol, price) {
                    if (!activeChartInstance) return;
                    const id = `alarm_${Date.now()}`;
                    const priceLine = activeChartInstance.series.createPriceLine({
                        price: price, color: '#f59e0b', lineWidth: 2, lineStyle: LightweightCharts.LineStyle.Dashed,
                        axisLabelVisible: true, title: `🔔 ${price}`
                    });
                    this.alarms.push({ id, symbol, price, priceLine, chartId: activeChartInstance.id });
                    this.renderAlarmsList();
                },
                remove(alarmId) {
                    const alarmIndex = this.alarms.findIndex(a => a.id === alarmId);
                    if (alarmIndex > -1) {
                        const alarm = this.alarms[alarmIndex];
                        const chartInstance = chartInstances.find(ci => ci.id === alarm.chartId);
                        if (chartInstance) {
                            try { chartInstance.series.removePriceLine(alarm.priceLine); } catch (e) { console.warn("Price line already removed."); }
                        }
                        this.alarms.splice(alarmIndex, 1);
                        this.renderAlarmsList();
                    }
                },
                checkAllAlarms() {
                     this.alarms.forEach(alarm => {
                        const ticker = liveTickerData.get(alarm.symbol);
                        if (ticker) {
                            const price = parseFloat(ticker.c);
                            const prevPrice = lastPrices[alarm.symbol] || price;
                            const crossesUp = prevPrice < alarm.price && price >= alarm.price;
                            const crossesDown = prevPrice > alarm.price && price <= alarm.price;
                            if (crossesUp || crossesDown) {
                                this.triggerAlarm(alarm);
                            }
                            lastPrices[alarm.symbol] = price;
                        }
                    });
                },
                triggerAlarm(alarm) {
                    this.showNotification(`Alarm Tetiklendi: ${alarm.symbol} fiyatı ${alarm.price} seviyesini geçti!`);
                    this.playAlertSound();
                    this.remove(alarm.id);
                },
                renderAlarmsList() {
                    const listEl = document.getElementById('alarms-list');
                    if (!listEl) return;
                    listEl.innerHTML = '';
                    if (this.alarms.length === 0) {
                        listEl.innerHTML = `<p class="text-center text-gray-500 p-4">Aktif alarm yok.</p>`;
                        return;
                    }
                    this.alarms.forEach(alarm => {
                        const item = document.createElement('div');
                        item.className = 'flex justify-between items-center p-3 border-b border-gray-700';
                        item.innerHTML = `<div><span class="font-bold">${alarm.symbol}</span> <span class="text-gray-400"> > ${alarm.price}</span></div>
                            <button data-alarm-id="${alarm.id}" class="remove-alarm-btn p-1 text-gray-500 hover:text-red-500"><i data-lucide="trash-2" class="w-4 h-4"></i></button>`;
                        listEl.appendChild(item);
                    });
                    listEl.querySelectorAll('.remove-alarm-btn').forEach(btn => btn.addEventListener('click', () => this.remove(btn.dataset.alarmId)));
                    lucide.createIcons();
                },
                showNotification(message) {
                    const toastContainer = document.getElementById('toast-container');
                    const toast = document.createElement('div');
                    toast.className = 'bg-blue-600 text-white px-6 py-3 rounded-lg shadow-lg animate-pulse';
                    toast.textContent = message;
                    toastContainer.appendChild(toast);
                    setTimeout(() => toast.remove(), 5000);
                },
                playAlertSound() {
                    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
                    const oscillator = audioContext.createOscillator(); const gainNode = audioContext.createGain();
                    oscillator.connect(gainNode); gainNode.connect(audioContext.destination);
                    oscillator.type = 'sine'; oscillator.frequency.setValueAtTime(440, audioContext.currentTime);
                    gainNode.gain.setValueAtTime(0.5, audioContext.currentTime);
                    oscillator.start(); oscillator.stop(audioContext.currentTime + 0.3);
                },
                redrawAllAlarmLines() {
                    this.alarms.forEach(alarm => {
                        const chartInstance = chartInstances.find(ci => ci.id === alarm.chartId);
                        if (chartInstance) {
                            try { chartInstance.series.removePriceLine(alarm.priceLine); } catch(e) {}
                            alarm.priceLine = chartInstance.series.createPriceLine({
                                price: alarm.price, color: alarm.symbol === chartInstance.symbol ? '#f59e0b' : 'transparent',
                                lineWidth: 2, lineStyle: LightweightCharts.LineStyle.Dashed,
                                axisLabelVisible: alarm.symbol === chartInstance.symbol,
                                title: alarm.symbol === chartInstance.symbol ? `🔔 ${alarm.price}` : ''
                            });
                        }
                    });
                }
            };
            
            // --- GÖSTERGE YÖNETİCİSİ VE KÜTÜPHANESİ ---
            const IndicatorLibrary = {};
            function createIndicatorManager(chartInstance) {
                return {
                    activeIndicators: {},
                    calculationCache: new Map(),
                    chartInstance: chartInstance,
                    getCacheKey(indicatorId, settings) {
                        return `${indicatorId}-${this.chartInstance.symbol}-${this.chartInstance.interval}-${JSON.stringify(settings)}`;
                    },
                    toggle(indicatorId) {
                        const button = document.querySelector(`#indicators-dropdown [data-indicator-id="${indicatorId}"]`);
                        const checkIcon = button ? button.querySelector('i, svg') : null;
                        if (this.activeIndicators[indicatorId]) {
                            this.remove(indicatorId);
                            if (checkIcon) checkIcon.classList.add('invisible');
                        } else {
                            this.add(indicatorId);
                            if (checkIcon) checkIcon.classList.remove('invisible');
                        }
                    },
                    add(indicatorId) {
                        const indicator = IndicatorLibrary[indicatorId];
                        if (!indicator) return;

                        // Her gösterge örneği için ayarların bir kopyasını oluştur
                        const instanceSettings = JSON.parse(JSON.stringify(indicator.settings));

                        if (indicator.type === 'pane') {
                            const resizer = document.createElement('div');
                            resizer.className = 'resizer-h';
                            addResizeListener(resizer);

                            const paneContainer = document.createElement('div');
                            paneContainer.id = `pane-${indicatorId}-${this.chartInstance.id}`;
                            paneContainer.className = 'indicator-pane-container flex-1';
                            paneContainer.style.minHeight = '80px';

                            this.chartInstance.container.appendChild(resizer);
                            this.chartInstance.container.appendChild(paneContainer);

                            const { series, uiElement, paneChart } = indicator.init(this.chartInstance, paneContainer);
                            this.activeIndicators[indicatorId] = { id: indicatorId, series, uiElement, definition: indicator, paneChart, paneContainer, resizer, settings: instanceSettings };
                            
                            this.update(indicatorId, this.chartInstance.candleData);
                            
                            setTimeout(resizeHandler, 50);

                        } else { // 'overlay'
                            const { series, uiElement } = indicator.init(this.chartInstance);
                            this.activeIndicators[indicatorId] = { id: indicatorId, series, uiElement, definition: indicator, settings: instanceSettings };
                            this.update(indicatorId, this.chartInstance.candleData);
                        }
                    },
                    update(indicatorId, dataToProcess) {
                        const active = this.activeIndicators[indicatorId]; if (!active) return;
                        const indicator = active.definition; let calculatedData;
                        if (isInReplayMode && activeChartInstance.id === this.chartInstance.id) {
                            calculatedData = indicator.calculate(dataToProcess, active.settings);
                        } else {
                            const cacheKey = this.getCacheKey(indicator.id, active.settings);
                            if (this.calculationCache.has(cacheKey)) {
                                calculatedData = this.calculationCache.get(cacheKey);
                            } else {
                                calculatedData = indicator.calculate(dataToProcess, active.settings);
                                this.calculationCache.set(cacheKey, calculatedData);
                            }
                        }
                        indicator.update(active.series, calculatedData);
                    },
                    remove(indicatorId) {
                        const active = this.activeIndicators[indicatorId]; if (!active) return;
                        
                        active.definition.remove(this.chartInstance.chart, active.series, active.uiElement, active.paneChart);
                        
                        if (active.definition.type === 'pane') {
                            active.paneContainer?.remove();
                            active.resizer?.remove();
                            setTimeout(resizeHandler, 50);
                        }

                        delete this.activeIndicators[indicatorId];
                    },
                    updateAllActive(dataToProcess) {
                        for (const id in this.activeIndicators) this.update(id, dataToProcess);
                    },
                    clearCache() { this.calculationCache.clear(); },
                    removeAll() { for (const id in this.activeIndicators) this.remove(id); }
                };
            }

            // --- GÖSTERGE TANIMLAMALARI (STATİK) ---
            const maIndicator = {
                id: 'ma', name: 'Hareketli Ortalama (MA)', type: 'overlay', settings: { period: 20 },
                init: function(chartInstance) {
                    const chart = chartInstance.chart;
                    const series = chart.addLineSeries({ color: 'rgba(255, 165, 0, 0.8)', lineWidth: 2, lastValueVisible: false, priceLineVisible: false });
                    const uiElement = this.createLabel(chartInstance); // chartInstance'ı gönder
                    return { series, uiElement };
                },
                calculate: function(data, settings) { // settings parametresi eklendi
                    const result = [];
                    const period = settings.period || this.settings.period;
                    for (let i = period - 1; i < data.length; i++) {
                        let sum = 0;
                        for (let j = 0; j < period; j++) sum += data[i - j].close;
                        result.push({ time: data[i].time, value: sum / period });
                    }
                    return result;
                },
                update: (series, data) => series.setData(data),
                remove: (chart, series, uiElement) => { 
                    try {
                        if(series) chart.removeSeries(series); 
                    } catch(e) { console.warn('Series already removed'); }
                    if (uiElement) uiElement.remove(); 
                },
                createLabel(chartInstance) { // chartInstance parametresi eklendi
                    const container = chartInstance.mainPane;
                    let labelsContainer = container.querySelector('.indicator-labels-container');
                    if (!labelsContainer) {
                        labelsContainer = document.createElement('div');
                        labelsContainer.className = 'indicator-labels-container';
                        container.appendChild(labelsContainer);
                    }
                    const el = document.createElement('div');
                    el.className = 'bg-gray-900 bg-opacity-70 px-2 py-1 rounded-md flex items-center gap-2 text-sm';
                    const settings = chartInstance.indicatorManager.activeIndicators[this.id]?.settings || this.settings;
                    el.innerHTML = `
                        <button class="settings-indicator-btn p-1 -ml-1 rounded-md hover:bg-gray-700" title="Ayarlar"><i data-lucide="settings" class="w-4 h-4"></i></button>
                        <span class="indicator-name-span">${this.name} (${settings.period})</span>
                        <button class="remove-indicator-btn p-1 -mr-1 rounded-md hover:bg-gray-700" title="Kaldır"><i data-lucide="x" class="w-4 h-4"></i></button>
                    `;
                    labelsContainer.appendChild(el);
                    lucide.createIcons();
                    el.querySelector('.remove-indicator-btn').addEventListener('click', e => { e.stopPropagation(); chartInstance.indicatorManager.toggle(this.id); });
                    el.querySelector('.settings-indicator-btn').addEventListener('click', e => { e.stopPropagation(); openIndicatorSettingsModal(this.id, chartInstance); });
                    return el;
                }
            };
            const rsiIndicator = {
                id: 'rsi', name: 'Göreceli Güç Endeksi (RSI)', type: 'pane', settings: { period: 14 },
                init: function(mainChartInstance, paneContainer) {
                    const mainChart = mainChartInstance.chart;
                    
                    const paneChart = LightweightCharts.createChart(paneContainer, {
                        layout: { background: { color: chartBackgroundColor }, textColor: chartTextColor },
                        grid: { vertLines: { visible: false }, horzLines: { color: 'rgba(255,255,255,0.1)' } },
                        timeScale: { visible: false, borderColor: '#485c7b' },
                        crosshair: {
                            mode: LightweightCharts.CrosshairMode.Normal, // Normal crosshair mode
                        },
                    });

                    // Pane grafiğini genel senkronizasyon servisine ekle
                    ChartSyncService.add(paneChart);

                    const series = paneChart.addLineSeries({ color: '#c771d2', lineWidth: 2, lastValueVisible: false, priceLineVisible: false });
                    series.createPriceLine({ price: 70, color: '#ef5350', lineWidth: 1, lineStyle: LightweightCharts.LineStyle.Dashed, axisLabelVisible: true, title: '70' });
                    series.createPriceLine({ price: 30, color: '#26a69a', lineWidth: 1, lineStyle: LightweightCharts.LineStyle.Dashed, axisLabelVisible: true, title: '30' });
                    
                    const uiElement = this.createLabel(mainChartInstance); // mainChartInstance'ı gönder
                    
                    return { series, uiElement, paneChart };
                },
                calculate: function(data, settings) { // settings parametresi eklendi
                    let result = [];
                    let changes = data.map((d, i) => i > 0 ? d.close - data[i - 1].close : 0);
                    let gains = changes.map(c => c > 0 ? c : 0);
                    let losses = changes.map(c => c < 0 ? Math.abs(c) : 0);
                    let avgGain = 0, avgLoss = 0;
                    const period = settings.period || this.settings.period;
                    for (let i = 0; i < data.length; i++) {
                        if (i < period) {
                            result.push({ time: data[i].time, value: undefined });
                            avgGain += gains[i]; avgLoss += losses[i];
                            if (i === period - 1) { avgGain /= period; avgLoss /= period; }
                        } else {
                            avgGain = (avgGain * (period - 1) + gains[i]) / period;
                            avgLoss = (avgLoss * (period - 1) + losses[i]) / period;
                            if (avgLoss === 0) result.push({ time: data[i].time, value: 100 });
                            else { const rs = avgGain / avgLoss; result.push({ time: data[i].time, value: 100 - (100 / (1 + rs)) }); }
                        }
                    }
                    return result;
                },
                update: (series, data) => series.setData(data),
                remove: function(mainChart, series, uiElement, paneChart) {
                    if (paneChart) {
                        ChartSyncService.remove(paneChart); // Senkronizasyondan kaldır
                        paneChart.remove();
                    }
                    if (uiElement) uiElement.remove();
                },
                createLabel: maIndicator.createLabel // maIndicator'daki createLabel fonksiyonunu yeniden kullan
            };
            IndicatorLibrary['ma'] = maIndicator;
            IndicatorLibrary['rsi'] = rsiIndicator;
            
            function showConfirmationModal(message, onConfirm) {
                const modal = document.getElementById('confirmation-modal');
                const messageEl = document.getElementById('confirmation-message');
                const okButton = document.getElementById('confirm-ok-button');
                const cancelButton = document.getElementById('confirm-cancel-button');
                
                messageEl.textContent = message;
                modal.style.display = 'flex';

                const closeHandler = () => {
                    modal.style.display = 'none';
                    okButton.removeEventListener('click', confirmHandler);
                    cancelButton.removeEventListener('click', closeHandler);
                };
                
                const confirmHandler = () => {
                    onConfirm();
                    closeHandler();
                };
                
                okButton.addEventListener('click', confirmHandler, { once: true });
                cancelButton.addEventListener('click', closeHandler, { once: true });
            }

            function openIndicatorSettingsModal(indicatorId, chartInstance) {
                const modal = document.getElementById('indicator-settings-modal');
                const titleEl = document.getElementById('indicator-settings-title');
                const fieldsEl = document.getElementById('indicator-settings-fields');
                const saveButton = document.getElementById('save-indicator-settings-button');
                const cancelButton = document.getElementById('cancel-indicator-settings-button');

                const indicator = IndicatorLibrary[indicatorId];
                const activeIndicator = chartInstance.indicatorManager.activeIndicators[indicatorId];
                if (!indicator || !activeIndicator) return;

                titleEl.textContent = `${indicator.name} Ayarları`;
                fieldsEl.innerHTML = '';

                // Mevcut ayarları modal'a yükle
                for (const key in activeIndicator.settings) {
                    const value = activeIndicator.settings[key];
                    const settingDiv = document.createElement('div');
                    settingDiv.className = 'flex items-center justify-between';
                    settingDiv.innerHTML = `
                        <label for="setting-${key}" class="text-gray-300 capitalize">${key}</label>
                        <input type="number" id="setting-${key}" data-key="${key}" value="${value}" class="w-24 bg-gray-900 border border-gray-700 rounded-md px-2 py-1 focus:outline-none focus:ring-1 focus:ring-blue-500">
                    `;
                    fieldsEl.appendChild(settingDiv);
                }
                
                modal.style.display = 'flex';

                const onSave = () => {
                    const newSettings = {};
                    fieldsEl.querySelectorAll('input').forEach(input => {
                        newSettings[input.dataset.key] = Number(input.value);
                    });

                    // Ayarları güncelle
                    activeIndicator.settings = newSettings;
                    
                    // Etiketi güncelle
                    const labelSpan = activeIndicator.uiElement.querySelector('.indicator-name-span');
                    if (labelSpan) {
                         labelSpan.textContent = `${indicator.name} (${Object.values(newSettings).join(', ')})`;
                    }
                    
                    // Göstergeyi yeni ayarlarla yeniden hesapla ve çiz
                    chartInstance.indicatorManager.update(indicatorId, chartInstance.candleData);

                    modal.style.display = 'none';
                    cleanup();
                };
                
                const cleanup = () => {
                    saveButton.removeEventListener('click', onSave);
                    cancelButton.removeEventListener('click', cleanupAndClose);
                    modal.removeEventListener('click', modalClose);
                };

                const cleanupAndClose = () => {
                    modal.style.display = 'none';
                    cleanup();
                };
                
                const modalClose = (e) => {
                    if (e.target === modal) cleanupAndClose();
                };

                saveButton.addEventListener('click', onSave, { once: true });
                cancelButton.addEventListener('click', cleanupAndClose, { once: true });
                modal.addEventListener('click', modalClose);
            }

            function makeModalResizable(modalId) {
                const modalContent = document.getElementById(modalId)?.querySelector('.bg-gray-800');
                const resizer = modalContent?.querySelector('.modal-resizer');
                
                if (!modalContent || !resizer) return;
                
                let isResizing = false;

                resizer.addEventListener('mousedown', function(e) {
                    isResizing = true;
                    let startX = e.clientX;
                    let startY = e.clientY;
                    let startWidth = parseInt(document.defaultView.getComputedStyle(modalContent).width, 10);
                    let startHeight = parseInt(document.defaultView.getComputedStyle(modalContent).height, 10);

                    function doDrag(e) {
                        if (!isResizing) return;
                        modalContent.style.width = (startWidth + e.clientX - startX) + 'px';
                        modalContent.style.height = (startHeight + e.clientY - startY) + 'px';
                    }

                    function stopDrag() {
                        isResizing = false;
                        document.removeEventListener('mousemove', doDrag);
                        document.removeEventListener('mouseup', stopDrag);
                    }

                    document.addEventListener('mousemove', doDrag);
                    document.addEventListener('mouseup', stopDrag);
                });
            }

            const chartWrapper = document.getElementById('chart-wrapper');

            // --- SAĞ PANEL YÖNETİCİSİ ---
            const RightPanelManager = {
                activePanel: null,
                togglePanel(panelId) {
                    const contentEl = document.getElementById('right-panel-content');
                    const tabs = document.querySelectorAll('.right-panel-tab');

                    // If clicking the active panel's tab, close it.
                    if (this.activePanel === panelId) {
                        contentEl.classList.add('hidden');
                        contentEl.innerHTML = '';
                        tabs.forEach(t => t.classList.remove('active'));
                        this.activePanel = null;
                        setTimeout(resizeHandler, 10);
                        return;
                    }

                    this.activePanel = panelId;
                    contentEl.classList.remove('hidden');
                    tabs.forEach(t => t.classList.toggle('active', t.dataset.panel === panelId));

                    this.renderPanelContent(panelId);
                    setTimeout(resizeHandler, 10);
                },
                renderPanelContent(panelId) {
                     const contentEl = document.getElementById('right-panel-content');
                     contentEl.innerHTML = ''; // Clear previous content
                     
                     switch (panelId) {
                        case 'watchlist':
                            contentEl.innerHTML = `
                                <div class="p-2 flex-shrink-0 border-b border-gray-700">
                                    <h3 class="text-lg font-semibold">İzleme Listesi</h3>
                                </div>
                                <ul id="watchlist" class="flex-1 overflow-y-auto p-1"></ul>
                                <div class="p-2 border-t border-gray-700">
                                    <button id="add-symbol-button" class="w-full flex items-center justify-center gap-2 p-2 text-sm bg-blue-600 hover:bg-blue-700 rounded-md">
                                        <i data-lucide="plus" class="w-4 h-4"></i> Sembol Ekle
                                    </button>
                                </div>`;
                            renderWatchlist();
                            document.getElementById('add-symbol-button').addEventListener('click', () => {
                                document.getElementById('add-symbol-modal').style.display = 'flex';
                            });
                            break;
                        case 'notes':
                            contentEl.innerHTML = `
                                <div class="p-2 flex-shrink-0 border-b border-gray-700 flex justify-between items-center">
                                    <h3 class="text-lg font-semibold">Notlar</h3>
                                    <div>
                                        <button id="add-note-btn" title="Yeni Not Ekle" class="p-1.5 hover:bg-gray-700 rounded-md"><i data-lucide="plus" class="w-4 h-4"></i></button>
                                        <button id="save-notes-btn" title="Notları Kaydet" class="p-1.5 hover:bg-gray-700 rounded-md"><i data-lucide="save" class="w-4 h-4"></i></button>
                                    </div>
                                </div>
                                <div id="notes-list" class="flex-1 overflow-y-auto p-2 space-y-2"></div>`;
                            NotesManager.load();
                            NotesManager.render();
                            document.getElementById('add-note-btn').addEventListener('click', () => NotesManager.add());
                            document.getElementById('save-notes-btn').addEventListener('click', () => NotesManager.save());
                            break;
                        case 'alarms':
                             contentEl.innerHTML = `
                                <div class="p-2 flex-shrink-0 border-b border-gray-700">
                                    <h3 class="text-lg font-semibold">Alarmlar</h3>
                                </div>
                                <div id="alarms-list" class="flex-1 overflow-y-auto p-2"></div>`;
                            AlarmManager.renderAlarmsList();
                            break;
                        case 'chat':
                            contentEl.innerHTML = `
                                <div class="flex-shrink-0 border-b border-gray-700">
                                    <div class="flex">
                                        <button id="chat-tab-btn-public" class="flex-1 p-2 text-sm border-b-2 border-blue-500 text-blue-400">Genel</button>
                                        <button id="chat-tab-btn-users" class="flex-1 p-2 text-sm border-b-2 border-transparent text-gray-400 hover:text-gray-200 hover:border-gray-500">Özel</button>
                                    </div>
                                </div>
                                <!-- Public Chat Tab -->
                                <div id="chat-tab-public" class="flex flex-col flex-1 overflow-hidden">
                                    <div id="chat-messages" class="flex-1 p-2 overflow-y-auto flex flex-col-reverse"></div>
                                    <form id="chat-form" class="p-2 border-t border-gray-700">
                                         <div class="relative flex items-center">
                                            <input type="text" id="chat-input" placeholder="Mesaj yaz..." class="w-full bg-gray-900 border border-gray-700 rounded-md px-3 py-1.5 pr-10 focus:outline-none focus:ring-1 focus:ring-blue-500 text-sm">
                                            <button type="submit" class="absolute right-2 p-1.5 rounded-md text-gray-400 hover:text-white hover:bg-blue-600">
                                                 <i data-lucide="send" class="w-4 h-4"></i>
                                            </button>
                                        </div>
                                    </form>
                                </div>
                                <!-- Users List Tab -->
                                <div id="chat-tab-users" class="flex flex-col flex-1 overflow-hidden hidden">
                                     <div class="p-2 border-b border-gray-700">
                                         <input type="text" id="user-search-input" placeholder="Kişi ara..." class="w-full bg-gray-900 border border-gray-700 rounded-md px-2 py-1.5 focus:outline-none focus:ring-1 focus:ring-blue-500 text-sm">
                                     </div>
                                     <div id="user-list-container" class="flex-1 p-1 overflow-y-auto"></div>
                                </div>`;
                            initializeChat();
                            break;
                         case 'sharing':
                             contentEl.innerHTML = `
                                 <div class="p-2 flex-shrink-0 border-b border-gray-700 flex justify-between items-center">
                                     <h3 class="text-lg font-semibold">Fikirler</h3>
                                 </div>
                                 <div class="flex-1 overflow-y-auto p-2 space-y-3">
                                     <div id="ideas-list"></div>
                                 </div>
                                 <div class="p-2 border-t border-gray-700">
                                    <button id="share-idea-button" class="w-full flex items-center justify-center gap-2 p-2 text-sm bg-blue-600 hover:bg-blue-700 rounded-md">
                                        <i data-lucide="share-2" class="w-4 h-4"></i> Fikir Paylaş
                                    </button>
                                 </div>`;
                             IdeaManager.init('everyone');
                             document.getElementById('share-idea-button').addEventListener('click', () => IdeaManager.captureAndShowModal());
                             break;
                         case 'following':
                             contentEl.innerHTML = `
                                 <div class="p-2 flex-shrink-0 border-b border-gray-700">
                                     <h3 class="text-lg font-semibold">Takip Edilenler</h3>
                                 </div>
                                 <div class="flex-1 overflow-y-auto p-2 space-y-3">
                                     <div id="following-ideas-list"></div>
                                 </div>`;
                             IdeaManager.init('following');
                             break;

                        default:
                            contentEl.innerHTML = `<p class="p-4 text-center text-gray-500">${panelId} paneli</p>`;
                     }
                     lucide.createIcons();
                }
            };
            
            function addResizeListener(resizer) {
                let prevSibling = resizer.previousElementSibling;
                let nextSibling = resizer.nextElementSibling;
                if (!prevSibling || !nextSibling) return;
                
                let isResizing = false;

                resizer.addEventListener('mousedown', (e) => {
                    isResizing = true;
                    e.preventDefault(); // Prevent text selection

                    let startX = e.clientX;
                    let startY = e.clientY;
                    let prevStartWidth = prevSibling.offsetWidth;
                    let prevStartHeight = prevSibling.offsetHeight;

                    const doDrag = (e) => {
                        if (!isResizing) return;
                        
                        if (resizer.classList.contains('resizer-v')) { // Vertical resizer
                            const dx = e.clientX - startX;
                            const newPrevWidth = prevStartWidth + dx;
                            prevSibling.style.width = `${newPrevWidth}px`;
                        } else { // Horizontal resizer
                            const dy = e.clientY - startY;
                            const newPrevHeight = prevStartHeight + dy;
                            prevSibling.style.height = `${newPrevHeight}px`;
                        }

                        resizeHandler();
                    };

                    const stopDrag = () => {
                        isResizing = false;
                        document.removeEventListener('mousemove', doDrag);
                        document.removeEventListener('mouseup', stopDrag);
                    };

                    document.addEventListener('mousemove', doDrag);
                    document.addEventListener('mouseup', stopDrag);
                });
            }

            function applyLayout(layout = '1x1') {
                chartInstances.forEach(instance => instance.destroy());
                chartInstances = [];
                ChartSyncService.clear();
                chartWrapper.innerHTML = '';
                chartWrapper.className = 'flex-1 w-full h-full'; // Reset classes

                if (layout === '1x1') {
                    chartWrapper.classList.add('flex', 'flex-col');
                    createChartInstance(chartWrapper, 'chart_0');
                } else if (layout === '2x1') {
                    chartWrapper.classList.add('flex', 'flex-row');
                    const left = document.createElement('div');
                    const right = document.createElement('div');
                    left.className = 'flex-1 h-full flex flex-col';
                    right.className = 'flex-1 h-full flex flex-col';
                    const resizer = document.createElement('div');
                    resizer.className = 'resizer-v';
                    chartWrapper.append(left, resizer, right);
                    addResizeListener(resizer);
                    createChartInstance(left, 'chart_0');
                    createChartInstance(right, 'chart_1');
                } else if (layout === '1x2') {
                    chartWrapper.classList.add('flex', 'flex-col');
                     const top = document.createElement('div');
                    const bottom = document.createElement('div');
                    top.className = 'flex-1 w-full flex flex-col';
                    bottom.className = 'flex-1 w-full flex flex-col';
                    const resizer = document.createElement('div');
                    resizer.className = 'resizer-h';
                    chartWrapper.append(top, resizer, bottom);
                    addResizeListener(resizer);
                    createChartInstance(top, 'chart_0');
                    createChartInstance(bottom, 'chart_1');
                } else if (layout === '1v2h') {
                    chartWrapper.className = 'flex-1 w-full h-full flex flex-row';
                    const leftPanel = document.createElement('div');
                    leftPanel.className = 'flex-1 flex flex-col';
                    chartWrapper.appendChild(leftPanel);
                    createChartInstance(leftPanel, 'chart_0');

                    const resizerV = document.createElement('div');
                    resizerV.className = 'resizer-v';
                    chartWrapper.appendChild(resizerV);
                    addResizeListener(resizerV);

                    const rightPanel = document.createElement('div');
                    rightPanel.className = 'flex-1 flex flex-col';
                    chartWrapper.appendChild(rightPanel);

                    const topRightPanel = document.createElement('div');
                    topRightPanel.className = 'flex-1 flex flex-col';
                    rightPanel.appendChild(topRightPanel);
                    createChartInstance(topRightPanel, 'chart_1');

                    const resizerH = document.createElement('div');
                    resizerH.className = 'resizer-h';
                    rightPanel.appendChild(resizerH);
                    addResizeListener(resizerH);

                    const bottomRightPanel = document.createElement('div');
                    bottomRightPanel.className = 'flex-1 flex flex-col';
                    rightPanel.appendChild(bottomRightPanel);
                    createChartInstance(bottomRightPanel, 'chart_2');
                }
                
                if (chartInstances.length > 0) {
                    setActiveChart(chartInstances[0]);
                    updateAllCharts(activeChartInstance.symbol, activeChartInstance.interval);
                }
            }
             
            function createChartInstance(container, id) {
                container.innerHTML = ''; // Clear container before creating chart
                container.classList.add('chart-instance-container');

                const mainPane = document.createElement('div');
                mainPane.className = 'main-chart-pane flex-grow h-full w-full';
                container.appendChild(mainPane);

                const chart = LightweightCharts.createChart(mainPane, {
                    layout: { background: { color: chartBackgroundColor }, textColor: chartTextColor },
                    grid: { vertLines: { visible: false }, horzLines: { visible: false } },
                    timeScale: { borderColor: '#485c7b' },
                    crosshair: { mode: LightweightCharts.CrosshairMode.Normal },
                    rightPriceScale: { borderColor: '#485c7b' },
                });
                ChartSyncService.add(chart);

                 chart.subscribeClick(param => {
                    if (isReplaySelectionActive && activeChartInstance && activeChartInstance.id === id) {
                        if (param.time) {
                            startReplay(param.time);
                        }
                    }
                });
                const series = chart.addCandlestickSeries({
                    upColor: '#26a69a', downColor: '#ef5350', borderDownColor: '#ef5350',
                    borderUpColor: '#26a69a', wickDownColor: '#ef5350', wickUpColor: '#26a69a',
                    lastValueVisible: false, priceLineVisible: false,
                });

                const chartInstance = {
                    id, chart, series, container, mainPane,
                    symbol: 'BTCUSDT', interval: '1d',
                    candleData: [],
                    destroy: function() {
                        ChartSyncService.remove(this.chart);
                        if (this.indicatorManager) this.indicatorManager.removeAll();
                        this.chart.remove();
                    }
                };
                chartInstance.indicatorManager = createIndicatorManager(chartInstance);
                chartInstances.push(chartInstance);
                container.addEventListener('click', () => setActiveChart(chartInstance));
                
                const resizeObserver = new ResizeObserver(() => {
                    const rect = container.getBoundingClientRect();
                    chart.applyOptions({ width: rect.width, height: mainPane.clientHeight });
                     Object.values(chartInstance.indicatorManager.activeIndicators).forEach(ind => {
                         if(ind.paneChart) ind.paneChart.applyOptions({ width: rect.width });
                    });
                });
                resizeObserver.observe(container);
                return chartInstance;
            }
            
            function setActiveChart(instance) {
                if(activeChartInstance) {
                    activeChartInstance.container.classList.remove('active-chart');
                }
                activeChartInstance = instance;
                activeChartInstance.container.classList.add('active-chart');
                
                document.getElementById('symbol-name').textContent = activeChartInstance.symbol;
                
                document.querySelectorAll('.timeframe-item').forEach(item => {
                    item.classList.toggle('active-timeframe', item.dataset.timeframe === activeChartInstance.interval);
                });
                
                renderIndicatorsMenu();
            }

            async function updateAllCharts(symbol, interval) {
                if (symbol && interval && activeChartInstance) {
                    activeChartInstance.symbol = symbol;
                    activeChartInstance.interval = interval;
                    document.getElementById('symbol-name').textContent = symbol;
                }
                for (const instance of chartInstances) {
                    try {
                        instance.symbol = activeChartInstance.symbol; // sync symbol for all charts
                        instance.interval = activeChartInstance.interval; // sync interval for all charts
                        const response = await fetch(`https://api.binance.com/api/v3/klines?symbol=${instance.symbol}&interval=${instance.interval}&limit=500`);
                        const data = await response.json();
                        instance.candleData = data.map(d => ({
                            time: d[0] / 1000, open: parseFloat(d[1]), high: parseFloat(d[2]),
                            low: parseFloat(d[3]), close: parseFloat(d[4]),
                        }));
                        instance.series.setData(instance.candleData);
                        instance.indicatorManager.clearCache();
                        instance.indicatorManager.updateAllActive(instance.candleData);
                    } catch (error) { console.error(`Chart ${instance.id} for ${instance.symbol} failed to load:`, error); }
                }
                AlarmManager.redrawAllAlarmLines();
            }
            
            function resizeHandler() {
                chartInstances.forEach(instance => {
                    if (instance.mainPane) {
                        instance.chart.resize(instance.mainPane.clientWidth, instance.mainPane.clientHeight);
                    }
                    Object.values(instance.indicatorManager.activeIndicators).forEach(activeInd => {
                        if (activeInd.paneChart && activeInd.paneContainer) {
                            const container = activeInd.paneContainer;
                            activeInd.paneChart.resize(container.clientWidth, container.clientHeight);
                        }
                    });
                });
            }
            
            function setupUIListeners() {
                const addSymbolModal = document.getElementById('add-symbol-modal');
                const createAlarmModal = document.getElementById('create-alarm-modal');
                
                document.getElementById('close-modal-button')?.addEventListener('click', () => addSymbolModal.style.display = 'none');
                addSymbolModal?.addEventListener('click', e => { if (e.target === addSymbolModal) addSymbolModal.style.display = 'none'; });
                document.getElementById('search-symbol-input')?.addEventListener('input', e => renderAvailableSymbols(e.target.value));
                document.getElementById('cancel-alarm-button')?.addEventListener('click', () => createAlarmModal.style.display = 'none');
                createAlarmModal?.addEventListener('click', e => { if (e.target === createAlarmModal) createAlarmModal.style.display = 'none'; });
                document.getElementById('alarm-form')?.addEventListener('submit', e => {
                    e.preventDefault();
                    const price = parseFloat(document.getElementById('alarm-price').value);
                    if (!isNaN(price) && activeChartInstance) { AlarmManager.add(activeChartInstance.symbol, price); createAlarmModal.style.display = 'none'; e.target.reset(); }
                });

                document.querySelectorAll('.right-panel-tab').forEach(button => {
                    button.addEventListener('click', () => RightPanelManager.togglePanel(button.dataset.panel));
                });
                document.querySelectorAll('.layout-item').forEach(button => {
                     button.addEventListener('click', (e) => {
                        e.preventDefault();
                        applyLayout(button.dataset.layout);
                        document.getElementById('layout-dropdown').classList.add('hidden');
                    });
                });
                
                const timeMenuDropdown = document.getElementById('time-menu-dropdown');
                document.getElementById('time-menu-button').addEventListener('click', e => {
                    e.stopPropagation();
                    timeMenuDropdown.classList.toggle('hidden');
                    document.getElementById('indicators-dropdown').classList.add('hidden');
                    document.getElementById('layout-dropdown').classList.add('hidden');
                });
                timeMenuDropdown.addEventListener('click', e => e.stopPropagation()); // Prevent clicks inside from closing it
                document.querySelectorAll('.timeframe-item').forEach(item => {
                    item.addEventListener('click', e => {
                        e.preventDefault();
                        document.querySelectorAll('.timeframe-item').forEach(i => i.classList.remove('active-timeframe'));
                        item.classList.add('active-timeframe');
                        document.querySelector('#time-menu-button span').textContent = item.textContent;
                        timeMenuDropdown.classList.add('hidden');
                        updateAllCharts(activeChartInstance.symbol, item.dataset.timeframe);
                    });
                });

                document.getElementById('save-custom-timeframe').addEventListener('click', (e) => {
                    e.preventDefault();
                    const value = document.getElementById('custom-timeframe-value').value;
                    const unit = document.getElementById('custom-timeframe-unit').value;
                    
                    if (!value || parseInt(value) < 1) {
                        AlarmManager.showNotification("Lütfen geçerli bir zaman değeri girin.");
                        return;
                    }
                    TimeframeManager.add(value, unit);
                });

                const indicatorsDropdown = document.getElementById('indicators-dropdown');
                document.getElementById('indicators-button').addEventListener('click', e => {
                    e.stopPropagation();
                    indicatorsDropdown.classList.toggle('hidden');
                    document.getElementById('time-menu-dropdown').classList.add('hidden');
                    document.getElementById('layout-dropdown').classList.add('hidden');
                });
                document.getElementById('indicator-search').addEventListener('input', e => renderIndicatorsMenu(e.target.value));
                 document.getElementById('replay-button').addEventListener('click', enterReplaySelectionMode);
                 document.getElementById('replay-exit').addEventListener('click', exitReplayMode);
                 document.getElementById('replay-step-forward').addEventListener('click', stepForwardReplay);
                 document.getElementById('replay-play-pause').addEventListener('click', e => {
                    const btn = e.currentTarget; if (btn.dataset.state === 'paused') playReplay(); else pauseReplay();
                });
                const speedDropdown = document.getElementById('replay-speed-dropdown');
                document.getElementById('replay-speed-button').addEventListener('click', e => { e.stopPropagation(); speedDropdown.classList.toggle('hidden'); });
                document.querySelectorAll('#replay-speed-dropdown a').forEach(item => {
                    item.addEventListener('click', e => {
                        e.preventDefault(); replaySpeed = parseInt(item.dataset.speed);
                        document.getElementById('replay-speed-button').textContent = item.textContent;
                        speedDropdown.classList.add('hidden'); if (replayIntervalId) playReplay();
                    });
                });
                const layoutDropdown = document.getElementById('layout-dropdown');
                document.getElementById('layout-button').addEventListener('click', e => {
                     e.stopPropagation();
                     layoutDropdown.classList.toggle('hidden');
                     document.getElementById('time-menu-dropdown').classList.add('hidden');
                     document.getElementById('indicators-dropdown').classList.add('hidden');
                });

                const settingsModal = document.getElementById('settings-modal');
                const bgColorPicker = document.getElementById('bg-color-picker');
                const crosshairColorPicker = document.getElementById('crosshair-color-picker');
                const crosshairWidthSlider = document.getElementById('crosshair-width-slider');
                const crosshairWidthValue = document.getElementById('crosshair-width-value');
                const crosshairStyleButtons = document.getElementById('crosshair-style-buttons');
                const bgColorSwatches = document.getElementById('bg-color-swatches');
                const customColorLabel = document.querySelector('label[for="bg-color-picker"]');

                let originalBgColor = chartBackgroundColor;
                let originalCrosshairColor = crosshairColor;
                let originalCrosshairWidth = crosshairWidth;
                let originalCrosshairStyle = crosshairStyle;


                document.getElementById('settings-button').addEventListener('click', () => {
                    originalBgColor = chartBackgroundColor;
                    originalCrosshairColor = crosshairColor;
                    originalCrosshairWidth = crosshairWidth;
                    originalCrosshairStyle = crosshairStyle;

                    bgColorPicker.value = originalBgColor;
                    let isPreset = false;
                    bgColorSwatches.querySelectorAll('.bg-color-swatch').forEach(swatch => {
                        const isActive = swatch.dataset.color === originalBgColor;
                        swatch.classList.toggle('active', isActive);
                        if (isActive) isPreset = true;
                    });
                    customColorLabel.classList.toggle('active', !isPreset);
                    
                    crosshairColorPicker.value = originalCrosshairColor;
                    crosshairWidthSlider.value = originalCrosshairWidth;
                    crosshairWidthValue.textContent = originalCrosshairWidth;
                    crosshairStyleButtons.querySelectorAll('.crosshair-style-btn').forEach(btn => {
                        btn.classList.toggle('active', btn.dataset.style == originalCrosshairStyle);
                    });

                    settingsModal.style.display = 'flex';
                });

                document.getElementById('cancel-settings-button').addEventListener('click', () => {
                    applyBackgroundColor(originalBgColor);
                    applyCrosshairSettings(originalCrosshairColor, originalCrosshairWidth, originalCrosshairStyle);
                    settingsModal.style.display = 'none';
                });

                settingsModal.addEventListener('click', e => {
                    if (e.target === settingsModal) {
                        applyBackgroundColor(originalBgColor);
                        applyCrosshairSettings(originalCrosshairColor, originalCrosshairWidth, originalCrosshairStyle);
                        settingsModal.style.display = 'none';
                    }
                });
                
                document.getElementById('save-settings-button').addEventListener('click', () => {
                    chartBackgroundColor = bgColorPicker.value;
                    chartTextColor = getContrastingTextColor(chartBackgroundColor);
                    localStorage.setItem('chartBackgroundColor', chartBackgroundColor);

                    crosshairColor = crosshairColorPicker.value;
                    crosshairWidth = parseInt(crosshairWidthSlider.value, 10);
                    const activeStyleBtn = crosshairStyleButtons.querySelector('.crosshair-style-btn.active');
                    crosshairStyle = activeStyleBtn ? parseInt(activeStyleBtn.dataset.style, 10) : 0;
                    localStorage.setItem('chartCrosshairColor', crosshairColor);
                    localStorage.setItem('chartCrosshairWidth', crosshairWidth);
                    localStorage.setItem('chartCrosshairStyle', crosshairStyle);
                    
                    originalBgColor = chartBackgroundColor; 
                    originalCrosshairColor = crosshairColor;
                    originalCrosshairWidth = crosshairWidth;
                    originalCrosshairStyle = crosshairStyle;

                    settingsModal.style.display = 'none';
                });

                bgColorPicker.addEventListener('input', (e) => {
                    const newColor = e.target.value;
                    applyBackgroundColor(newColor);
                    bgColorSwatches.querySelectorAll('.bg-color-swatch').forEach(s => s.classList.remove('active'));
                    customColorLabel.classList.add('active');
                });

                bgColorSwatches.addEventListener('click', (e) => {
                    const swatch = e.target.closest('.bg-color-swatch');
                    if (swatch) {
                        bgColorSwatches.querySelectorAll('.bg-color-swatch').forEach(s => s.classList.remove('active'));
                        swatch.classList.add('active');
                        customColorLabel.classList.remove('active');

                        const newColor = swatch.dataset.color;
                        bgColorPicker.value = newColor;
                        applyBackgroundColor(newColor);
                    }
                });

                crosshairColorPicker.addEventListener('input', (e) => {
                    const newColor = e.target.value;
                    const currentWidth = parseInt(crosshairWidthSlider.value, 10);
                    const activeStyleBtn = crosshairStyleButtons.querySelector('.crosshair-style-btn.active');
                    const currentStyle = activeStyleBtn ? parseInt(activeStyleBtn.dataset.style, 10) : 0;
                    applyCrosshairSettings(newColor, currentWidth, currentStyle);
                });

                crosshairWidthSlider.addEventListener('input', (e) => {
                    const newWidth = parseInt(e.target.value, 10);
                    const currentColor = crosshairColorPicker.value;
                    const activeStyleBtn = crosshairStyleButtons.querySelector('.crosshair-style-btn.active');
                    const currentStyle = activeStyleBtn ? parseInt(activeStyleBtn.dataset.style, 10) : 0;
                    crosshairWidthValue.textContent = newWidth;
                    applyCrosshairSettings(currentColor, newWidth, currentStyle);
                });

                crosshairStyleButtons.addEventListener('click', (e) => {
                    const button = e.target.closest('.crosshair-style-btn');
                    if (!button) return;

                    crosshairStyleButtons.querySelectorAll('.crosshair-style-btn').forEach(btn => btn.classList.remove('active'));
                    button.classList.add('active');

                    const newStyle = parseInt(button.dataset.style, 10);
                    const currentColor = crosshairColorPicker.value;
                    const currentWidth = parseInt(crosshairWidthSlider.value, 10);
                    applyCrosshairSettings(currentColor, currentWidth, newStyle);
                });


                window.addEventListener('click', () => {
                    document.getElementById('time-menu-dropdown').classList.add('hidden');
                    document.getElementById('indicators-dropdown').classList.add('hidden');
                    document.getElementById('replay-speed-dropdown').classList.add('hidden');
                    document.getElementById('layout-dropdown').classList.add('hidden');
                });
                
                const leftToolbarToggle = document.getElementById('left-toolbar-toggle');
                const leftToolbar = document.getElementById('left-toolbar');
                
                leftToolbarToggle.addEventListener('click', (e) => {
                    e.stopPropagation();
                    const icon = leftToolbarToggle.querySelector('svg');
                    leftToolbar.classList.toggle('!w-14');
                    leftToolbar.classList.toggle('!w-0');
                    leftToolbar.classList.toggle('!p-2');
                    leftToolbar.classList.toggle('!p-0');
                    leftToolbar.classList.toggle('!border-r-0');
                    
                    if (icon) {
                        icon.classList.toggle('rotate-180');
                    }
                    
                    setTimeout(resizeHandler, 310);
                });
            }
            
            function getContrastingTextColor(hexcolor){
                if (hexcolor.slice(0, 1) === '#') { hexcolor = hexcolor.slice(1); }
                const r = parseInt(hexcolor.substr(0,2),16);
                const g = parseInt(hexcolor.substr(2,2),16);
                const b = parseInt(hexcolor.substr(4,2),16);
                const yiq = ((r*299)+(g*587)+(b*114))/1000;
                return (yiq >= 128) ? '#131722' : '#d1d4dc';
            }

            function applyBackgroundColor(color) {
                const textColor = getContrastingTextColor(color);
                chartInstances.forEach(instance => {
                    instance.chart.applyOptions({ layout: { background: { color }, textColor } });
                     Object.values(instance.indicatorManager.activeIndicators).forEach(activeInd => {
                        if(activeInd.definition.type === 'pane' && activeInd.paneChart) {
                           activeInd.paneChart.applyOptions({ layout: { background: { color }, textColor } });
                        }
                    });
                });
            }
            
            function applyCrosshairSettings(color, width, style) {
                const crosshairOptions = {
                    crosshair: {
                        color: color,
                        vertLine: {
                            width: width,
                            color: color,
                            style: style,
                        },
                        horzLine: {
                            width: width,
                            color: color,
                            style: style,
                        }
                    }
                };
                chartInstances.forEach(instance => {
                    instance.chart.applyOptions(crosshairOptions);
                });
            }

            function renderIndicatorsMenu(filter = '') {
                const listEl = document.getElementById('indicator-list');
                listEl.innerHTML = '';
                Object.values(IndicatorLibrary).filter(ind => ind.name.toLowerCase().includes(filter.toLowerCase()))
                    .forEach(ind => {
                        const isChecked = activeChartInstance ? !!activeChartInstance.indicatorManager.activeIndicators[ind.id] : false;
                        const item = document.createElement('a'); item.href = '#';
                        item.className = 'indicator-item flex items-center justify-between px-2 py-2 text-sm text-gray-300 hover:bg-gray-700 rounded-md';
                        item.dataset.indicatorId = ind.id;
                        item.innerHTML = `<span>${ind.name}</span> <i data-lucide="check" class="w-4 h-4 text-blue-500 ${isChecked ? '' : 'invisible'}"></i>`;
                        item.addEventListener('click', e => {
                            e.preventDefault();
                            if(activeChartInstance) activeChartInstance.indicatorManager.toggle(ind.id);
                        });
                        listEl.appendChild(item);
                    });
                lucide.createIcons();
            }
            async function fetchAllSymbols() {
                try {
                    const response = await fetch('https://api.binance.com/api/v3/exchangeInfo');
                    const data = await response.json();
                    allSymbols = data.symbols.filter(s => s.status === 'TRADING').map(s => s.symbol);
                } catch (error) { console.error("Sembol listesi alınamadı:", error); }
            }
            function renderAvailableSymbols(filter = '') {
                const resultsList = document.getElementById('symbol-results-list');
                resultsList.innerHTML = '';
                allSymbols.filter(s => s.toLowerCase().includes(filter.toLowerCase())).slice(0, 100).forEach(symbol => {
                    const item = document.createElement('div');
                    item.className = 'p-3 hover:bg-gray-700 cursor-pointer rounded-md';
                    item.textContent = symbol;
                    item.addEventListener('click', () => {
                        updateAllCharts(symbol, activeChartInstance.interval);
                        if (!watchlistData.includes(symbol)) {
                            watchlistData.push(symbol);
                            renderWatchlist();
                        }
                        const modal = document.getElementById('add-symbol-modal');
                        modal.style.display = 'none';
                        document.getElementById('search-symbol-input').value = '';
                        renderAvailableSymbols(''); // Reset list
                    });
                    resultsList.appendChild(item);
                });
            }
             function renderWatchlist() {
                const watchlistEl = document.getElementById('watchlist');
                if (!watchlistEl) return;
                watchlistEl.innerHTML = ''; 
                watchlistData.forEach(symbol => {
                    const li = document.createElement('li');
                    li.className = 'group flex justify-between items-center pl-2 pr-1 py-1 text-xs border-b border-gray-800';
                    li.innerHTML = `
                        <div class="flex-1 min-w-0 chart-switcher cursor-pointer p-1 -ml-1 rounded-md hover:bg-gray-800">
                            <span class="font-medium">${symbol}</span>
                        </div>
                        <div class="text-right flex-shrink-0 w-16">
                            <span id="price-${symbol}" class="block">...</span>
                        </div>
                        <div class="pl-1 flex items-center flex-shrink-0">
                            <button class="remove-from-watchlist p-1 rounded-md text-gray-500 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-opacity" title="${symbol} Kaldır">
                                <i data-lucide="trash-2" class="w-4 h-4"></i>
                            </button>
                        </div>`;
                    li.querySelector('.chart-switcher').addEventListener('click', () => updateAllCharts(symbol, activeChartInstance.interval));
                    li.querySelector('.remove-from-watchlist').addEventListener('click', e => {
                        e.stopPropagation();
                        watchlistData = watchlistData.filter(s => s !== symbol);
                        renderWatchlist();
                    });
                    watchlistEl.appendChild(li);
                });
                lucide.createIcons();
            }
            function subscribeToAllTickers() {
                const socket = new WebSocket('wss://stream.binance.com:9443/ws/!ticker@arr');
                socket.onmessage = event => {
                    const tickers = JSON.parse(event.data);
                    tickers.forEach(ticker => liveTickerData.set(ticker.s, ticker));
                    
                    AlarmManager.checkAllAlarms();
                    
                    // Update watchlist prices
                    watchlistData.forEach(symbol => {
                        const data = liveTickerData.get(symbol);
                        if(data) {
                            const priceEl = document.getElementById(`price-${symbol}`);
                            if (priceEl) {
                                priceEl.textContent = parseFloat(data.c).toFixed(symbol === 'SHIBUSDT' ? 8 : 4);
                            }
                        }
                    });
                }
            }

            // --- CHAT FONKSİYONLARI ---
            function initializeChat() {
                const { auth, db, collection, addDoc, query, orderBy, onSnapshot, serverTimestamp, doc, setDoc, deleteDoc } = window.firebaseTools;
                
                // Tab elements
                const publicTabBtn = document.getElementById('chat-tab-btn-public');
                const usersTabBtn = document.getElementById('chat-tab-btn-users');
                const publicTabContent = document.getElementById('chat-tab-public');
                const usersTabContent = document.getElementById('chat-tab-users');
                
                // Public chat elements
                const chatMessagesEl = document.getElementById('chat-messages');
                const chatForm = document.getElementById('chat-form');
                const chatInput = document.getElementById('chat-input');
                
                if(!auth || !db || !publicTabBtn) {
                     console.error("Chat elements or Firebase not ready.");
                     return;
                }

                const user = auth.currentUser;
                const username = user ? (user.displayName || 'YÖNETİCİ') : 'Anonim';
                
                // --- Tab Switching Logic ---
                const switchToPublic = () => {
                    publicTabContent.classList.remove('hidden');
                    usersTabContent.classList.add('hidden');
                    publicTabBtn.classList.add('border-blue-500', 'text-blue-400');
                    publicTabBtn.classList.remove('border-transparent', 'text-gray-400', 'hover:text-gray-200', 'hover:border-gray-500');
                    usersTabBtn.classList.add('border-transparent', 'text-gray-400', 'hover:text-gray-200', 'hover:border-gray-500');
                    usersTabBtn.classList.remove('border-blue-500', 'text-blue-400');
                };
                const switchToUsers = () => {
                    publicTabContent.classList.add('hidden');
                    usersTabContent.classList.remove('hidden');
                    usersTabBtn.classList.add('border-blue-500', 'text-blue-400');
                    usersTabBtn.classList.remove('border-transparent', 'text-gray-400', 'hover:text-gray-200', 'hover:border-gray-500');
                    publicTabBtn.classList.add('border-transparent', 'text-gray-400', 'hover:text-gray-200', 'hover:border-gray-500');
                    publicTabBtn.classList.remove('border-blue-500', 'text-blue-400');
                };
                publicTabBtn.addEventListener('click', switchToPublic);
                usersTabBtn.addEventListener('click', switchToUsers);

                // --- Public Chat Logic ---
                const messagesCol = collection(db, `artifacts/${appId}/public/data/chat_messages`);
                const qPublic = query(messagesCol, orderBy('timestamp', 'desc'));

                chatListeners.publicUnsub = onSnapshot(qPublic, (snapshot) => {
                    const currentMessagesEl = document.getElementById('chat-messages');
                    if (!currentMessagesEl) return;
                    currentMessagesEl.innerHTML = '';
                    snapshot.forEach(doc => {
                        const msg = doc.data();
                        if (user && msg.userId !== user.uid && BlockedUsersManager.isBlocked(msg.userId)) return;

                        const msgEl = document.createElement('div');
                        msgEl.className = 'mb-1 text-xs';
                        const time = msg.timestamp ? new Date(msg.timestamp.seconds * 1000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit'}) : '';
                        
                        let usernameHtml;
                        if (user && msg.userId && msg.userId === user.uid) {
                            usernameHtml = `<span class="font-semibold text-blue-400">${msg.username}:</span>`;
                        } else if (msg.userId) { 
                            usernameHtml = `<button data-user-id="${msg.userId}" data-username="${msg.username}" class="font-semibold text-blue-400 hover:underline focus:outline-none text-left">${msg.username}:</button>`;
                        } else {
                            usernameHtml = `<span class="font-semibold text-blue-400">${msg.username}:</span>`;
                        }

                        msgEl.innerHTML = `
                            <div class="flex items-baseline gap-2 group">
                                ${usernameHtml}
                                <span class="text-gray-300 break-words flex-1">${msg.text}</span>
                                <span class="text-xs text-gray-500 ml-auto flex-shrink-0">${time}</span>
                                ${user && msg.userId === user.uid ? `
                                    <button data-message-id="${doc.id}" class="delete-public-msg-btn p-1 text-gray-500 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-opacity" title="Mesajı Sil">
                                        <i data-lucide="trash-2" class="w-3 h-3"></i>
                                    </button>
                                ` : ''}
                            </div>`;
                        currentMessagesEl.prepend(msgEl);
                    });

                    currentMessagesEl.querySelectorAll('button[data-user-id]').forEach(button => {
                        button.addEventListener('click', () => {
                            initializePrivateChat(button.dataset.userId, button.dataset.username);
                        });
                    });

                    currentMessagesEl.querySelectorAll('.delete-public-msg-btn').forEach(button => {
                        button.addEventListener('click', () => {
                            const messageId = button.dataset.messageId;
                            showConfirmationModal('Bu mesajı silmek istediğinizden emin misiniz?', async () => {
                                try {
                                    const msgRef = doc(db, `artifacts/${appId}/public/data/chat_messages`, messageId);
                                    await deleteDoc(msgRef);
                                } catch (error) {
                                    console.error("Mesaj silinirken hata:", error);
                                    AlarmManager.showNotification("Hata: Mesaj silinemedi.");
                                }
                            });
                        });
                    });
                    lucide.createIcons();
                });

                chatForm.addEventListener('submit', async (e) => {
                    e.preventDefault();
                    const text = chatInput.value.trim();
                    if (text && user) {
                        try {
                            await addDoc(messagesCol, {
                                text: text,
                                username: username,
                                userId: user.uid,
                                timestamp: serverTimestamp()
                            });
                             const userRef = doc(db, `artifacts/${appId}/public/data/chat_users`, user.uid);
                             await setDoc(userRef, { username: username, lastSeen: serverTimestamp() }, { merge: true });
                            chatInput.value = '';
                        } catch (error) {
                            console.error("Mesaj gönderilirken hata oluştu:", error);
                        }
                    }
                });
                
                // --- Users List Logic ---
                const usersCol = collection(db, `artifacts/${appId}/public/data/chat_users`);
                const userSearchInput = document.getElementById('user-search-input');
                const userListContainer = document.getElementById('user-list-container');
                let allChatUsers = [];

                const renderUserList = (filter = '') => {
                    if (!userListContainer) return;
                    userListContainer.innerHTML = '';
                    const lowerCaseFilter = filter.trim().toLowerCase();
                    
                    const fiveMinutesAgo = Date.now() - (5 * 60 * 1000);

                    const filteredUsers = allChatUsers.filter(doc => {
                        const userData = doc.data();
                        if (!userData.username) return false;
                        
                        if (user && doc.id === user.uid && username !== 'YÖNETİCİ') {
                            return false;
                        }
                        
                        return userData.username.toLowerCase().includes(lowerCaseFilter);
                    });

                    if (filteredUsers.length === 0) {
                        const message = lowerCaseFilter ? 'Aramanızla eşleşen kişi bulunamadı.' : 'Sohbette başka kişi bulunmuyor.';
                        userListContainer.innerHTML = `<p class="text-center text-gray-500 p-4 text-xs">${message}</p>`;
                    } else {
                        filteredUsers.forEach(doc => {
                            const userData = doc.data();
                            const lastSeen = userData.lastSeen ? userData.lastSeen.toMillis() : 0;
                            const isOnline = lastSeen > fiveMinutesAgo;
                            const isBlocked = BlockedUsersManager.isBlocked(doc.id);

                            const userEl = document.createElement('div');
                            userEl.className = 'flex items-center justify-between p-2 hover:bg-gray-700 rounded-md';

                            let blockButtonHtml = '';
                            const isSelf = user && doc.id === user.uid;
                            // Yönetici, kendisi hariç herkesi engelleyebilir.
                            // Normal bir kullanıcı, yönetici hariç herkesi engelleyebilir.
                            // Kimse kendini engelleyemez.
                            if (!isSelf && (username === 'YÖNETİCİ' || userData.username !== 'YÖNETİCİ')) {
                                blockButtonHtml = `
                                    <button title="${isBlocked ? 'Engeli Kaldır' : 'Kullanıcıyı Engelle'}" class="block-user-btn p-1 ${isBlocked ? 'text-yellow-500 hover:text-yellow-400' : 'text-gray-400 hover:text-red-500'}" data-user-id="${doc.id}" data-username="${userData.username}">
                                        <i data-lucide="${isBlocked ? 'shield-check' : 'shield-x'}" class="w-4 h-4"></i>
                                    </button>
                                `;
                            }

                            userEl.innerHTML = `
                                <div class="flex items-center gap-2">
                                    <span class="relative flex h-2.5 w-2.5">
                                        <span class="animate-ping absolute inline-flex h-full w-full rounded-full ${isOnline ? 'bg-green-400' : 'bg-gray-500'} opacity-75"></span>
                                        <span class="relative inline-flex rounded-full h-2.5 w-2.5 ${isOnline ? 'bg-green-500' : 'bg-gray-600'}"></span>
                                    </span>
                                    <span class="text-sm font-medium ${isBlocked ? 'line-through text-gray-500' : ''}">${userData.username}</span>
                                </div>
                                <div class="flex items-center">
                                    <button title="Özel Mesaj Gönder" class="private-chat-btn p-1 text-gray-400 hover:text-blue-500"><i data-lucide="message-circle" class="w-4 h-4"></i></button>
                                    ${blockButtonHtml}
                                </div>
                            `;
                            
                            userEl.querySelector('.private-chat-btn').addEventListener('click', (e) => {
                                e.stopPropagation();
                                if (isBlocked) {
                                    AlarmManager.showNotification('Engellenen bir kullanıcıya özel mesaj gönderemezsiniz.');
                                    return;
                                }
                                initializePrivateChat(doc.id, userData.username);
                            });

                            const blockBtn = userEl.querySelector('.block-user-btn');
                            if (blockBtn) {
                                blockBtn.addEventListener('click', (e) => {
                                    e.stopPropagation();
                                    const userIdToBlock = blockBtn.dataset.userId;
                                    const usernameToBlock = blockBtn.dataset.username;
                                    BlockedUsersManager.toggleBlock(userIdToBlock, usernameToBlock);
                                    renderUserList(userSearchInput?.value || '');
                                });
                            }
                            
                            userListContainer.appendChild(userEl);
                        });
                    }
                    
                    const infoEl = document.createElement('div');
                    infoEl.className = 'text-center text-xs text-gray-500 p-3 border-t border-gray-800 mt-2';
                    infoEl.innerHTML = 'Özel sohbet başlatmak için bir kullanıcının yanındaki <i data-lucide="message-circle" class="inline-block w-3 h-3"></i> ikonuna tıklayın.';
                    userListContainer.appendChild(infoEl);

                    lucide.createIcons();
                };

                userSearchInput?.addEventListener('input', (e) => {
                    renderUserList(e.target.value);
                });

                chatListeners.usersUnsub = onSnapshot(usersCol, (snapshot) => {
                    if (!document.getElementById('user-list-container')) return;
                    allChatUsers = snapshot.docs;
                    const currentSearchInput = document.getElementById('user-search-input');
                    const currentFilter = currentSearchInput ? currentSearchInput.value : '';
                    renderUserList(currentFilter);
                });

                // --- Keep user status updated ---
                const updateUserStatus = async () => {
                    if (user) {
                        try {
                            const userRef = doc(db, `artifacts/${appId}/public/data/chat_users`, user.uid);
                            await setDoc(userRef, { username: username, lastSeen: serverTimestamp() }, { merge: true });
                        } catch (error) {
                            console.error("Kullanıcı durumu güncellenirken hata oluştu:", error);
                        }
                    }
                };
                updateUserStatus(); // Update immediately on chat open
                chatListeners.statusInterval = setInterval(updateUserStatus, 5 * 60 * 1000); // And every 5 minutes
            }

             function initializePrivateChat(recipientId, recipientName) {
                if (BlockedUsersManager.isBlocked(recipientId)) {
                    AlarmManager.showNotification(`${recipientName} adlı kullanıcıyı engellediğiniz için özel sohbet başlatılamaz.`);
                    return;
                }
                const { auth, db, collection, addDoc, query, orderBy, onSnapshot, serverTimestamp, doc, deleteDoc } = window.firebaseTools;
                const modal = document.getElementById('private-chat-modal');
                const recipientNameEl = document.getElementById('private-chat-recipient-name');
                const messagesEl = document.getElementById('private-chat-messages');
                const form = document.getElementById('private-chat-form');
                const input = document.getElementById('private-chat-input');
                const closeButton = document.getElementById('close-private-chat-button');

                if (chatListeners.privateUnsub) chatListeners.privateUnsub();

                const user = auth.currentUser;
                if (!user) return;
                
                const chatRoomId = [user.uid, recipientId].sort().join('_');
                const username = user ? (user.displayName || 'YÖNETİCİ') : 'Anonim';

                recipientNameEl.textContent = recipientName;
                modal.style.display = 'flex';
                input.focus();

                const privateMessagesCol = collection(db, `artifacts/${appId}/public/data/private_chats/${chatRoomId}/messages`);
                const qPrivate = query(privateMessagesCol, orderBy('timestamp', 'asc'));

                chatListeners.privateUnsub = onSnapshot(qPrivate, (snapshot) => {
                    messagesEl.innerHTML = '';
                    snapshot.forEach(doc => {
                        const msg = doc.data();
                        const msgEl = document.createElement('div');
                        const isMe = msg.senderId === user.uid;
                        msgEl.className = `mb-2 text-sm flex w-full ${isMe ? 'justify-end' : 'justify-start'}`;
                        const time = msg.timestamp ? new Date(msg.timestamp.seconds * 1000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit'}) : '';
                        
                        msgEl.innerHTML = `
                            <div class="group relative p-2 rounded-lg max-w-xs ${isMe ? 'bg-blue-600' : 'bg-gray-700'}">
                                <div class="font-bold">${msg.senderName}</div>
                                <div class="break-words">${msg.text}</div>
                                <div class="text-xs text-gray-400 text-right mt-1">${time}</div>
                                ${isMe ? `
                                    <button data-message-id="${doc.id}" class="delete-private-msg-btn absolute top-0 -left-7 p-1 text-gray-300 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-opacity" title="Mesajı Sil">
                                        <i data-lucide="trash-2" class="w-4 h-4"></i>
                                    </button>
                                ` : ''}
                            </div>`;
                        messagesEl.appendChild(msgEl);
                    });

                    messagesEl.querySelectorAll('.delete-private-msg-btn').forEach(button => {
                        button.addEventListener('click', () => {
                            const messageId = button.dataset.messageId;
                            showConfirmationModal('Bu mesajı silmek istediğinizden emin misiniz?', async () => {
                                try {
                                    const msgRef = doc(db, `artifacts/${appId}/public/data/private_chats/${chatRoomId}/messages`, messageId);
                                    await deleteDoc(msgRef);
                                } catch (error) {
                                    console.error("Özel mesaj silinirken hata:", error);
                                    AlarmManager.showNotification("Hata: Mesaj silinemedi.");
                                }
                            });
                        });
                    });

                    lucide.createIcons();
                    messagesEl.scrollTop = messagesEl.scrollHeight;
                });

                const submitHandler = async (e) => {
                    e.preventDefault();
                    const text = input.value.trim();
                    if (text) {
                        await addDoc(privateMessagesCol, {
                            text,
                            senderId: user.uid,
                            senderName: username,
                            recipientId: recipientId,
                            timestamp: serverTimestamp()
                        });
                        input.value = '';
                    }
                };
                
                form.onsubmit = submitHandler;
                
                const closeModal = () => {
                    if (chatListeners.privateUnsub) chatListeners.privateUnsub();
                    chatListeners.privateUnsub = null;
                    modal.style.display = 'none';
                    form.onsubmit = null;
                };

                closeButton.addEventListener('click', closeModal, { once: true });
                modal.addEventListener('click', e => { if (e.target === modal) closeModal(); }, { once: true });
            }

            // --- NOT YÖNETİCİSİ ---
            const NotesManager = {
                notes: [], // [{id, title, content, color}]
                load() {
                    const savedNotes = localStorage.getItem('ersinTeknikUserNotes');
                    if (savedNotes) {
                        this.notes = JSON.parse(savedNotes).map(note => ({
                            ...note,
                             title: note.title === 'Yeni Not' ? 'Not başlığı' : note.title,
                            color: note.color || '#374151' // Fallback for old notes
                        }));
                    } else {
                        this.notes = [{ id: Date.now(), title: 'Not başlığı', content: '', color: '#374151' }];
                    }
                },
                save() {
                    const notesListEl = document.getElementById('notes-list');
                    if (!notesListEl) return;
                    const updatedNotes = [];
                    notesListEl.querySelectorAll('.note-item').forEach(noteEl => {
                        const id = noteEl.dataset.noteId;
                        const title = noteEl.querySelector('.note-title').value;
                        const content = noteEl.querySelector('.note-content').value;
                        const color = noteEl.querySelector('.note-color-picker').value;
                        updatedNotes.push({ id, title, content, color });
                    });
                    this.notes = updatedNotes;
                    localStorage.setItem('ersinTeknikUserNotes', JSON.stringify(this.notes));
                    AlarmManager.showNotification('Notlar kaydedildi!');
                },
                add() {
                    this.notes.unshift({ id: Date.now(), title: 'Not başlığı', content: '', color: '#374151' });
                    this.render();
                },
                remove(noteId) {
                    this.notes = this.notes.filter(note => note.id != noteId);
                    this.render();
                },
                render() {
                    const listEl = document.getElementById('notes-list');
                    if (!listEl) return;
                    listEl.innerHTML = '';
                    if(this.notes.length === 0){
                         listEl.innerHTML = `<p class="text-center text-gray-500 p-4">Hiç not yok.</p>`;
                    }
                    this.notes.forEach(note => {
                        const noteEl = document.createElement('div');
                        noteEl.className = 'note-item bg-gray-800 rounded-md flex flex-col';
                        noteEl.dataset.noteId = note.id;
                        const headerColor = note.color || '#374151';
                        noteEl.innerHTML = `
                            <div class="note-header flex items-center gap-2 p-2 rounded-t-md" style="background-color: ${headerColor};">
                                <input type="color" class="note-color-picker" value="${headerColor}">
                                <input type="text" class="note-title text-sm font-semibold bg-transparent focus:outline-none w-full" value="${note.title}">
                                <button class="remove-note-btn p-1 text-gray-300 hover:text-red-500 flex-shrink-0"><i data-lucide="trash-2" class="w-4 h-4"></i></button>
                            </div>
                            <div class="p-2">
                                <textarea class="note-content w-full bg-transparent text-xs text-gray-400 focus:outline-none resize-y" rows="3" placeholder="Notunuzu yazın...">${note.content}</textarea>
                            </div>
                        `;
                        listEl.appendChild(noteEl);
                        
                        const colorPicker = noteEl.querySelector('.note-color-picker');
                        const noteHeader = noteEl.querySelector('.note-header');
                        colorPicker.addEventListener('input', (e) => {
                            noteHeader.style.backgroundColor = e.target.value;
                        });
                    });

                    listEl.querySelectorAll('.remove-note-btn').forEach(btn => {
                        btn.addEventListener('click', (e) => {
                            const noteId = e.currentTarget.closest('.note-item').dataset.noteId;
                            this.remove(noteId);
                        });
                    });
                    lucide.createIcons();
                }
            };
            
            // --- FİKİR PAYLAŞIM YÖNETİCİSİ ---
            const IdeaManager = {
                currentUserFollowing: [],
                init(initialFeedType = 'everyone') {
                    const { auth, db, doc, onSnapshot } = window.firebaseTools;
                    const user = auth.currentUser;
                    
                    if (user) {
                        const userProfileRef = doc(db, `artifacts/${appId}/public/data/user_profiles`, user.uid);
                        onSnapshot(userProfileRef, (docSnap) => {
                           this.currentUserFollowing = docSnap.exists() ? (docSnap.data().following || []) : [];
                           this.renderIdeas(initialFeedType);
                        });
                    } else {
                        this.currentUserFollowing = [];
                        this.renderIdeas(initialFeedType);
                    }
                },

                renderIdeas(feedType) {
                    const { auth, db, collection, query, where, orderBy, onSnapshot } = window.firebaseTools;
                    const user = auth.currentUser;

                    if (chatListeners.ideasUnsub) chatListeners.ideasUnsub();

                    const listId = feedType === 'following' ? 'following-ideas-list' : 'ideas-list';
                    const ideasListEl = document.getElementById(listId);
                    if (!ideasListEl) return;


                    const ideasCol = collection(db, `artifacts/${appId}/public/data/shared_ideas`);
                    let q;

                    if (feedType === 'following') {
                        if (!user || !this.currentUserFollowing || this.currentUserFollowing.length === 0) {
                            ideasListEl.innerHTML = `<p class="text-center text-gray-500 p-4 text-xs">Takip ettiğiniz kimse yok veya hiç fikir paylaşmamışlar.</p>`;
                            return;
                        }
                        q = query(ideasCol, where('userId', 'in', this.currentUserFollowing));
                    } else { // everyone
                        q = query(ideasCol, orderBy('timestamp', 'desc'));
                    }
                    
                    chatListeners.ideasUnsub = onSnapshot(q, (snapshot) => {
                        ideasListEl.innerHTML = '';

                        if (snapshot.empty) {
                            ideasListEl.innerHTML = `<p class="text-center text-gray-500 p-4 text-xs">${feedType === 'following' ? 'Takip ettikleriniz henüz fikir paylaşmamış.' : 'Henüz fikir paylaşılmamış.'}</p>`;
                            return;
                        }
                        
                        let docs = snapshot.docs;
                        if(feedType === 'following') {
                            docs.sort((a, b) => (b.data().timestamp?.seconds || 0) - (a.data().timestamp?.seconds || 0));
                        }

                        docs.forEach(doc => {
                            const idea = doc.data();
                            const ideaEl = this.createIdeaElement(doc.id, idea);
                            ideasListEl.appendChild(ideaEl);
                        });
                        lucide.createIcons();
                    });
                },

                createIdeaElement(id, idea) {
                    const { auth } = window.firebaseTools;
                    const user = auth.currentUser;
                    const ideaEl = document.createElement('div');
                    ideaEl.className = 'bg-gray-800 rounded-md flex flex-col';
                    const time = idea.timestamp ? new Date(idea.timestamp.seconds * 1000).toLocaleString('tr-TR') : '';
                    const isLiked = user && idea.likes && idea.likes.includes(user.uid);
                    const isFollowing = user && this.currentUserFollowing.includes(idea.userId);

                    let videoHtml = '';
                    if (idea.videoUrl) {
                        const embedUrl = this.getVideoEmbedUrl(idea.videoUrl);
                        if (embedUrl) {
                            videoHtml = `
                                <div class="mt-2 aspect-video">
                                    <iframe src="${embedUrl}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen class="w-full h-full rounded-md bg-black"></iframe>
                                </div>
                            `;
                        }
                    }

                    ideaEl.innerHTML = `
                        <div class="p-3">
                            <div class="flex justify-between items-start">
                                <div>
                                    <h4 class="font-bold text-base">${idea.username}</h4>
                                    <p class="text-xs text-gray-400">${time}</p>
                                </div>
                                <div class="flex items-center gap-1">
                                    ${user ? `<button data-author-id="${idea.userId}" title="${isFollowing ? 'Takibi Bırak' : 'Takip Et'}" class="follow-btn p-1 rounded-md ${isFollowing ? 'text-green-500 hover:text-green-600' : 'text-gray-400 hover:text-blue-500'}"><i data-lucide="${isFollowing ? 'user-check' : 'user-plus'}" class="w-4 h-4"></i></button>` : ''}
                                    ${user && user.uid === idea.userId ? `<button data-idea-id="${id}" class="edit-idea-btn p-1 text-gray-400 hover:text-green-500 flex-shrink-0" title="Düzenle"><i data-lucide="edit-3" class="w-4 h-4"></i></button>` : ''}
                                    ${user && user.uid === idea.userId ? `<button data-idea-id="${id}" class="delete-idea-btn p-1 text-gray-400 hover:text-red-500 flex-shrink-0" title="Sil"><i data-lucide="trash-2" class="w-4 h-4"></i></button>` : ''}
                                </div>
                            </div>
                            <h5 class="font-semibold mt-2 cursor-pointer" data-idea-id="${id}" data-action="view">${idea.title}</h5>
                            <p class="text-sm mt-1 text-gray-300">${idea.description}</p>
                        </div>
                        <img src="${idea.imageData}" alt="Grafik Fikri" class="w-full h-auto object-contain bg-black cursor-pointer" data-idea-id="${id}" data-action="view">
                        ${videoHtml}
                        <div class="flex items-center gap-4 p-2 border-t border-gray-700">
                            <button data-idea-id="${id}" class="like-idea-btn flex items-center gap-1.5 text-sm hover:text-blue-400 ${isLiked ? 'text-blue-500' : 'text-gray-400'}">
                                <i data-lucide="thumbs-up" class="w-4 h-4"></i>
                                <span>${idea.likes ? idea.likes.length : 0}</span>
                            </button>
                            <button data-idea-id="${id}" class="comment-idea-btn flex items-center gap-1.5 text-sm text-gray-400 hover:text-blue-400 p-1 rounded-md">
                                <i data-lucide="message-circle" class="w-4 h-4"></i>
                                <span>${idea.commentCount || 0}</span>
                            </button>
                        </div>
                        <div class="idea-comments-section p-2 border-t border-gray-700/50 hidden"></div>
                    `;

                    ideaEl.querySelector('.like-idea-btn')?.addEventListener('click', (e) => { e.stopPropagation(); this.toggleLike(id); });
                    ideaEl.querySelector('.delete-idea-btn')?.addEventListener('click', (e) => { e.stopPropagation(); this.deleteIdea(id); });
                    ideaEl.querySelector('.edit-idea-btn')?.addEventListener('click', (e) => { e.stopPropagation(); this.showEditModal(id, idea); });
                    ideaEl.querySelectorAll('[data-action="view"]').forEach(el => el.addEventListener('click', () => this.showIdeaViewModal(id, idea)));
                    ideaEl.querySelector('.follow-btn')?.addEventListener('click', (e) => {
                        e.stopPropagation();
                        this.toggleFollow(idea.userId);
                    });
                    return ideaEl;
                },

                getVideoEmbedUrl(url) {
                    let videoId;
                    try {
                        const urlObj = new URL(url);
                        // YouTube URLs
                        if (urlObj.hostname.includes('youtube.com')) {
                            videoId = urlObj.searchParams.get('v');
                            if(videoId) return `https://www.youtube.com/embed/${videoId}`;
                        }
                        if (urlObj.hostname.includes('youtu.be')) {
                            videoId = urlObj.pathname.slice(1);
                             if(videoId) return `https://www.youtube.com/embed/${videoId}`;
                        }
                        // Vimeo URLs
                        if (urlObj.hostname.includes('vimeo.com')) {
                            videoId = urlObj.pathname.slice(1);
                             if(videoId && !isNaN(videoId)) return `https://player.vimeo.com/video/${videoId}`;
                        }
                    } catch(e) {
                        console.error("Invalid URL for video embed:", url);
                        return null;
                    }
                    return null;
                },

                async captureAndShowModal() {
                    if (!activeChartInstance) {
                        AlarmManager.showNotification("Lütfen önce bir grafik seçin.");
                        return;
                    }
                    const modal = document.getElementById('share-idea-modal');
                    const previewImg = document.getElementById('share-image-preview');
                    const publishButton = document.getElementById('publish-share-button');
                    const imageContainer = document.getElementById('share-image-container'); 
                    
                    try {
                        const canvas = await html2canvas(activeChartInstance.container, { useCORS: true, backgroundColor: chartBackgroundColor });
                        const imageData = canvas.toDataURL('image/png');
                        previewImg.src = imageData;
                        document.getElementById('share-title').value = '';
                        document.getElementById('share-description').value = '';
                        publishButton.textContent = 'Paylaş';
                        imageContainer.style.display = 'block'; 
                         imageContainer.querySelector('.flex').style.display = 'flex';
                        modal.style.display = 'flex';

                        publishButton.onclick = () => this.publishIdea();
                        document.getElementById('cancel-share-button').onclick = () => modal.style.display = 'none';
                        document.getElementById('close-share-modal-button').onclick = () => modal.style.display = 'none';
                        modal.onclick = (e) => { if(e.target === modal) modal.style.display = 'none'; };

                        makeModalResizable('share-idea-modal');
                        this.setupImagePanAndZoom();

                    } catch (error) {
                        console.error("Ekran görüntüsü alınamadı:", error);
                        AlarmManager.showNotification("Hata: Ekran görüntüsü alınamadı.");
                    }
                },
                
                showEditModal(ideaId, idea) {
                    const modal = document.getElementById('share-idea-modal');
                    const previewImg = document.getElementById('share-image-preview');
                    const titleInput = document.getElementById('share-title');
                    const descriptionInput = document.getElementById('share-description');
                    const videoUrlInput = document.getElementById('share-video-url');
                    const publishButton = document.getElementById('publish-share-button');
                    const imageContainer = document.getElementById('share-image-container');
                    
                    previewImg.src = idea.imageData;
                    titleInput.value = idea.title;
                    descriptionInput.value = idea.description;
                    videoUrlInput.value = idea.videoUrl || '';
                    publishButton.textContent = 'Güncelle';
                    imageContainer.style.display = 'block';
                    imageContainer.querySelector('.flex').style.display = 'none'; // Hide zoom controls
                    imageContainer.querySelector('#share-image-viewport').style.cursor = 'default';
                    
                    modal.style.display = 'flex';

                    publishButton.onclick = () => this.updateIdea(ideaId);
                    document.getElementById('cancel-share-button').onclick = () => modal.style.display = 'none';
                    document.getElementById('close-share-modal-button').onclick = () => modal.style.display = 'none';
                    modal.onclick = (e) => { if (e.target === modal) modal.style.display = 'none'; };
                    makeModalResizable('share-idea-modal');
                },

                async updateIdea(ideaId) {
                    const { db, doc, updateDoc } = window.firebaseTools;
                    const title = document.getElementById('share-title').value.trim();
                    const description = document.getElementById('share-description').value.trim();
                    const videoUrl = document.getElementById('share-video-url').value.trim();

                    if (!title) {
                        AlarmManager.showNotification("Başlık boş olamaz.");
                        return;
                    }

                    const ideaRef = doc(db, `artifacts/${appId}/public/data/shared_ideas`, ideaId);

                    try {
                        await updateDoc(ideaRef, { title, description, videoUrl });
                        AlarmManager.showNotification("Fikriniz güncellendi!");
                        document.getElementById('share-idea-modal').style.display = 'none';
                    } catch (error) {
                        console.error("Fikir güncellenemedi:", error);
                        AlarmManager.showNotification("Hata: Fikir güncellenemedi.");
                    }
                },

                async publishIdea() {
                    const viewport = document.getElementById('share-image-viewport');
                    const finalCanvas = await html2canvas(viewport, { useCORS: true, backgroundColor: chartBackgroundColor });
                    const finalImageData = finalCanvas.toDataURL('image/png');

                    const { auth, db, collection, addDoc, serverTimestamp } = window.firebaseTools;
                    const user = auth.currentUser;
                    if (!user) {
                         AlarmManager.showNotification("Fikir paylaşmak için giriş yapmalısınız.");
                         return;
                    }
                    const title = document.getElementById('share-title').value.trim();
                    const description = document.getElementById('share-description').value.trim();
                    const videoUrl = document.getElementById('share-video-url').value.trim();

                    if (!title) {
                         AlarmManager.showNotification("Lütfen bir başlık girin.");
                         return;
                    }

                    const username = user ? (user.displayName || 'YÖNETİCİ') : 'Anonim';
                    const ideasCol = collection(db, `artifacts/${appId}/public/data/shared_ideas`);

                    try {
                        await addDoc(ideasCol, {
                            userId: user.uid,
                            username: username,
                            title: title,
                            description: description,
                            imageData: finalImageData,
                            videoUrl: videoUrl,
                            symbol: activeChartInstance.symbol,
                            interval: activeChartInstance.interval,
                            likes: [],
                            commentCount: 0,
                            timestamp: serverTimestamp()
                        });
                        AlarmManager.showNotification("Fikriniz başarıyla paylaşıldı!");
                        document.getElementById('share-idea-modal').style.display = 'none';
                        document.getElementById('share-title').value = '';
                        document.getElementById('share-description').value = '';
                        document.getElementById('share-video-url').value = '';
                    } catch(error) {
                        console.error("Fikir paylaşılamadı:", error);
                        AlarmManager.showNotification("Hata: Fikir paylaşılamadı.");
                    }
                },
                
                async toggleLike(ideaId) {
                    const { auth, db, doc, updateDoc, arrayUnion, arrayRemove } = window.firebaseTools;
                    const user = auth.currentUser;
                    if (!user) return;
                    
                    const ideaRef = doc(db, `artifacts/${appId}/public/data/shared_ideas`, ideaId);
                    const likeBtn = document.querySelector(`.like-idea-btn[data-idea-id="${ideaId}"]`);
                    const isLiked = likeBtn ? likeBtn.classList.contains('text-blue-500') : false;

                    try {
                        if (isLiked) {
                            await updateDoc(ideaRef, { likes: arrayRemove(user.uid) });
                        } else {
                            await updateDoc(ideaRef, { likes: arrayUnion(user.uid) });
                        }
                    } catch (error) {
                        console.error("Beğeni hatası:", error);
                    }
                },
                 async toggleFollow(authorId) {
                    const { auth, db, doc, updateDoc, arrayUnion, arrayRemove, setDoc } = window.firebaseTools;
                    const user = auth.currentUser;
                    if (!user) return;

                    const userProfileRef = doc(db, `artifacts/${appId}/public/data/user_profiles`, user.uid);
                    const isFollowing = this.currentUserFollowing.includes(authorId);

                    try {
                        if (isFollowing) {
                            await updateDoc(userProfileRef, { following: arrayRemove(authorId) });
                        } else {
                             await setDoc(userProfileRef, { following: arrayUnion(authorId) }, { merge: true });
                        }
                    } catch (error) {
                        console.error("Takip etme hatası:", error);
                    }
                },

                async deleteIdea(ideaId) {
                    showConfirmationModal("Bu fikri silmek istediğinizden emin misiniz?", async () => {
                        const { db, doc, deleteDoc } = window.firebaseTools;
                         try {
                            const ideaRef = doc(db, `artifacts/${appId}/public/data/shared_ideas`, ideaId);
                            await deleteDoc(ideaRef);
                             AlarmManager.showNotification("Fikir silindi.");
                         } catch (error) {
                            console.error("Silme hatası:", error);
                             AlarmManager.showNotification("Hata: Fikir silinemedi.");
                         }
                    });
                },
                
                toggleCommentSection(button, ideaId) {
                    const commentSection = button.closest('.bg-gray-800').querySelector('.idea-comments-section');
                    const isHidden = commentSection.classList.toggle('hidden');

                    if (chatListeners.commentsUnsub[ideaId]) {
                        chatListeners.commentsUnsub[ideaId]();
                        delete chatListeners.commentsUnsub[ideaId];
                    }

                    if (!isHidden) {
                        this.loadComments(ideaId, commentSection);
                    }
                },
                
                loadComments(ideaId, targetElement, listenerIdSuffix = '') {
                    const { auth, db, collection, query, orderBy, onSnapshot, serverTimestamp, addDoc, updateDoc, doc, increment } = window.firebaseTools;
                    
                    const listenerId = ideaId + listenerIdSuffix;

                    const commentsCol = collection(db, `artifacts/${appId}/public/data/shared_ideas/${ideaId}/comments`);
                    const q = query(commentsCol, orderBy('timestamp', 'asc'));

                    if(chatListeners.commentsUnsub[listenerId]) chatListeners.commentsUnsub[listenerId]();

                    chatListeners.commentsUnsub[listenerId] = onSnapshot(q, (snapshot) => {
                        targetElement.innerHTML = ''; // Clear old comments
                        snapshot.forEach(doc => {
                             const comment = doc.data();
                             const commentEl = document.createElement('div');
                             commentEl.className = 'text-sm mb-2 p-2 bg-gray-700/50 rounded';
                             const time = comment.timestamp ? new Date(comment.timestamp.seconds * 1000).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) : '';
                             commentEl.innerHTML = `
                                 <div class="flex justify-between items-center">
                                     <span class="font-semibold text-blue-400">${comment.username}</span>
                                     <span class="text-xs text-gray-500">${time}</span>
                                 </div>
                                 <p class="text-gray-300 mt-1">${comment.text}</p>
                             `;
                             targetElement.appendChild(commentEl);
                        });
                        
                        // Add comment form at the end
                        const form = document.createElement('form');
                        form.className = 'mt-2';
                        form.innerHTML = `
                            <div class="relative flex items-center">
                                <input type="text" placeholder="Yorum yaz..." class="comment-input w-full bg-gray-900 border border-gray-600 rounded-md px-3 py-1.5 pr-10 focus:outline-none focus:ring-1 focus:ring-blue-500 text-sm">
                                <button type="submit" class="absolute right-2 p-1.5 rounded-md text-gray-400 hover:text-white hover:bg-blue-600">
                                    <i data-lucide="send" class="w-4 h-4"></i>
                                </button>
                            </div>
                        `;
                        targetElement.appendChild(form);
                        lucide.createIcons();

                        form.addEventListener('submit', async (e) => {
                            e.preventDefault();
                            const input = form.querySelector('.comment-input');
                            const text = input.value.trim();
                            const user = auth.currentUser;
                            if (text && user) {
                                const username = user ? (user.displayName || 'YÖNETİCİ') : 'Anonim';
                                await addDoc(commentsCol, {
                                    text: text,
                                    userId: user.uid,
                                    username: username,
                                    timestamp: serverTimestamp()
                                });
                                const ideaRef = doc(db, `artifacts/${appId}/public/data/shared_ideas`, ideaId);
                                await updateDoc(ideaRef, { commentCount: increment(1) });
                                input.value = '';
                            }
                        });
                    });
                },
                setupImagePanAndZoom() {
                    const viewport = document.getElementById('share-image-viewport');
                    const image = document.getElementById('share-image-preview');
                    const zoomInBtn = document.getElementById('zoom-in-btn');
                    const zoomOutBtn = document.getElementById('zoom-out-btn');
                    const resetZoomBtn = document.getElementById('reset-zoom-btn');

                    if (!viewport || !image || !zoomInBtn || !zoomOutBtn || !resetZoomBtn) return;

                    let scale = 1;
                    let translateX = 0;
                    let translateY = 0;
                    let isPanning = false;
                    let startX, startY;

                    const updateTransform = () => {
                        image.style.transform = `translate(${translateX}px, ${translateY}px) scale(${scale})`;
                    };

                    zoomInBtn.onclick = () => {
                        scale *= 1.2;
                        updateTransform();
                    };

                    zoomOutBtn.onclick = () => {
                        scale /= 1.2;
                        updateTransform();
                    };

                    resetZoomBtn.onclick = () => {
                        scale = 1;
                        translateX = 0;
                        translateY = 0;
                        updateTransform();
                    };

                    viewport.onmousedown = (e) => {
                        e.preventDefault();
                        isPanning = true;
                        startX = e.clientX - translateX;
                        startY = e.clientY - translateY;
                        viewport.style.cursor = 'grabbing';
                    };

                    viewport.onmousemove = (e) => {
                        if (!isPanning) return;
                        translateX = e.clientX - startX;
                        translateY = e.clientY - startY;
                        updateTransform();
                    };
                    
                    viewport.onmouseup = () => {
                        isPanning = false;
                        viewport.style.cursor = 'grab';
                    };
                    
                    viewport.onmouseleave = () => {
                        isPanning = false;
                        viewport.style.cursor = 'grab';
                    };

                    // Reset on modal open
                    scale = 1;
                    translateX = 0;
                    translateY = 0;
                    updateTransform();
                },

                showIdeaViewModal(ideaId, idea) {
                    const modal = document.getElementById('idea-view-modal');
                    if (!modal) return;

                    document.getElementById('idea-view-title').textContent = idea.title;
                    document.getElementById('idea-view-author').textContent = `${idea.username} - ${new Date(idea.timestamp.seconds * 1000).toLocaleString('tr-TR')}`;
                    document.getElementById('idea-view-description').textContent = idea.description;
                    document.getElementById('idea-view-image').src = idea.imageData;
                    
                    const videoContainer = document.getElementById('idea-view-video-container');
                    if (idea.videoUrl) {
                        const embedUrl = this.getVideoEmbedUrl(idea.videoUrl);
                        if (embedUrl) {
                            videoContainer.innerHTML = `<iframe src="${embedUrl}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen class="w-full h-full rounded-md bg-black"></iframe>`;
                            videoContainer.classList.remove('hidden');
                        } else {
                            videoContainer.classList.add('hidden');
                        }
                    } else {
                        videoContainer.classList.add('hidden');
                    }
                    
                    const closeButton = document.getElementById('close-idea-view-modal-button');
                    
                    const close = () => {
                        modal.style.display = 'none';
                        const commentsContainer = document.getElementById('idea-view-comments');
                        if (commentsContainer) commentsContainer.innerHTML = '';
                        
                        const listenerId = ideaId + '_modal';
                        if (chatListeners.commentsUnsub[listenerId]) {
                            chatListeners.commentsUnsub[listenerId]();
                            delete chatListeners.commentsUnsub[listenerId];
                        }
                    };

                    closeButton.onclick = close;
                    modal.onclick = (e) => {
                        if (e.target === modal) {
                            close();
                        }
                    };

                    modal.style.display = 'flex';
                    this.loadComments(ideaId, document.getElementById('idea-view-comments'), '_modal');
                }
            };
            
            function showConfirmationModal(message, onConfirm) {
                const modal = document.getElementById('confirmation-modal');
                const messageEl = document.getElementById('confirmation-message');
                const okButton = document.getElementById('confirm-ok-button');
                const cancelButton = document.getElementById('confirm-cancel-button');

                messageEl.textContent = message;
                modal.style.display = 'flex';

                const close = () => {
                    modal.style.display = 'none';
                    okButton.replaceWith(okButton.cloneNode(true));
                    cancelButton.replaceWith(cancelButton.cloneNode(true));
                };

                document.getElementById('confirm-ok-button').onclick = () => {
                    onConfirm();
                    close();
                };
                document.getElementById('confirm-cancel-button').onclick = close;
                
                modal.onclick = (e) => {
                     if (e.target === modal) close();
                };
            }
            
            function makeModalResizable(modalId) {
                const modalContent = document.getElementById(modalId)?.querySelector('.bg-gray-800');
                const resizer = modalContent?.querySelector('.modal-resizer');
                
                if (!modalContent || !resizer) return;
                
                let isResizing = false;

                resizer.addEventListener('mousedown', function(e) {
                    isResizing = true;
                    let startX = e.clientX;
                    let startY = e.clientY;
                    let startWidth = parseInt(document.defaultView.getComputedStyle(modalContent).width, 10);
                    let startHeight = parseInt(document.defaultView.getComputedStyle(modalContent).height, 10);

                    function doDrag(e) {
                        if (!isResizing) return;
                        modalContent.style.width = (startWidth + e.clientX - startX) + 'px';
                        modalContent.style.height = (startHeight + e.clientY - startY) + 'px';
                    }

                    function stopDrag() {
                        isResizing = false;
                        document.removeEventListener('mousemove', doDrag);
                        document.removeEventListener('mouseup', stopDrag);
                    }

                    document.addEventListener('mousemove', doDrag);
                    document.addEventListener('mouseup', stopDrag);
                });
            }


            // --- UYGULAMAYI BAŞLAT ---
            const savedBgColor = localStorage.getItem('chartBackgroundColor');
            if (savedBgColor) {
                chartBackgroundColor = savedBgColor;
                chartTextColor = getContrastingTextColor(chartBackgroundColor);
            }
            const savedCrosshairColor = localStorage.getItem('chartCrosshairColor');
            if (savedCrosshairColor) {
                crosshairColor = savedCrosshairColor;
            }
            const savedCrosshairWidth = localStorage.getItem('chartCrosshairWidth');
            if (savedCrosshairWidth) {
                crosshairWidth = parseInt(savedCrosshairWidth, 10);
            }
            const savedCrosshairStyle = localStorage.getItem('chartCrosshairStyle');
            if (savedCrosshairStyle) {
                crosshairStyle = parseInt(savedCrosshairStyle, 10);
            }
            applyLayout('1x1');
            TimeframeManager.load();
            fetchAllSymbols().then(() => {
                 subscribeToAllTickers();
            });
            setupUIListeners();
            renderIndicatorsMenu();
        });
    </script>
</body>
</html>







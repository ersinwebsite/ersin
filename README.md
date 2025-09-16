<!DOCTYPE html>
<html lang="tr" class="h-full">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TradingView Tarzı Grafik Prototipi</title>
    <!-- Tailwind CSS for styling -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- TradingView Lightweight Charts Library -->
    <script src="https://unpkg.com/lightweight-charts@3.8.0/dist/lightweight-charts.standalone.production.js"></script>
    <!-- Split.js for resizable panes -->
    <script src="https://unpkg.com/split.js/dist/split.min.js"></script>
    <style>
        /* Custom styles for a better look and feel */
        body {
            font-family: 'Inter', sans-serif;
        }
        /* Custom scrollbar */
        ::-webkit-scrollbar { width: 8px; height: 8px; }
        ::-webkit-scrollbar-track { background: #1e293b; }
        ::-webkit-scrollbar-thumb { background: #475569; border-radius: 10px; }
        ::-webkit-scrollbar-thumb:hover { background: #64748b; }
        
        /* Tab styles */
        .tab-btn { 
            background-color: #374151; /* bg-gray-700 */
            transition: all 0.2s ease-in-out; 
            color: #d1d5db;
            border-radius: 0.375rem; /* rounded-md */
        }
        .tab-btn:hover { 
            background-color: #4B5563; /* bg-gray-600 */
            color: #ffffff; 
        }
        .tab-btn.active { 
            background-color: #2563EB; /* bg-blue-600 */
            color: white; 
        }
        
        /* Active coin in sidebar */
        .coin-item.active { background-color: #3b82f6; }
        .coin-item.active:hover { background-color: #2563eb; }

        /* Styles for resizable split panes */
        .split { display: flex; flex-direction: row; }
        .gutter { background-color: #4b5563; background-repeat: no-repeat; background-position: 50%; }
        .gutter.gutter-horizontal { cursor: col-resize; background-image: url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAeCAYAAADkftS9AAAAIklEQVQoU2M4c+bM/5+BgoCnA0AGiI0xEwU6GgAA+v8DARHyL2kAAAAASUVORK5CYII='); }
        .gutter.gutter-vertical { cursor: row-resize; background-image: url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB4AAAAFAQMAAABo7865AAAABlBMVEVHcEzMzMzyAv2sAAAAAXRSTlMAQObYZgAAABBJREFUeF5jOAMEEAIEEFwAn3kMwcB6I2AAAAAASUVORK5CYII='); }
        
        /* Styles for chart grid */
        .chart-grid-container { width: 100%; height: 100%; }
        .chart-pane { position: relative; overflow: hidden; border: 2px solid transparent; transition: border-color 0.2s; }
        .chart-pane.active { border-color: #3b82f6; }
        .chart-pane.replay-active { cursor: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="6" cy="6" r="3"></circle><circle cx="6" cy="18" r="3"></circle><line x1="20" y1="4" x2="8.12" y2="15.88"></line><line x1="14.47" y1="14.48" x2="20" y2="20"></line><line x1="8.12" y1="8.12" x2="12" y2="12"></line></svg>') 12 12, auto; }
        .chart-pane.drawing-cursor .tv-lightweight-charts { cursor: crosshair !important; }

        /* Custom style for color input */
        input[type="color"]::-webkit-color-swatch-wrapper { padding: 0; }
        input[type="color"]::-webkit-color-swatch { border: none; border-radius: 4px; }
        
        /* Gemini loading spinner */
        .spinner {
            border: 2px solid #374151; /* Lighter border */
            border-top: 2px solid #3b82f6; /* Blue border */
            border-radius: 50%;
            width: 16px;
            height: 16px;
            animation: spin 1s linear infinite;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        /* Drawing Toolbar Styles */
        #drawing-toolbar {
            transition: transform 0.3s ease-in-out;
        }
        #drawing-toolbar.hidden {
            transform: translateX(-100%);
        }
        .drawing-tool-btn.active {
            background-color: #2563eb;
            color: white;
        }
    </style>
    <!-- Google Fonts for a nice typography -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
</head>
<body class="bg-gray-900 text-white antialiased overflow-hidden flex flex-col h-screen">

    <div class="w-full h-full p-4 flex flex-col flex-grow">
        <!-- Header Section -->
        <header class="flex-shrink-0">
            <!-- Header can be used for a logo or main title if needed -->
        </header>

        <!-- Main Chart Section -->
        <main class="bg-gray-800 rounded-lg shadow-2xl flex flex-col flex-grow min-h-0">
            <!-- Chart Header: Tabs, Indicators, and Timeframe Dropdown -->
            <div class="flex justify-between items-center p-2 border-b border-gray-700 flex-shrink-0">
                <!-- Left side: Tabs and Indicators -->
                <div class="flex items-center space-x-2">
                     <div class="flex space-x-2">
                        <button id="chart-tab" class="tab-btn active px-3 py-1 text-sm font-medium">Grafik</button>
                        <button id="pine-tab" class="tab-btn px-3 py-1 text-sm font-medium">Kodyaz</button>
                    </div>

                    <div class="relative" id="timeframe-dropdown">
                        <button id="timeframe-toggle" class="flex items-center space-x-2 px-3 py-1 text-sm rounded-md bg-gray-700 hover:bg-gray-600 transition-colors">
                            <span id="current-timeframe-label" class="font-semibold">1h</span>
                            <svg class="h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" /></svg>
                        </button>
                        <div id="timeframe-menu" class="absolute left-0 mt-2 w-36 bg-gray-700 rounded-md shadow-lg z-20 hidden">
                            <a href="#" data-interval="1m" class="timeframe-item block px-4 py-2 text-sm text-white hover:bg-blue-600 rounded-t-md">1 Dakika</a>
                            <a href="#" data-interval="5m" class="timeframe-item block px-4 py-2 text-sm text-white hover:bg-blue-600">5 Dakika</a>
                            <a href="#" data-interval="15m" class="timeframe-item block px-4 py-2 text-sm text-white hover:bg-blue-600">15 Dakika</a>
                            <a href="#" data-interval="1h" class="timeframe-item block px-4 py-2 text-sm text-white hover:bg-blue-600">1 Saat</a>
                            <a href="#" data-interval="4h" class="timeframe-item block px-4 py-2 text-sm text-white hover:bg-blue-600">4 Saat</a>
                            <a href="#" data-interval="1d" class="timeframe-item block px-4 py-2 text-sm text-white hover:bg-blue-600 rounded-b-md">1 Gün</a>
                        </div>
                    </div>

                     <!-- Layout Dropdown -->
                    <div class="relative" id="layout-dropdown">
                        <button id="layout-toggle" class="px-3 py-1 text-sm rounded-md bg-gray-700 hover:bg-gray-600 transition-colors">
                            <span class="font-semibold">Bölme</span>
                        </button>
                        <div id="layout-menu" class="absolute left-0 mt-2 p-2 w-48 bg-gray-700 rounded-md shadow-lg z-20 hidden">
                            <div class="flex flex-col space-y-1">
                                <button data-layout="1x1" class="layout-item w-full flex items-center space-x-3 p-2 text-sm text-left text-white hover:bg-blue-600 rounded">
                                    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 flex-shrink-0"><path d="M21 3H3v18h18V3z" stroke="currentColor" stroke-width="2"></path></svg>
                                    <span>Tekli</span>
                                </button>
                                <button data-layout="2x1v" class="layout-item w-full flex items-center space-x-3 p-2 text-sm text-left text-white hover:bg-blue-600 rounded">
                                    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 flex-shrink-0"><path d="M3 3h18v18H3V3zm9-1v20" stroke="currentColor" stroke-width="2"></path></svg>
                                    <span>Dikey İkili</span>
                                </button>
                                <button data-layout="2x1h" class="layout-item w-full flex items-center space-x-3 p-2 text-sm text-left text-white hover:bg-blue-600 rounded">
                                    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 flex-shrink-0"><path d="M3 3h18v18H3V3zM2 12h20" stroke="currentColor" stroke-width="2"></path></svg>
                                    <span>Yatay İkili</span>
                                </button>
                                <button data-layout="3x1v" class="layout-item w-full flex items-center space-x-3 p-2 text-sm text-left text-white hover:bg-blue-600 rounded">
                                    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 flex-shrink-0"><path d="M3 3h18v18H3V3zM8 2v20M16 2v20" stroke="currentColor" stroke-width="2"></path></svg>
                                    <span>Dikey Üçlü</span>
                                </button>
                                <button data-layout="3x1h" class="layout-item w-full flex items-center space-x-3 p-2 text-sm text-left text-white hover:bg-blue-600 rounded">
                                    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 flex-shrink-0"><path d="M3 3h18v18H3V3zM2 8h20M2 16h20" stroke="currentColor" stroke-width="2"></path></svg>
                                    <span>Yatay Üçlü</span>
                                </button>
                                <button data-layout="2x2" class="layout-item w-full flex items-center space-x-3 p-2 text-sm text-left text-white hover:bg-blue-600 rounded">
                                    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 flex-shrink-0"><path d="M3 3h18v18H3V3zM12 2v20M2 12h20" stroke="currentColor" stroke-width="2"></path></svg>
                                    <span>Dörtlü</span>
                                </button>
                            </div>
                        </div>
                    </div>

                    <!-- Indicators Dropdown -->
                    <div class="relative" id="indicators-dropdown">
                        <button id="indicators-toggle" class="px-3 py-1 text-sm rounded-md bg-gray-700 hover:bg-gray-600 transition-colors">
                            <span class="font-semibold">Gösterge</span>
                        </button>
                        <div id="indicators-menu" class="absolute left-0 mt-2 w-56 bg-gray-700 rounded-md shadow-lg z-20 hidden">
                            <!-- Menu content generated by JS -->
                        </div>
                    </div>

                    <!-- Replay Button -->
                    <button id="replay-btn" class="flex items-center space-x-2 px-3 py-1 text-sm rounded-md bg-gray-700 hover:bg-gray-600 transition-colors">
                        <svg class="h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" /><path stroke-linecap="round" stroke-linejoin="round" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                        <span id="replay-btn-text" class="font-semibold">Tekrar</span>
                    </button>
                </div>
                
                <!-- Right side: Settings -->
                <div class="flex items-center space-x-2">
                     <!-- Settings Dropdown -->
                    <div class="relative" id="settings-dropdown">
                        <button id="settings-toggle" class="p-2 text-sm rounded-md bg-gray-700 hover:bg-gray-600 transition-colors">
                            <svg class="w-4 h-4 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                                <path fill-rule="evenodd" d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0l-.1.41a1.5 1.5 0 01-2.1 1.45l-.41-.1a1.5 1.5 0 00-1.74 1.06l-.27.48a1.5 1.5 0 00.92 1.95l.38.19a1.5 1.5 0 010 2.62l-.38.19a1.5 1.5 0 00-.92 1.95l.27.48a1.5 1.5 0 001.74 1.06l.41-.1a1.5 1.5 0 012.1 1.45l.1.41c.38 1.56 2.6 1.56 2.98 0l.1-.41a1.5 1.5 0 012.1-1.45l.41.1a1.5 1.5 0 001.74-1.06l.27-.48a1.5 1.5 0 00-.92-1.95l-.38-.19a1.5 1.5 0 010-2.62l.38-.19a1.5 1.5 0 00.92-1.95l-.27-.48a1.5 1.5 0 00-1.74-1.06l-.41.1a1.5 1.5 0 01-2.1-1.45l-.1-.41zM10 13a3 3 0 100-6 3 3 0 000 6z" clip-rule="evenodd" />
                            </svg>
                        </button>
                        <div id="settings-menu" class="absolute right-0 mt-2 p-3 w-56 bg-gray-700 rounded-md shadow-lg z-20 hidden">
                            <div class="flex items-center justify-between">
                                <label for="background-color-picker" class="text-sm text-white">Grafik Arka Plan</label>
                                <div class="flex items-center space-x-2">
                                    <input type="color" id="background-color-picker" value="#1f2937" class="w-8 h-8 p-0 border-none rounded cursor-pointer bg-transparent">
                                    <button id="save-color-btn" title="Rengi Kaydet" class="p-1.5 text-gray-400 hover:text-white hover:bg-gray-600 rounded-md transition-colors">
                                        <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                                            <path d="M5 4a2 2 0 012-2h6a2 2 0 012 2v12l-5-3-5 3V4z" />
                                        </svg>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                     <button id="sidebar-toggle" class="p-2 rounded-md bg-gray-700 hover:bg-gray-600 transition-colors" title="İzleme Listesini Aç">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h7" />
                        </svg>
                    </button>
                </div>
            </div>

            <!-- Tab Content -->
            <div id="tab-content-wrapper" class="flex-grow relative min-h-0">
                <!-- Chart Panel -->
                <div id="chart-panel" class="w-full h-full relative">
                    <!-- Drawing Toolbar -->
                    <div id="drawing-toolbar-container" class="absolute top-0 left-0 h-full z-20 flex items-center">
                        <div id="drawing-toolbar" class="bg-gray-900/50 backdrop-blur-sm p-1.5 rounded-r-lg flex flex-col items-center space-y-2 hidden">
                            <button data-tool="cursor" class="drawing-tool-btn active p-2 rounded-md hover:bg-gray-700 transition-colors" title="İmleç">
                                <svg class="w-5 h-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 15l-2 5L9 4l11 4-5 2zm0 0l5 5M7.188 8.812l5.938 2.375" /></svg>
                            </button>
                            <button data-tool="trendline" class="drawing-tool-btn p-2 rounded-md hover:bg-gray-700 transition-colors" title="Trend Çizgisi">
                                <svg class="w-5 h-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="19" x2="19" y2="5"></line></svg>
                            </button>
                             <button data-tool="fib" class="drawing-tool-btn p-2 rounded-md hover:bg-gray-700 transition-colors" title="Fibonacci Düzeltmesi">
                                <svg class="w-5 h-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"/><path d="M21 12H3"/><path d="M21 8H3"/><path d="M21 16H3"/></svg>
                            </button>
                            <button data-tool="rectangle" class="drawing-tool-btn p-2 rounded-md hover:bg-gray-700 transition-colors" title="Dikdörtgen">
                                <svg class="w-5 h-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect></svg>
                            </button>
                             <div class="border-t border-gray-700 w-full my-1"></div>
                            <button data-tool="clear" class="p-2 rounded-md hover:bg-gray-700 text-red-500 hover:text-red-400 transition-colors" title="Tüm Çizimleri Sil">
                                <svg class="w-5 h-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" /></svg>
                            </button>
                        </div>
                         <button id="drawing-toolbar-toggle" class="bg-gray-900/50 hover:bg-gray-700/80 p-1 rounded-r-lg transition-colors">
                            <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" /></svg>
                        </button>
                    </div>

                    <div id="chart-grid-container" class="w-full h-full">
                         <!-- Chart panes will be injected here by JS -->
                    </div>
                    <div id="loading-indicator" class="absolute inset-0 flex items-center justify-center bg-gray-800 bg-opacity-75 z-10 hidden">
                        <p class="text-lg font-medium">Grafik verileri yükleniyor...</p>
                    </div>
                     <!-- Replay Controls -->
                    <div id="replay-controls" class="absolute bottom-4 left-1/2 -translate-x-1/2 bg-gray-900/80 backdrop-blur-sm p-2 rounded-lg shadow-2xl flex items-center space-x-4 z-20 hidden">
                        <button id="replay-play-pause" class="p-2 hover:bg-gray-700 rounded-md transition-colors">
                            <svg id="play-icon" class="w-5 h-5" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8.118v3.764a1 1 0 001.555.832l3.197-1.882a1 1 0 000-1.664l-3.197-1.882z" clip-rule="evenodd" /></svg>
                            <svg id="pause-icon" class="w-5 h-5 hidden" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zM7 8a1 1 0 012 0v4a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v4a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" /></svg>
                        </button>
                        <button id="replay-forward" class="p-2 hover:bg-gray-700 rounded-md transition-colors">
                            <svg class="w-5 h-5" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" /></svg>
                        </button>
                        <select id="replay-speed" class="bg-gray-700 text-white text-sm rounded-md p-1 border border-transparent focus:outline-none focus:ring-2 focus:ring-blue-500">
                            <option value="1000">1x</option>
                            <option value="500">2x</option>
                            <option value="200">5x</option>
                        </select>
                        <button id="replay-exit" class="p-2 text-red-500 hover:bg-red-500 hover:text-white rounded-md transition-colors">
                            <svg class="w-5 h-5" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" /></svg>
                        </button>
                    </div>
                </div>
                 <!-- Pine Script Editor Panel -->
                <div id="pine-panel" class="hidden h-full flex flex-col">
                    <div class="p-2 bg-gray-900/50 rounded-t-md border-b border-gray-700">
                        <div class="flex items-center space-x-2">
                             <input type="text" id="script-prompt-input" class="flex-grow bg-gray-700 text-white p-2 rounded-md border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm" placeholder="Örn: 50 ve 100 günlük hareketli ortalamaları çizdir">
                             <button id="generate-script-btn" class="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 px-3 rounded-md transition-colors text-sm flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed">
                                <span id="generate-btn-text">Kod Oluştur ✨</span>
                                <div id="generate-spinner" class="spinner hidden ml-2"></div>
                            </button>
                        </div>
                    </div>
                    <textarea id="pine-editor" class="w-full flex-grow bg-gray-900 text-gray-300 font-mono p-4 resize-none border-x border-gray-700 focus:outline-none"></textarea>
                    <div class="flex items-center justify-end space-x-2 bg-gray-700 p-2 rounded-b-md">
                        <button id="apply-script-btn" class="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-1 px-3 rounded-md transition-colors text-sm">Uygula</button>
                        <button id="save-script-btn" class="bg-green-600 hover:bg-green-700 text-white font-semibold py-1 px-3 rounded-md transition-colors text-sm">Kaydet</button>
                    </div>
                </div>
            </div>
        </main>
    </div>

    <!-- Sidebar Overlay -->
    <div id="sidebar-overlay" class="fixed inset-0 bg-black bg-opacity-50 z-30 hidden"></div>
    
    <!-- Sidebar -->
    <aside id="sidebar" class="fixed top-0 right-0 h-full w-72 bg-gray-800 shadow-2xl transform translate-x-full transition-transform duration-300 ease-in-out z-40 flex flex-col">
        <div class="p-4 border-b border-gray-700 flex justify-between items-center">
            <h2 class="text-lg font-bold">İzleme Listesi</h2>
            <button id="sidebar-close" class="p-1 hover:bg-gray-700 rounded-md" title="Kapat">
                <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
            </button>
        </div>
        <ul id="coin-list" class="flex-grow overflow-y-auto">
           <!-- Coin list items will be generated by JS -->
        </ul>
        <div class="p-2 border-t border-gray-700">
            <button id="add-coin-btn" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors flex items-center justify-center">
                 <svg class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" /></svg>
                Ekle
            </button>
        </div>
    </aside>

    <!-- Add Coin Modal -->
    <div id="add-coin-modal" class="fixed inset-0 bg-black bg-opacity-60 z-50 hidden items-center justify-center">
        <div class="bg-gray-800 rounded-lg shadow-2xl p-6 w-full max-w-sm">
            <h3 class="text-xl font-bold mb-4">Yeni Varlık Ekle</h3>
            <p class="text-gray-400 text-sm mb-4">Binance sembolünü girin (örn: DOGEUSDT, SHIBUSDT).</p>
            <input type="text" id="new-coin-input" class="w-full bg-gray-900 text-white p-2 rounded-md border border-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 uppercase" placeholder="AVAXUSDT">
            <div class="flex justify-end space-x-3 mt-5">
                <button id="modal-cancel-btn" class="px-4 py-2 bg-gray-600 hover:bg-gray-700 rounded-md transition-colors">İptal</button>
                <button id="modal-add-btn" class="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-md transition-colors">Ekle</button>
            </div>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', () => {
            // --- DOM element references ---
            const loadingIndicator = document.getElementById('loading-indicator');
            const chartTab = document.getElementById('chart-tab');
            const pineTab = document.getElementById('pine-tab');
            const chartPanel = document.getElementById('chart-panel');
            const pinePanel = document.getElementById('pine-panel');
            const pineEditor = document.getElementById('pine-editor');
            const applyScriptBtn = document.getElementById('apply-script-btn');
            const saveScriptBtn = document.getElementById('save-script-btn');
            const scriptPromptInput = document.getElementById('script-prompt-input');
            const generateScriptBtn = document.getElementById('generate-script-btn');
            const generateBtnText = document.getElementById('generate-btn-text');
            const generateSpinner = document.getElementById('generate-spinner');
            const sidebar = document.getElementById('sidebar');
            const sidebarToggle = document.getElementById('sidebar-toggle');
            const sidebarClose = document.getElementById('sidebar-close');
            const sidebarOverlay = document.getElementById('sidebar-overlay');
            const coinList = document.getElementById('coin-list');
            const addCoinBtn = document.getElementById('add-coin-btn');
            const addCoinModal = document.getElementById('add-coin-modal');
            const modalCancelBtn = document.getElementById('modal-cancel-btn');
            const modalAddBtn = document.getElementById('modal-add-btn');
            const newCoinInput = document.getElementById('new-coin-input');
            const timeframeDropdown = document.getElementById('timeframe-dropdown');
            const timeframeToggle = document.getElementById('timeframe-toggle');
            const timeframeMenu = document.getElementById('timeframe-menu');
            const currentTimeframeLabel = document.getElementById('current-timeframe-label');
            const indicatorsDropdown = document.getElementById('indicators-dropdown');
            const indicatorsToggle = document.getElementById('indicators-toggle');
            const indicatorsMenu = document.getElementById('indicators-menu');
            const layoutDropdown = document.getElementById('layout-dropdown');
            const layoutToggle = document.getElementById('layout-toggle');
            const layoutMenu = document.getElementById('layout-menu');
            const chartGridContainer = document.getElementById('chart-grid-container');
            const settingsDropdown = document.getElementById('settings-dropdown');
            const settingsToggle = document.getElementById('settings-toggle');
            const settingsMenu = document.getElementById('settings-menu');
            const backgroundColorPicker = document.getElementById('background-color-picker');
            const saveColorBtn = document.getElementById('save-color-btn');
            const replayBtn = document.getElementById('replay-btn');
            const replayBtnText = document.getElementById('replay-btn-text');
            const replayControls = document.getElementById('replay-controls');
            const replayPlayPauseBtn = document.getElementById('replay-play-pause');
            const playIcon = document.getElementById('play-icon');
            const pauseIcon = document.getElementById('pause-icon');
            const replayForwardBtn = document.getElementById('replay-forward');
            const replaySpeedSelect = document.getElementById('replay-speed');
            const replayExitBtn = document.getElementById('replay-exit');
            const drawingToolbar = document.getElementById('drawing-toolbar');
            const drawingToolbarToggle = document.getElementById('drawing-toolbar-toggle');


            // --- Global State ---
            let chartInstances = [];
            let activeChartId = null;
            let splitInstance = null;
            let watchlistSymbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT', 'ADAUSDT'];
            let lastPrices = {};
            let customScripts = {};
            let currentBackgroundColor = '#1f2937';

            // Replay Mode State
            let isReplayModeActive = false;
            let replayState = {
                instance: null,
                fullData: [],
                futureData: [],
                currentIndex: 0,
                isPlaying: false,
                timer: null,
                speed: 1000,
            };

            // Drawing State
            let activeDrawingTool = 'cursor';
            let isDrawing = false;
            let drawingStartPoint = null;

            // --- WebSocket Management (Centralized) ---
            let mainSocket = null;
            let activeStreams = new Set();
            let subscriptionIdCounter = 1;

            const defaultScript = 
`/**
 * Bu alanda JavaScript kullanarak kendi göstergenizi yazabilirsiniz.
 * Fonksiyonunuz 'data' adında bir dizi alır. 
 * Her dizi elemanı: { time, open, high, low, close }
 * * Fonksiyonunuz { time, value } formatında bir dizi döndürmelidir.
 * Aşağıdaki örnek 20 periyotluk bir Basit Hareketli Ortalama (SMA) hesaplar.
 */

const period = 20;
const result = [];

for (let i = period - 1; i < data.length; i++) {
    let sum = 0;
    for (let j = 0; j < period; j++) {
        sum += data[i - j].close;
    }
    result.push({
        time: data[i].time,
        value: sum / period,
    });
}

return result;
`;
            pineEditor.value = defaultScript;
            
             // --- Gemini API Integration ---
            const API_KEY = ""; // Keep this empty.
            const API_URL = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key=${API_KEY}`;
            
            async function callGeminiAPI(prompt, systemInstruction = "") {
                const payload = {
                    contents: [{ parts: [{ text: prompt }] }],
                };

                if (systemInstruction) {
                    payload.systemInstruction = { parts: [{ text: systemInstruction }] };
                }

                try {
                    const response = await fetch(API_URL, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(payload)
                    });

                    if (!response.ok) {
                        const errorBody = await response.json();
                        console.error("Gemini API Error:", errorBody);
                        throw new Error(`API isteği başarısız oldu: ${response.status}`);
                    }

                    const result = await response.json();
                    return result.candidates?.[0]?.content?.parts?.[0]?.text || "";
                } catch (error) {
                    console.error("Gemini API çağrısı sırasında hata:", error);
                    throw error;
                }
            }


            // --- Chart & Layout Management ---

            function createChartInstance(container, id, initialState) {
                if (typeof LightweightCharts === 'undefined') {
                    console.error('LightweightCharts library is not loaded.');
                    container.innerHTML = '<p class="text-red-500 text-center p-4">Grafik kütüphanesi yüklenemedi.</p>';
                    return null;
                }

                const chart = LightweightCharts.createChart(container, {
                    width: container.clientWidth,
                    height: container.clientHeight,
                    layout: { 
                        backgroundColor: currentBackgroundColor, 
                        textColor: 'rgba(229, 231, 235, 1)' 
                    },
                    grid: { 
                        vertLines: { visible: false }, 
                        horzLines: { visible: false } 
                    },
                    crosshair: { mode: LightweightCharts.CrosshairMode.Normal },
                    rightPriceScale: { 
                        borderColor: '#4b5563',
                    },
                    timeScale: { 
                        borderColor: '#4b5563', 
                        timeVisible: true, 
                        secondsVisible: false,
                    },
                });

                const candlestickSeries = chart.addCandlestickSeries({
                    upColor: '#22c55e', downColor: '#ef4444', borderDownColor: '#ef4444',
                    borderUpColor: '#22c55e', wickDownColor: '#ef4444', wickUpColor: '#22c55e',
                    priceLineVisible: false,
                });

                const instance = {
                    id,
                    container,
                    chart,
                    candlestickSeries,
                    symbol: initialState.symbol,
                    interval: initialState.interval,
                    historicalData: [],
                    activeIndicators: {},
                    drawings: [],
                };
                
                fetchHistoricalData(instance);

                container.parentElement.addEventListener('click', () => {
                     if (isReplayModeActive && !replayState.instance) return;
                     if (isDrawing) return;
                    setActiveChart(id)
                });
                 
                chart.subscribeClick(param => {
                     if (isReplayModeActive && replayState.instance?.id === id) {
                        handleReplayCut(param.time);
                        return;
                    }

                    if (activeDrawingTool !== 'cursor' && instance.id === activeChartId) {
                        handleDrawing(param, instance);
                    }
                });
                
                return instance;
            }

            function destroyAllCharts() {
                if (splitInstance) {
                    splitInstance.destroy();
                    splitInstance = null;
                }
                const streamsToUnsub = chartInstances.map(inst => `${inst.symbol.toLowerCase()}@kline_${inst.interval}`);
                unsubscribeFromStreams(streamsToUnsub);

                chartInstances.forEach(instance => {
                    if (instance.chart) instance.chart.remove();
                });
                chartInstances = [];
                chartGridContainer.innerHTML = '';
            }

            function applyLayout(layoutType) {
                destroyAllCharts();
                
                chartGridContainer.removeAttribute('style');
                
                const getInitialState = (index) => ({
                    symbol: watchlistSymbols[index] || 'BTCUSDT',
                    interval: '1h',
                });
                
                const splitOptions = {
                    minSize: 100,
                    onDrag: () => {
                        chartInstances.forEach(instance => {
                            if (instance.chart) {
                                instance.chart.resize(instance.container.clientWidth, instance.container.clientHeight);
                            }
                        });
                    }
                };

                if (layoutType === '1x1') {
                    chartGridContainer.style.display = 'grid';
                    const pane = document.createElement('div');
                    pane.id = 'pane-0';
                    pane.className = 'chart-pane w-full h-full';
                    chartGridContainer.appendChild(pane);
                    chartInstances.push(createChartInstance(pane, 0, getInitialState(0)));
                } else if (layoutType === '2x1v') {
                    chartGridContainer.style.display = 'flex';
                    chartGridContainer.style.flexDirection = 'row';
                    chartGridContainer.innerHTML = '<div id="pane-0" class="chart-pane"></div><div id="pane-1" class="chart-pane"></div>';
                    chartInstances.push(createChartInstance(document.getElementById('pane-0'), 0, getInitialState(0)));
                    chartInstances.push(createChartInstance(document.getElementById('pane-1'), 1, getInitialState(1)));
                    splitInstance = Split(['#pane-0', '#pane-1'], { ...splitOptions, direction: 'horizontal', sizes: [50, 50] });
                } else if (layoutType === '2x1h') {
                    chartGridContainer.style.display = 'flex';
                    chartGridContainer.style.flexDirection = 'column';
                    chartGridContainer.innerHTML = '<div id="pane-0" class="chart-pane"></div><div id="pane-1" class="chart-pane"></div>';
                    chartInstances.push(createChartInstance(document.getElementById('pane-0'), 0, getInitialState(0)));
                    chartInstances.push(createChartInstance(document.getElementById('pane-1'), 1, getInitialState(1)));
                    splitInstance = Split(['#pane-0', '#pane-1'], { ...splitOptions, direction: 'vertical', sizes: [50, 50] });
                } else if (layoutType === '3x1v') {
                    chartGridContainer.style.display = 'flex';
                     chartGridContainer.style.flexDirection = 'row';
                    chartGridContainer.innerHTML = '<div id="pane-0" class="chart-pane"></div><div id="pane-1" class="chart-pane"></div><div id="pane-2" class="chart-pane"></div>';
                    for(let i=0; i<3; i++) {
                        chartInstances.push(createChartInstance(document.getElementById(`pane-${i}`), i, getInitialState(i)));
                    }
                    splitInstance = Split(['#pane-0', '#pane-1', '#pane-2'], { ...splitOptions, direction: 'horizontal', sizes: [33.3, 33.3, 33.4] });
                } else if (layoutType === '3x1h') {
                    chartGridContainer.style.display = 'flex';
                    chartGridContainer.style.flexDirection = 'column';
                    chartGridContainer.innerHTML = '<div id="pane-0" class="chart-pane"></div><div id="pane-1" class="chart-pane"></div><div id="pane-2" class="chart-pane"></div>';
                     for(let i=0; i<3; i++) {
                        chartInstances.push(createChartInstance(document.getElementById(`pane-${i}`), i, getInitialState(i)));
                    }
                    splitInstance = Split(['#pane-0', '#pane-1', '#pane-2'], { ...splitOptions, direction: 'vertical', sizes: [33.3, 33.3, 33.4] });
                } else if (layoutType === '2x2') {
                    chartGridContainer.style.display = 'grid';
                    chartGridContainer.style.gridTemplateColumns = '1fr 1fr';
                    chartGridContainer.style.gridTemplateRows = '1fr 1fr';
                    chartGridContainer.innerHTML = `
                        <div id="pane-0" class="chart-pane"></div><div id="pane-1" class="chart-pane"></div>
                        <div id="pane-2" class="chart-pane"></div><div id="pane-3" class="chart-pane"></div>
                    `;
                    for(let i=0; i<4; i++) {
                         chartInstances.push(createChartInstance(document.getElementById(`pane-${i}`), i, getInitialState(i)));
                    }
                }

                setTimeout(() => {
                    chartInstances.forEach(instance => {
                        if (instance.chart) {
                             instance.chart.resize(instance.container.clientWidth, instance.container.clientHeight);
                        }
                    });
                }, 100);

                if (chartInstances.length > 0) {
                    setActiveChart(0);
                }
            }
            
            function setActiveChart(id) {
                activeChartId = id;
                document.querySelectorAll('.chart-pane').forEach(pane => pane.classList.remove('active'));
                const activePane = chartInstances.find(inst => inst.id === id)?.container.parentElement;
                if (activePane) activePane.classList.add('active');
                
                const activeInstance = chartInstances.find(inst => inst.id === activeChartId);
                 if (activeInstance) {
                    const intervalShortLabelMap = { '1m': '1m', '5m': '5m', '15m': '15m', '1h': '1h', '4h': '4h', '1d': '1d' };
                    currentTimeframeLabel.textContent = intervalShortLabelMap[activeInstance.interval] || activeInstance.interval;
                }
            }

            // --- Data Fetching & WebSockets ---
            async function fetchHistoricalData(instance) {
                loadingIndicator.style.display = 'flex';
                removeAllIndicators(instance);
                try {
                    const fiveYearsAgo = new Date();
                    fiveYearsAgo.setFullYear(fiveYearsAgo.getFullYear() - 5);
                    const targetStartTime = fiveYearsAgo.getTime();

                    let allKlines = [];
                    let endTime = null;
                    let limit = 1000;
                    let safetyBreak = 15; 

                    while (safetyBreak > 0) {
                        let url = `https://api.binance.com/api/v3/klines?symbol=${instance.symbol}&interval=${instance.interval}&limit=${limit}`;
                        if (endTime) {
                            url += `&endTime=${endTime}`;
                        }

                        const response = await fetch(url);
                        if (!response.ok) throw new Error(`Network response was not ok for ${instance.symbol}`);
                        
                        const klines = await response.json();
                        if (klines.length === 0) {
                            break; 
                        }

                        allKlines.unshift(...klines);
                        const firstKlineTime = klines[0][0];

                        if (firstKlineTime <= targetStartTime) {
                            break; 
                        }

                        endTime = firstKlineTime - 1;
                        safetyBreak--;
                    }

                    if(allKlines.length === 0){
                         throw new Error("API'den hiç veri alınamadı.");
                    }

                    const formattedData = allKlines.map(d => ({
                        time: d[0] / 1000,
                        open: parseFloat(d[1]),
                        high: parseFloat(d[2]),
                        low: parseFloat(d[3]),
                        close: parseFloat(d[4]),
                    }));
                    
                    instance.historicalData = formattedData;
                    instance.candlestickSeries.setData(formattedData);
                    subscribeToStreams([`${instance.symbol.toLowerCase()}@kline_${instance.interval}`]);

                } catch (error) {
                    console.error('Failed to fetch historical data:', error);
                    instance.container.innerHTML = `<p class="text-red-500 p-4">${instance.symbol} için veri yüklenemedi.</p>`;
                } finally {
                    loadingIndicator.style.display = 'none';
                    if (instance.chart) instance.chart.timeScale().fitContent();
                }
            }

            function connectMainWebSocket() {
                if (mainSocket && mainSocket.readyState < 2) { return; }
                
                const socketUrl = `wss://stream.binance.com:9443/stream`;
                mainSocket = new WebSocket(socketUrl);

                mainSocket.onopen = () => {
                    console.log("Main WebSocket connection opened.");
                    if (activeStreams.size > 0) {
                        mainSocket.send(JSON.stringify({
                            method: "SUBSCRIBE",
                            params: Array.from(activeStreams),
                            id: subscriptionIdCounter++
                        }));
                    }
                };

                mainSocket.onmessage = (event) => {
                    const message = JSON.parse(event.data);
                    if (message.result === null && message.id) { return; }
                    if (!message.stream || !message.data) { return; }

                    const stream = message.stream;
                    const data = message.data;

                    if (stream.endsWith('@ticker')) {
                        updateWatchlistPrice(data.s, parseFloat(data.c));
                    } else if (stream.includes('@kline')) {
                        const symbol = data.s;
                        const interval = data.k.i;
                        const instance = chartInstances.find(inst => inst.symbol === symbol && inst.interval === interval);
                        if (instance) {
                            const candle = data.k;
                            const formattedCandle = {
                                time: candle.t / 1000,
                                open: parseFloat(candle.o),
                                high: parseFloat(candle.h),
                                low: parseFloat(candle.l),
                                close: parseFloat(candle.c),
                            };
                            if (instance.candlestickSeries) instance.candlestickSeries.update(formattedCandle);
                        }
                    }
                };

                mainSocket.onerror = (error) => { console.error("Main WebSocket Error:", error); };
                mainSocket.onclose = () => {
                    console.log("Main WebSocket closed. Reconnecting...");
                    setTimeout(connectMainWebSocket, 5000);
                };
            }

            function subscribeToStreams(streams) {
                connectMainWebSocket();
                const newStreams = streams.filter(s => !activeStreams.has(s));
                if (newStreams.length === 0) return;

                newStreams.forEach(s => activeStreams.add(s));
                if (mainSocket && mainSocket.readyState === WebSocket.OPEN) {
                    mainSocket.send(JSON.stringify({
                        method: "SUBSCRIBE",
                        params: newStreams,
                        id: subscriptionIdCounter++
                    }));
                }
            }

            function unsubscribeFromStreams(streams) {
                const streamsToUnsub = streams.filter(s => activeStreams.has(s));
                if (streamsToUnsub.length === 0) return;
                
                streamsToUnsub.forEach(s => activeStreams.delete(s));

                if (mainSocket && mainSocket.readyState === WebSocket.OPEN) {
                     mainSocket.send(JSON.stringify({
                        method: "UNSUBSCRIBE",
                        params: streamsToUnsub,
                        id: subscriptionIdCounter++
                    }));
                }
            }
            
            // --- Indicator & Scripting Logic ---
            function calculateMA(data, period) {
                let result = [];
                for (let i = period - 1; i < data.length; i++) {
                    let sum = 0;
                    for (let j = 0; j < period; j++) { sum += data[i - j].close; }
                    result.push({ time: data[i].time, value: sum / period });
                }
                return result;
            }

            function applyIndicator(type) {
                const instance = chartInstances.find(inst => inst.id === activeChartId);
                if (!instance) return;

                if (type === 'MA') {
                    if (instance.activeIndicators['MA']) return;
                    const maPeriod = 20;
                    const maData = calculateMA(instance.historicalData, maPeriod);
                    if (maData.length > 0) {
                        const maSeries = instance.chart.addLineSeries({
                            color: 'rgba(255, 165, 0, 0.8)', lineWidth: 2, title: `MA ${maPeriod}`,
                            priceLineVisible: false, lastValueVisible: false,
                        });
                        maSeries.setData(maData);
                        instance.activeIndicators['MA'] = maSeries;
                    }
                } else if (customScripts[type]) {
                     if (instance.activeIndicators[type]) return;
                    executeAndDrawScript(customScripts[type], type);
                }
            }
            
            function executeAndDrawScript(scriptCode, scriptName) {
                const instance = chartInstances.find(inst => inst.id === activeChartId);
                if (!instance) return;

                if (typeof scriptCode !== 'string' || scriptCode.trim().startsWith('#')) {
                    console.error("Invalid script code provided:", scriptCode);
                    alert("Geçersiz komut dosyası. Lütfen geçerli bir JavaScript kodu girin.");
                    return;
                }

                try {
                    const scriptFunction = new Function('data', scriptCode);
                    const indicatorData = scriptFunction(instance.historicalData);

                    if (!Array.isArray(indicatorData) || (indicatorData.length > 0 && (indicatorData[0].time === undefined || indicatorData[0].value === undefined))) {
                         throw new Error("Komut dosyası geçerli bir {time, value} dizisi döndürmedi.");
                    }

                    const scriptSeries = instance.chart.addLineSeries({
                        color: 'rgba(255, 165, 0, 0.8)',
                        lineWidth: 2,
                        title: scriptName,
                        priceLineVisible: false,
                        lastValueVisible: false,
                    });
                    scriptSeries.setData(indicatorData);
                    instance.activeIndicators[scriptName] = scriptSeries;

                } catch (error) {
                    console.error("Özel Komut Dosyası Hatası:", error);
                    alert(`Komut dosyasında hata: ${error.message}`);
                }
            }

            function removeAllIndicators(instance) {
                if (!instance) return;
                for (const key in instance.activeIndicators) {
                    instance.chart.removeSeries(instance.activeIndicators[key]);
                }
                instance.activeIndicators = {};
            }
            
            // --- Replay Mode Logic ---
            function toggleReplayMode() {
                isReplayModeActive = !isReplayModeActive;
                const activeInstance = chartInstances.find(inst => inst.id === activeChartId);
                if (!activeInstance) {
                     isReplayModeActive = false;
                     return;
                }

                if (isReplayModeActive) {
                    setActiveDrawingTool('cursor');
                    replayState.instance = activeInstance;
                    replayState.fullData = [...activeInstance.historicalData];
                    replayBtnText.textContent = "Kesmek için Tıkla";
                    replayBtn.classList.add('bg-blue-600', 'text-white');
                    activeInstance.container.parentElement.classList.add('replay-active');
                    document.querySelectorAll('#layout-toggle, #indicators-toggle, #timeframe-toggle, #settings-toggle, #drawing-toolbar button').forEach(el => el.disabled = true);
                } else {
                    exitReplayMode();
                }
            }
            
            function handleReplayCut(time) {
                if (!isReplayModeActive || !replayState.instance || replayState.futureData.length > 0) return;
                
                const cutIndex = replayState.fullData.findIndex(d => d.time >= time);
                if (cutIndex <= 1) return; 

                const pastData = replayState.fullData.slice(0, cutIndex);
                replayState.futureData = replayState.fullData.slice(cutIndex);
                replayState.currentIndex = 0;
                
                replayState.instance.candlestickSeries.setData(pastData);
                
                const lastVisibleCandle = pastData[pastData.length - 1];
                if (lastVisibleCandle) {
                    const marker = {
                        time: lastVisibleCandle.time,
                        position: 'aboveBar',
                        color: '#3b82f6',
                        shape: 'arrowDown',
                        text: 'Başlangıç'
                    };
                    replayState.instance.candlestickSeries.setMarkers([marker]);
                }
                
                unsubscribeFromStreams([`${replayState.instance.symbol.toLowerCase()}@kline_${replayState.instance.interval}`]);


                replayState.instance.container.parentElement.classList.remove('replay-active');
                replayControls.classList.remove('hidden');
                replayBtnText.textContent = "Tekrar Modu Aktif";
            }

            function stepReplayForward() {
                if (replayState.currentIndex >= replayState.futureData.length) {
                    pauseReplay(); 
                    return;
                }
                const nextCandle = replayState.futureData[replayState.currentIndex];
                replayState.instance.candlestickSeries.update(nextCandle);
                replayState.currentIndex++;
            }

            function playReplay() {
                if (replayState.isPlaying) return;
                replayState.isPlaying = true;
                playIcon.classList.add('hidden');
                pauseIcon.classList.remove('hidden');
                replayState.timer = setInterval(stepReplayForward, replayState.speed);
            }

            function pauseReplay() {
                if (!replayState.isPlaying) return;
                replayState.isPlaying = false;
                pauseIcon.classList.add('hidden');
                playIcon.classList.remove('hidden');
                clearInterval(replayState.timer);
                replayState.timer = null;
            }

            function exitReplayMode() {
                if(replayState.timer) clearInterval(replayState.timer);

                if (replayState.instance) {
                    replayState.instance.candlestickSeries.setData(replayState.fullData);
                    replayState.instance.candlestickSeries.setMarkers([]);
                    subscribeToStreams([`${replayState.instance.symbol.toLowerCase()}@kline_${replayState.instance.interval}`]);
                    replayState.instance.container.parentElement.classList.remove('replay-active');
                }
                
                isReplayModeActive = false;
                replayState = { instance: null, fullData: [], futureData: [], currentIndex: 0, isPlaying: false, timer: null, speed: 1000 };
                
                replayControls.classList.add('hidden');
                replayBtnText.textContent = "Tekrar";
                replayBtn.classList.remove('bg-blue-600', 'text-white');
                pauseIcon.classList.add('hidden');
                playIcon.classList.remove('hidden');

                document.querySelectorAll('#layout-toggle, #indicators-toggle, #timeframe-toggle, #settings-toggle, #drawing-toolbar button').forEach(el => el.disabled = false);
            }
            
             // --- Drawing Logic ---

            function setActiveDrawingTool(tool) {
                if (isReplayModeActive) return;

                activeDrawingTool = tool;
                document.querySelectorAll('.drawing-tool-btn').forEach(btn => {
                    btn.classList.toggle('active', btn.dataset.tool === tool);
                });
                 document.querySelectorAll('.chart-pane').forEach(pane => {
                    pane.classList.toggle('drawing-cursor', tool !== 'cursor');
                });

                isDrawing = false;
                drawingStartPoint = null;
            }

            function handleDrawing(param, instance) {
                if (!param.point || !param.time) return;

                const price = instance.candlestickSeries.coordinateToPrice(param.point.y);
                if (!price) return;
                
                if (!isDrawing) {
                    isDrawing = true;
                    drawingStartPoint = { time: param.time, price: price };
                } else {
                    const endPoint = { time: param.time, price: price };

                    if (activeDrawingTool === 'trendline') {
                        const line = instance.chart.addLineSeries({ color: '#2563eb', lineWidth: 2, priceLineVisible: false, lastValueVisible: false, crosshairMarkerVisible: false });
                        line.setData([
                            { time: drawingStartPoint.time, value: drawingStartPoint.price },
                            { time: endPoint.time, value: endPoint.price }
                        ]);
                        instance.drawings.push({ type: 'series', obj: line });
                    }
                    else if (activeDrawingTool === 'fib') {
                        drawFibRetracement(instance, drawingStartPoint, endPoint);
                    }
                    else if (activeDrawingTool === 'rectangle') {
                        drawRectangle(instance, drawingStartPoint, endPoint);
                    }
                    
                    isDrawing = false;
                    drawingStartPoint = null;
                    setActiveDrawingTool('cursor');
                }
            }
            
            function drawRectangle(instance, start, end) {
                const commonOptions = { 
                    color: 'rgba(59, 130, 246, 0.7)', 
                    lineWidth: 1, 
                    priceLineVisible: false, 
                    lastValueVisible: false, 
                    crosshairMarkerVisible: false 
                };

                const time1 = Math.min(start.time, end.time);
                const time2 = Math.max(start.time, end.time);
                const price1 = start.price;
                const price2 = end.price;

                const topLine = instance.chart.addLineSeries(commonOptions);
                const bottomLine = instance.chart.addLineSeries(commonOptions);
                const leftLine = instance.chart.addLineSeries(commonOptions);
                const rightLine = instance.chart.addLineSeries(commonOptions);

                topLine.setData([{ time: time1, value: price1 }, { time: time2, value: price1 }]);
                bottomLine.setData([{ time: time1, value: price2 }, { time: time2, value: price2 }]);
                leftLine.setData([{ time: time1, value: price1 }, { time: time1, value: price2 }]);
                rightLine.setData([{ time: time2, value: price1 }, { time: time2, value: price2 }]);
                
                instance.drawings.push({ type: 'series', obj: topLine });
                instance.drawings.push({ type: 'series', obj: bottomLine });
                instance.drawings.push({ type: 'series', obj: leftLine });
                instance.drawings.push({ type: 'series', obj: rightLine });
            }

            function drawFibRetracement(instance, start, end) {
                const levels = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1];
                const priceDiff = end.price - start.price;

                levels.forEach(level => {
                    const price = start.price + priceDiff * level;
                    const color = level === 0.5 ? 'rgba(255, 165, 0, 0.7)' : 'rgba(59, 130, 246, 0.7)';
                    const priceLine = instance.chart.createPriceLine({
                        price: price,
                        color: color,
                        lineWidth: 1,
                        lineStyle: LightweightCharts.LineStyle.Dashed,
                        axisLabelVisible: true,
                        title: level.toFixed(3),
                    });
                    instance.drawings.push({ type: 'priceLine', obj: priceLine });
                });
            }
             
            function clearAllDrawings() {
                const instance = chartInstances.find(inst => inst.id === activeChartId);
                if (!instance) return;

                instance.drawings.forEach(drawing => {
                    if (drawing.type === 'series') {
                        instance.chart.removeSeries(drawing.obj);
                    } else if (drawing.type === 'priceLine') {
                        instance.chart.removePriceLine(drawing.obj);
                    }
                });
                instance.drawings = [];
            }


            // --- UI Updates ---
            function renderIndicatorsMenu() {
                indicatorsMenu.innerHTML = '';
                
                const builtInHeader = document.createElement('div');
                builtInHeader.className = 'px-4 py-2 text-xs font-bold text-gray-400 uppercase';
                builtInHeader.textContent = 'Yerleşik';
                indicatorsMenu.appendChild(builtInHeader);

                const maItem = document.createElement('a');
                maItem.href = '#';
                maItem.dataset.indicator = 'MA';
                maItem.className = 'indicator-item block px-4 py-2 text-sm text-white hover:bg-blue-600';
                maItem.textContent = 'Moving Average (MA)';
                indicatorsMenu.appendChild(maItem);
                
                if (Object.keys(customScripts).length > 0) {
                    const customHeader = document.createElement('div');
                    customHeader.className = 'px-4 py-2 text-xs font-bold text-gray-400 uppercase border-t border-gray-600 mt-1 pt-2';
                    customHeader.textContent = 'Özel Komut Dosyalarım';
                    indicatorsMenu.appendChild(customHeader);

                    for (const name in customScripts) {
                         const scriptItem = document.createElement('a');
                        scriptItem.href = '#';
                        scriptItem.dataset.indicator = name;
                        scriptItem.className = 'indicator-item block px-4 py-2 text-sm text-white hover:bg-blue-600';
                        scriptItem.textContent = name;
                        indicatorsMenu.appendChild(scriptItem);
                    }
                }
            }


            function renderWatchlist() {
                coinList.innerHTML = '';
                watchlistSymbols.forEach(symbol => {
                    const li = createCoinListItem(symbol);
                    coinList.appendChild(li);
                });
            }

            function createCoinListItem(symbol) {
                const li = document.createElement('li');
                li.className = "coin-item flex justify-between items-center p-3 hover:bg-gray-700 border-b border-gray-700/50 transition-colors";
                li.dataset.symbol = symbol;

                const infoDiv = document.createElement('div');
                infoDiv.className = 'flex-grow flex justify-between items-center cursor-pointer mr-2';
                infoDiv.innerHTML = `
                    <span class="font-medium">${symbol.replace('USDT', '/USDT')}</span>
                    <span id="price-${symbol}" class="font-mono text-sm text-gray-400">...</span>
                `;

                const removeBtn = document.createElement('button');
                removeBtn.className = 'remove-coin-btn p-1 text-gray-500 hover:text-red-500 rounded-md transition-colors flex-shrink-0';
                removeBtn.title = `${symbol} Kaldır`;
                removeBtn.innerHTML = `
                    <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                    </svg>
                `;

                li.appendChild(infoDiv);
                li.appendChild(removeBtn);
                return li;
            }

            function updateWatchlistPrice(symbol, price) {
                const priceElement = document.getElementById(`price-${symbol}`);
                if (!priceElement) return;
                const lastPrice = lastPrices[symbol] || 0;
                const priceString = price.toFixed(price > 10 ? 2 : 4);
                priceElement.textContent = priceString;
                if (price > lastPrice) {
                    priceElement.className = "font-mono text-sm text-green-400";
                } else if (price < lastPrice) {
                    priceElement.className = "font-mono text-sm text-red-400";
                }
                lastPrices[symbol] = price;
            }
            
            // --- Event Handlers ---
            async function handleGenerateScript() {
                const userPrompt = scriptPromptInput.value;
                if (!userPrompt) {
                    alert("Lütfen oluşturmak istediğiniz göstergeyi açıklayın.");
                    return;
                }

                generateScriptBtn.disabled = true;
                generateBtnText.textContent = "Oluşturuluyor...";
                generateSpinner.classList.remove('hidden');

                const systemInstruction = "Sen finansal grafik göstergeleri için JavaScript kodu yazan uzman bir programcısın. Kullanıcının doğal dildeki isteğini, belirli bir ortamda çalışacak bir JavaScript koduna dönüştürmelisin. Kod, 'data' adında tek bir argüman alan bir fonksiyonun gövdesi olmalı. 'data' argümanı, {time, open, high, low, close} formatında nesneler içeren bir dizidir. Kod, grafiğe çizilmek üzere {time, value} formatında nesneler içeren bir dizi döndürmelidir. Yalnızca fonksiyon gövdesini içeren saf JavaScript kodunu, herhangi bir açıklama veya markdown olmadan döndür.";
                
                try {
                    let generatedCode = await callGeminiAPI(userPrompt, systemInstruction);
                    generatedCode = generatedCode.replace(/```javascript/g, '').replace(/```/g, '').trim();
                    pineEditor.value = generatedCode;
                } catch (error) {
                    alert("Kod oluşturulurken bir hata oluştu. Lütfen tekrar deneyin.");
                } finally {
                    generateScriptBtn.disabled = false;
                    generateBtnText.textContent = "Kod Oluştur ✨";
                    generateSpinner.classList.add('hidden');
                }
            }

            function handleTimeframeChange(newInterval) {
                 if (isReplayModeActive) return;
                const instance = chartInstances.find(inst => inst.id === activeChartId);
                if (!instance || newInterval === instance.interval) return;
                
                unsubscribeFromStreams([`${instance.symbol.toLowerCase()}@kline_${instance.interval}`]);
                instance.interval = newInterval;
                fetchHistoricalData(instance);
                setActiveChart(activeChartId);
            }

            function handleSymbolChange(newSymbol) {
                 if (isReplayModeActive) return;
                const instance = chartInstances.find(inst => inst.id === activeChartId);
                if (!instance || newSymbol === instance.symbol) return;
                
                unsubscribeFromStreams([`${instance.symbol.toLowerCase()}@kline_${instance.interval}`]);
                instance.symbol = newSymbol;
                fetchHistoricalData(instance);
                closeSidebar();
            }

            function handleAddNewCoin() {
                const newSymbol = newCoinInput.value.trim().toUpperCase();
                if (newSymbol && !watchlistSymbols.includes(newSymbol)) {
                    watchlistSymbols.push(newSymbol);
                    coinList.appendChild(createCoinListItem(newSymbol));
                    subscribeToStreams([`${newSymbol.toLowerCase()}@ticker`]);
                }
                newCoinInput.value = '';
                closeAddCoinModal();
            }

            function handleSaveScript() {
                const scriptName = prompt("Komut dosyası için bir ad girin:", "Benim Göstergem");
                if (scriptName && scriptName.trim() !== "") {
                    customScripts[scriptName.trim()] = pineEditor.value;
                    renderIndicatorsMenu();
                    alert(`"${scriptName.trim()}" kaydedildi!`);
                }
            }
            
            function handleRemoveCoin(symbolToRemove) {
                const index = watchlistSymbols.indexOf(symbolToRemove);
                if (index > -1) {
                    watchlistSymbols.splice(index, 1);
                }

                const itemToRemove = coinList.querySelector(`li[data-symbol="${symbolToRemove}"]`);
                if (itemToRemove) {
                    itemToRemove.remove();
                }

                unsubscribeFromStreams([`${symbolToRemove.toLowerCase()}@ticker`]);
            }

            // --- Modal & Sidebar & Dropdown Logic ---
            function openSidebar() { sidebar.classList.remove('translate-x-full'); sidebarOverlay.classList.remove('hidden'); }
            function closeSidebar() { sidebar.classList.add('translate-x-full'); sidebarOverlay.classList.add('hidden'); }
            function openAddCoinModal() { addCoinModal.classList.remove('hidden'); addCoinModal.classList.add('flex'); }
            function closeAddCoinModal() { addCoinModal.classList.add('hidden'); addCoinModal.classList.remove('flex');}

            // --- Event Listeners Setup---
            layoutToggle.addEventListener('click', () => layoutMenu.classList.toggle('hidden'));
            layoutMenu.addEventListener('click', (e) => {
                const item = e.target.closest('.layout-item');
                if (item) {
                     if (isReplayModeActive) return;
                    applyLayout(item.dataset.layout);
                    layoutMenu.classList.add('hidden');
                }
            });

            timeframeToggle.addEventListener('click', () => timeframeMenu.classList.toggle('hidden'));
            timeframeMenu.addEventListener('click', (e) => {
                e.preventDefault();
                if (e.target.matches('.timeframe-item')) {
                    handleTimeframeChange(e.target.dataset.interval);
                    timeframeMenu.classList.add('hidden');
                }
            });
            
            indicatorsToggle.addEventListener('click', () => indicatorsMenu.classList.toggle('hidden'));
            indicatorsMenu.addEventListener('click', (e) => {
                e.preventDefault();
                const item = e.target.closest('.indicator-item');
                if (item) {
                    applyIndicator(item.dataset.indicator);
                    indicatorsMenu.classList.add('hidden');
                }
            });

            settingsToggle.addEventListener('click', () => settingsMenu.classList.toggle('hidden'));
            backgroundColorPicker.addEventListener('input', (e) => {
                const newColor = e.target.value;
                currentBackgroundColor = newColor; 
                chartInstances.forEach(instance => {
                    if (instance.chart) {
                        instance.chart.applyOptions({ 
                            layout: { 
                                backgroundColor: newColor,
                                textColor: 'rgba(229, 231, 235, 1)'
                            }
                        });
                    }
                });
            });

            saveColorBtn.addEventListener('click', () => {
                localStorage.setItem('chartBackgroundColor', currentBackgroundColor);
                const icon = saveColorBtn.querySelector('svg');
                icon.classList.add('text-green-400');
                setTimeout(() => {
                    icon.classList.remove('text-green-400');
                }, 1500);
            });
            
            generateScriptBtn.addEventListener('click', handleGenerateScript);


            window.addEventListener('click', (e) => { // Hide dropdowns on outside click
                if (!timeframeDropdown.contains(e.target)) timeframeMenu.classList.add('hidden');
                if (!indicatorsDropdown.contains(e.target)) indicatorsMenu.classList.add('hidden');
                if (!layoutDropdown.contains(e.target)) layoutMenu.classList.add('hidden');
                if (!settingsDropdown.contains(e.target)) settingsMenu.classList.add('hidden');
            });

            chartTab.addEventListener('click', () => {
                pineTab.classList.remove('active');
                chartTab.classList.add('active');
                pinePanel.classList.add('hidden');
                pinePanel.classList.remove('flex'); 
                chartPanel.classList.remove('hidden');
                 setTimeout(() => chartInstances.forEach(instance => {
                     if (instance.chart) instance.chart.resize(instance.container.clientWidth, instance.container.clientHeight)
                 }), 50);
            });
            pineTab.addEventListener('click', () => {
                chartTab.classList.remove('active');
                pineTab.classList.add('active');
                chartPanel.classList.add('hidden');
                pinePanel.classList.remove('hidden');
                pinePanel.classList.add('flex');
            });

            applyScriptBtn.addEventListener('click', () => executeAndDrawScript(pineEditor.value, 'Özel Script'));
            saveScriptBtn.addEventListener('click', handleSaveScript);

            sidebarToggle.addEventListener('click', openSidebar);
            sidebarClose.addEventListener('click', closeSidebar);
            sidebarOverlay.addEventListener('click', closeSidebar);

            coinList.addEventListener('click', (e) => {
                const removeBtn = e.target.closest('.remove-coin-btn');
                if (removeBtn) {
                    const symbol = removeBtn.parentElement.dataset.symbol;
                    handleRemoveCoin(symbol);
                    return; 
                }

                const coinItem = e.target.closest('.coin-item > div');
                if (coinItem) {
                    const symbol = coinItem.parentElement.dataset.symbol;
                    handleSymbolChange(symbol);
                }
            });
            
            replayBtn.addEventListener('click', toggleReplayMode);
            replayPlayPauseBtn.addEventListener('click', () => {
                if(replayState.isPlaying) pauseReplay();
                else playReplay();
            });
            replayForwardBtn.addEventListener('click', stepReplayForward);
            replaySpeedSelect.addEventListener('change', (e) => {
                replayState.speed = parseInt(e.target.value);
                if (replayState.isPlaying) { // Restart timer with new speed
                    pauseReplay();
                    playReplay();
                }
            });
            replayExitBtn.addEventListener('click', exitReplayMode);
            
            drawingToolbar.addEventListener('click', (e) => {
                const btn = e.target.closest('.drawing-tool-btn');
                if (!btn) return;
                const tool = btn.dataset.tool;
                if (tool === 'clear') {
                    clearAllDrawings();
                } else {
                    setActiveDrawingTool(tool);
                }
            });

            drawingToolbarToggle.addEventListener('click', () => {
                drawingToolbar.classList.toggle('hidden');
                const icon = drawingToolbarToggle.querySelector('svg');
                if (drawingToolbar.classList.contains('hidden')) {
                    icon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />';
                } else {
                    icon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />';
                }
            });
            
            addCoinBtn.addEventListener('click', openAddCoinModal);
            modalCancelBtn.addEventListener('click', closeAddCoinModal);
            modalAddBtn.addEventListener('click', handleAddNewCoin);
            newCoinInput.addEventListener('keyup', (e) => { if(e.key === 'Enter') handleAddNewCoin(); });

            window.addEventListener('resize', () => {
                chartInstances.forEach(instance => {
                     if(instance && instance.chart && instance.container) {
                         instance.chart.resize(instance.container.clientWidth, instance.container.clientHeight);
                     }
                });
            });

            // --- Initial Load ---
            const savedColor = localStorage.getItem('chartBackgroundColor');
            if (savedColor) {
                currentBackgroundColor = savedColor;
                backgroundColorPicker.value = savedColor;
            }

            applyLayout('1x1'); 
            renderWatchlist();
            renderIndicatorsMenu();
            subscribeToStreams(watchlistSymbols.map(s => `${s.toLowerCase()}@ticker`));
        });
    </script>
</body>
</html>


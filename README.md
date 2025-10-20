<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Teknik Analiz Platformu - Canlı Veri</title>
    <!-- Tailwind CSS --><script src="https://cdn.tailwindcss.com"></script>
    <!-- Lightweight Charts by TradingView --><script src="https://cdn.jsdelivr.net/npm/lightweight-charts@3.8.0/dist/lightweight-charts.standalone.production.js"></script>
    <style>
        html, body {
            width: 100%;
            height: 100%;
            margin: 0;
            padding: 0;
            overflow: hidden;
            font-family: 'Inter', sans-serif;
            background-color: #111827; /* bg-gray-900 */
        }
        #app {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            display: flex;
            flex-direction: column;
        }
        .btn-active {
            background-color: #3b82f6; /* blue-500 */
            color: white;
        }
        /* Dropdown için stiller */
        .dropdown-content {
            display: none;
            position: absolute;
            background-color: #1f2937; /* bg-gray-800 */
            min-width: 120px; /* Genişliği daralttık */
            box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
            z-index: 20; /* Diğer elementlerin üzerinde kalması için */
            border-radius: 0.375rem; /* rounded-md */
            border: 1px solid #374151; /* border-gray-700 */
            padding: 0.25rem; /* p-1 */
        }
        .dropdown-content a, .dropdown-content button {
            color: #d1d5db; /* text-gray-300 */
            padding: 8px 12px;
            text-decoration: none;
            display: block;
            width: 100%;
            text-align: left;
        }
        .dropdown-content a:hover, .dropdown-content button:hover {
            background-color: #374151; /* bg-gray-700 */
        }
        /* Menüyü göstermek için JS tarafından eklenecek class */
        .dropdown-content.show {
            display: block;
        }
        /* Modal için stiller */
        #add-coin-modal-list::-webkit-scrollbar { width: 8px; }
        #add-coin-modal-list::-webkit-scrollbar-track { background: #2d3748; }
        #add-coin-modal-list::-webkit-scrollbar-thumb { background: #4a5568; border-radius: 4px; }
        #add-coin-modal-list::-webkit-scrollbar-thumb:hover { background: #718096; }
    </style>
</head>
<body class="bg-gray-900 text-gray-200">

    <div id="app">
        <!-- Header --><header class="bg-gray-800 border-b border-gray-700 px-4 h-12 flex justify-between items-center shadow-lg relative z-10 shrink-0">
            <!-- Left: Symbol Name, Coins & Timeframe Dropdowns --><div class="flex items-center space-x-4">
                <h1 id="header-symbol" class="text-lg font-bold text-white">BTC/USDT</h1>
                <!-- Coinler Dropdown --><div class="dropdown relative hidden lg:inline-block">
                    <button id="coins-dropdown-btn" class="flex items-center space-x-2 px-2 py-1 text-sm rounded-md hover:bg-gray-700">
                        <span>Coinler</span>
                    </button>
                    <div id="coin-list" class="dropdown-content mt-2">
                        <!-- Coin listesi dinamik olarak buraya eklenecek -->
                    </div>
                </div>
                 <!-- Saat Dropdown --><div class="dropdown relative hidden lg:inline-block">
                    <button id="timeframe-dropdown-btn" class="flex items-center px-2 py-1 text-sm rounded-md hover:bg-gray-700">
                        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
                        <span id="selected-timeframe-display" class="text-sm text-gray-400 ml-1"></span>
                    </button>
                    <div id="timeframe-list-header" class="dropdown-content mt-2 p-1">
                        <!-- Zaman dilimleri dinamik olarak buraya eklenecek -->
                    </div>
                </div>
            </div>

            <!-- Center: Empty --><div id="header-menu" class="absolute left-1/2 -translate-x-1/2 hidden lg:flex items-center">
                <!-- Burası artık boş --></div>

            <!-- Right: Mobile Menu Button (Sadece küçük ekranlarda görünür) --><div class="lg:hidden">
                 <button id="mobile-menu-btn" class="text-gray-300 hover:text-white focus:outline-none">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7"></path></svg>
                </button>
            </div>
        </header>

        <div class="flex-1 min-h-0">
            <!-- Main Content (Chart) --><main class="w-full h-full">
                <div id="chart-container" class="w-full h-full">
                    <!-- Yükleniyor göstergesi kaldırıldı -->
                </div>
            </main>
        </div>
    </div>
    
    <!-- Mobile Menu (Başlangıçta gizli) --><div id="mobile-menu" class="hidden fixed inset-0 bg-gray-900 bg-opacity-95 z-50 p-6 text-lg">
        <div class="flex justify-end mb-8">
            <button id="mobile-menu-close-btn" class="text-gray-300 hover:text-white text-4xl">&times;</button>
        </div>
        
        <div class="flex flex-col space-y-8">
            <div>
                <h3 class="text-gray-400 text-sm font-bold mb-4">Zaman Aralığı</h3>
                <div id="timeframe-list-mobile" class="flex flex-col items-start space-y-4">
                    <!-- Mobil zaman aralıkları buraya dinamik olarak eklenecek --></div>
            </div>

            <div>
                 <h3 class="text-gray-400 text-sm font-bold mt-6 mb-4">Coinler</h3>
                 <div id="coin-list-mobile" class="flex flex-col items-start space-y-4 w-full">
                    <!-- Mobil coin listesi buraya dinamik olarak eklenecek --></div>
            </div>
        </div>
    </div>

    <!-- Add Coin Modal --><div id="add-coin-modal" class="hidden fixed inset-0 bg-black bg-opacity-70 z-50 flex items-center justify-center">
        <div class="bg-gray-800 rounded-lg shadow-xl w-full max-w-md flex flex-col">
            <div class="p-4 border-b border-gray-700 flex justify-between items-center">
                <h3 class="text-lg font-semibold text-white">Coin Ekle</h3>
                <button id="modal-close-btn" class="text-gray-400 hover:text-white">&times;</button>
            </div>
            <div class="p-4">
                <input id="modal-search-input" type="text" placeholder="Coin ara (örn: BTC)" class="w-full bg-gray-900 border border-gray-700 text-white rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
            </div>
            <div id="add-coin-modal-list" class="overflow-y-auto h-80 p-4">
                <!-- Binance coin listesi buraya gelecek -->
            </div>
        </div>
    </div>


    <script>
        function initializeApp() {
            const chartContainer = document.getElementById('chart-container');
            const headerSymbol = document.getElementById('header-symbol');
            const selectedTimeframeDisplay = document.getElementById('selected-timeframe-display');
            
            let currentSymbol = 'BTCUSDT';
            let currentTimeframe = '1d';
            let websocket;
            let candleSeries;
            const dataCache = {};
            const pendingFetches = {};

            let coins = [];
            const DEFAULT_COINS = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT'];
            let allBinanceSymbols = [];

            const TIMEFRAMES = [
                { interval: '5m', label: '5 dk' }, { interval: '15m', label: '15 dk' },
                { interval: '30m', label: '30 dk' }, { interval: '1h', label: '1 Saat' },
                { interval: '4h', label: '4 Saat' }, { interval: '1d', label: '1 Gün' },
                { interval: '1M', label: '1 Ay' },
            ];

            // --- DATA & STATE MANAGEMENT ---
            function loadCoins() { /* ... unchanged ... */ const storedCoins = localStorage.getItem('tradingAppCoins'); if (storedCoins) { coins = JSON.parse(storedCoins); } else { coins = [...DEFAULT_COINS]; } }
            function saveCoins() { /* ... unchanged ... */ localStorage.setItem('tradingAppCoins', JSON.stringify(coins)); }
            async function fetchBinanceSymbols() { /* ... unchanged ... */ try { const response = await fetch('https://api.binance.com/api/v3/exchangeInfo'); const data = await response.json(); allBinanceSymbols = data.symbols .filter(s => s.quoteAsset === 'USDT' && s.status === 'TRADING') .map(s => s.symbol); } catch (error) { console.error("Binance sembolleri alınamadı:", error); } }

            // --- UI RENDERING ---
            function renderTimeframeButtons() { /* ... unchanged ... */ const desktopList = document.getElementById('timeframe-list-header'); const mobileList = document.getElementById('timeframe-list-mobile'); desktopList.innerHTML = ''; mobileList.innerHTML = ''; TIMEFRAMES.forEach(tf => { const desktopBtn = document.createElement('button'); desktopBtn.className = 'timeframe-btn rounded-md transition-colors duration-200'; desktopBtn.dataset.interval = tf.interval; desktopBtn.textContent = tf.label; desktopBtn.addEventListener('click', () => { selectTimeframe(tf.interval); document.getElementById('timeframe-list-header').classList.remove('show'); }); desktopList.appendChild(desktopBtn); const mobileBtn = document.createElement('button'); mobileBtn.className = 'timeframe-btn-mobile text-lg'; mobileBtn.dataset.interval = tf.interval; mobileBtn.textContent = tf.label; mobileBtn.addEventListener('click', () => { selectTimeframe(tf.interval); document.getElementById('mobile-menu').classList.add('hidden'); }); mobileList.appendChild(mobileBtn); }); }
            function renderDesktopCoinList() { /* ... unchanged ... */ const list = document.getElementById('coin-list'); list.innerHTML = ''; coins.forEach(symbol => { list.innerHTML += ` <a href="#" class="coin-item flex justify-between items-center group rounded-md" data-symbol="${symbol}"> <span class="flex items-center px-3 py-2 text-sm"> ${symbol.replace('USDT','/USDT')} <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="delete-coin-btn hidden group-hover:block text-gray-500 hover:text-red-400 ml-2" data-symbol="${symbol}"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg> </span> </a> `; }); list.innerHTML += ` <div class="border-t border-gray-600 my-1 mx-2"></div> <a href="#" id="add-coin-btn" class="flex items-center space-x-2 text-green-400 rounded-md hover:bg-gray-700"> <span class="flex items-center p-2"> <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-2"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg> <span>Ekle</span> </span> </a> `; }
            function renderMobileCoinList() { /* ... unchanged ... */ const list = document.getElementById('coin-list-mobile'); list.innerHTML = ''; coins.forEach(symbol => { list.innerHTML += ` <a href="#" class="coin-item-mobile flex justify-between items-center w-full" data-symbol="${symbol}"> <span class="flex items-center text-sm"> ${symbol.replace('USDT','/USDT')} </span> <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="delete-coin-btn text-gray-500 hover:text-red-400" data-symbol="${symbol}"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg> </a> `; }); list.innerHTML += ` <a href="#" id="add-coin-btn-mobile" class="flex items-center space-x-2 mt-4 text-green-400"> <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg> <span>Ekle</span> </a> `; }

            // --- CHART & API LOGIC ---
            const chart = LightweightCharts.createChart(chartContainer, { /* ... unchanged ... */ width: chartContainer.clientWidth, height: chartContainer.clientHeight, layout: { backgroundColor: '#ffffff', textColor: 'rgba(0, 0, 0, 0.9)' }, grid: { vertLines: { visible: false }, horzLines: { visible: false } }, crosshair: { mode: LightweightCharts.CrosshairMode.Normal }, rightPriceScale: { borderColor: '#D1D5DB' }, timeScale: { borderColor: '#D1D5DB', timeVisible: true, secondsVisible: false } });
            candleSeries = chart.addCandlestickSeries({ /* ... unchanged ... */ upColor: '#22c55e', downColor: '#ef4444', borderDownColor: '#ef4444', borderUpColor: '#22c55e', wickDownColor: '#ef4444', wickUpColor: '#22c55e', priceLineVisible: false, });
            
            async function fetchAndCacheData(symbol, interval) {
                const cacheKey = `${symbol}_${interval}`;
                if (dataCache[cacheKey]) return dataCache[cacheKey];
                if (pendingFetches[cacheKey]) return await pendingFetches[cacheKey];

                const fetchPromise = (async () => {
                    try {
                        const now = new Date();
                        let startTime = 0;
                        switch (interval) {
                            case '5m': startTime = new Date(now.setDate(now.getDate() - 7)).getTime(); break;
                            case '15m': startTime = new Date(now.setDate(now.getDate() - 14)).getTime(); break;
                            case '30m': startTime = new Date(now.setDate(now.getDate() - 30)).getTime(); break;
                            case '1h': startTime = new Date(now.setDate(now.getDate() - 90)).getTime(); break;
                            case '4h': startTime = new Date(now.setFullYear(now.getFullYear() - 1)).getTime(); break;
                            default: startTime = 0; // 1d ve 1M için limit yok
                        }

                        let allKlines = [], endTime = Date.now(), limit = 1000;

                        while (true) {
                            const url = `https://api.binance.com/api/v3/klines?symbol=${symbol}&interval=${interval}&limit=${limit}&endTime=${endTime}`;
                            const response = await fetch(url);
                            if (!response.ok) throw new Error(`Binance API error: ${response.status}`);
                            const klines = await response.json();
                            if (klines.length === 0) break;
                            allKlines = klines.concat(allKlines);
                            const firstKlineTimestamp = klines[0][0];

                            if (startTime > 0 && firstKlineTimestamp < startTime) {
                                break;
                            }
                            
                            endTime = firstKlineTimestamp - 1;
                            await new Promise(resolve => setTimeout(resolve, 100));
                        }
                        
                        const finalKlines = startTime > 0 ? allKlines.filter(k => k[0] >= startTime) : allKlines;
                        const formattedData = finalKlines.map(item => ({ time: item[0] / 1000, open: parseFloat(item[1]), high: parseFloat(item[2]), low: parseFloat(item[3]), close: parseFloat(item[4]), }));
                        
                        if (formattedData.length > 0) dataCache[cacheKey] = formattedData;
                        return formattedData;
                    } catch (error) {
                        console.error(`Veri çekme hatası for ${cacheKey}:`, error);
                        return [];
                    } finally {
                        delete pendingFetches[cacheKey];
                    }
                })();
                
                pendingFetches[cacheKey] = fetchPromise;
                return await fetchPromise;
            }

            async function getHistoricalData(symbol, interval) { /* ... unchanged ... */ const dataFromCache = dataCache[`${symbol}_${interval}`]; if (dataFromCache) { candleSeries.setData(dataFromCache); return dataFromCache; } const data = await fetchAndCacheData(symbol, interval); candleSeries.setData(data); return data; }
            function preFetchDataForSymbol(symbol) { const timeframes = TIMEFRAMES.map(tf => tf.interval); timeframes.forEach(tf => { fetchAndCacheData(symbol, tf); }); }
            function subscribeToStream(symbol, interval) { /* ... unchanged ... */ if (websocket) { websocket.onopen = null; websocket.onmessage = null; websocket.onerror = null; websocket.onclose = null; if (websocket.readyState === WebSocket.OPEN || websocket.readyState === WebSocket.CONNECTING) { websocket.close(); } } const wsUrl = `wss://stream.binance.com/ws/${symbol.toLowerCase()}@kline_${interval}`; websocket = new WebSocket(wsUrl); websocket.onopen = () => { console.log(`WebSocket bağlantısı başarılı: ${symbol}`); }; websocket.onmessage = (event) => { const message = JSON.parse(event.data); const kline = message.k; candleSeries.update({ time: kline.t / 1000, open: parseFloat(kline.o), high: parseFloat(kline.h), low: parseFloat(kline.l), close: parseFloat(kline.c), }); }; websocket.onerror = (error) => { console.error(`WebSocket Hatası for ${symbol}:`, error); }; websocket.onclose = (event) => { if (!event.wasClean) { console.warn(`WebSocket bağlantısı beklenmedik şekilde kesildi: ${symbol}`); } }; }
            
            async function updateChart(isNewCoin = false) {
                headerSymbol.textContent = `${currentSymbol.replace("USDT", "")}/USDT`;
                
                const activeTimeframe = TIMEFRAMES.find(tf => tf.interval === currentTimeframe);
                if (activeTimeframe) {
                    const shortLabel = activeTimeframe.interval.replace('h', 's').replace('d', 'g').replace('M', 'a');
                    selectedTimeframeDisplay.textContent = shortLabel;
                }

                setTimeout(async () => {
                    try {
                        const data = await getHistoricalData(currentSymbol, currentTimeframe);
                        subscribeToStream(currentSymbol, currentTimeframe);
                        
                        if (isNewCoin && data && data.length > 0) {
                            const dataSize = data.length;
                            const barsToShow = 150;
                            const fromIndex = Math.max(0, dataSize - barsToShow);
                            const toIndex = dataSize - 1;
                            chart.timeScale().setVisibleLogicalRange({ from: fromIndex, to: toIndex });
                        } else {
                            chart.timeScale().fitContent();
                        }

                    } catch (error) {
                        console.error("Grafik güncellenirken hata oluştu:", error);
                    }
                }, 0);
            }

            // --- EVENT HANDLERS & LISTENERS ---
            function selectTimeframe(interval) {
                currentTimeframe = interval;
                document.querySelectorAll('.timeframe-btn, .timeframe-btn-mobile').forEach(btn => {
                    btn.classList.toggle('btn-active', btn.dataset.interval === interval);
                });
                updateChart();
            }
            
            function selectCoin(symbol) { /* ... unchanged ... */ currentSymbol = symbol; updateChart(true); preFetchDataForSymbol(symbol); }
            function addCoinHandler(newSymbol) { /* ... unchanged ... */ if (!newSymbol || coins.includes(newSymbol)) return; coins.push(newSymbol); saveCoins(); renderDesktopCoinList(); renderMobileCoinList(); selectCoin(newSymbol); closeAddCoinModal(); }
            function deleteCoinHandler(symbol) { /* ... unchanged ... */ if (coins.length <= 1) { return; } coins = coins.filter(c => c !== symbol); saveCoins(); if (currentSymbol === symbol) { selectCoin(coins[0]); } renderDesktopCoinList(); renderMobileCoinList(); }

            // Masaüstü Zaman Aralığı Dropdown
            document.getElementById('timeframe-dropdown-btn').addEventListener('click', (e) => { e.stopPropagation(); document.getElementById('timeframe-list-header').classList.toggle('show'); });
            
            // Masaüstü Coinler Dropdown
            document.getElementById('coins-dropdown-btn').addEventListener('click', (e) => { e.stopPropagation(); document.getElementById('coin-list').classList.toggle('show'); });
            document.getElementById('coin-list').addEventListener('click', (e) => { e.preventDefault(); const target = e.target; const deleteBtn = target.closest('.delete-coin-btn'); const addBtn = target.closest('#add-coin-btn'); const coinItem = target.closest('.coin-item'); if (deleteBtn) { e.stopPropagation(); deleteCoinHandler(deleteBtn.dataset.symbol); } else if (addBtn) { openAddCoinModal(); document.getElementById('coin-list').classList.remove('show'); } else if (coinItem) { selectCoin(coinItem.dataset.symbol); document.getElementById('coin-list').classList.remove('show'); } });

            // Açık dropdown'ları kapatmak için genel click listener
            window.addEventListener('click', (e) => { const coinList = document.getElementById('coin-list'); if (!e.target.closest('#coins-dropdown-btn') && coinList.classList.contains('show')) { coinList.classList.remove('show'); } const timeframeList = document.getElementById('timeframe-list-header'); if (!e.target.closest('#timeframe-dropdown-btn') && timeframeList.classList.contains('show')) { timeframeList.classList.remove('show'); } });

            // --- MOBİL MENU MANTIĞI ---
            const mobileMenu = document.getElementById('mobile-menu');
            const mobileMenuBtn = document.getElementById('mobile-menu-btn'); 
            const mobileMenuCloseBtn = document.getElementById('mobile-menu-close-btn');
            mobileMenuBtn.addEventListener('click', () => mobileMenu.classList.remove('hidden')); 
            mobileMenuCloseBtn.addEventListener('click', () => mobileMenu.classList.add('hidden'));

            // --- ADD COIN MODAL LOGIC ---
            const modal = document.getElementById('add-coin-modal');
            const modalCloseBtn = document.getElementById('modal-close-btn');
            const modalSearchInput = document.getElementById('modal-search-input');
            const modalList = document.getElementById('add-coin-modal-list');

            function renderModalCoinList(filter = '') { /* ... unchanged ... */ modalList.innerHTML = '<div class="text-center text-gray-400">Yükleniyor...</div>'; if (allBinanceSymbols.length === 0) return; const filteredSymbols = allBinanceSymbols .filter(s => s.includes(filter.toUpperCase())) .filter(s => !coins.includes(s)); modalList.innerHTML = ''; if (filteredSymbols.length === 0) { modalList.innerHTML = '<div class="text-center text-gray-400">Sonuç bulunamadı.</div>'; return; } filteredSymbols.forEach(symbol => { const item = document.createElement('a'); item.href = '#'; item.className = 'block p-2 rounded-md hover:bg-gray-700 text-gray-300'; item.textContent = symbol; item.dataset.symbol = symbol; item.onclick = (e) => { e.preventDefault(); addCoinHandler(symbol); }; modalList.appendChild(item); }); }
            function openAddCoinModal() { /* ... unchanged ... */ modal.classList.remove('hidden'); modalSearchInput.value = ''; modalSearchInput.focus(); renderModalCoinList(); }
            function closeAddCoinModal() { /* ... unchanged ... */ modal.classList.add('hidden'); }
            modalCloseBtn.onclick = closeAddCoinModal;
            modal.onclick = (e) => { if (e.target === modal) closeAddCoinModal(); };
            modalSearchInput.oninput = () => renderModalCoinList(modalSearchInput.value);
            
            // Pencere yeniden boyutlandırıldığında grafiği ayarla
            const resizeObserver = new ResizeObserver(entries => { const { width, height } = entries[0].contentRect; chart.resize(width, height); });
            resizeObserver.observe(chartContainer);
            
            // --- İLK YÜKLEME ---
            async function start() {
                loadCoins();
                saveCoins();
                renderTimeframeButtons();
                renderDesktopCoinList();
                renderMobileCoinList();

                if (coins.length > 0) currentSymbol = coins[0];
                
                // Set initial active button
                document.querySelectorAll('.timeframe-btn, .timeframe-btn-mobile').forEach(btn => {
                    btn.classList.toggle('btn-active', btn.dataset.interval === currentTimeframe);
                });
                
                await updateChart(true);
                
                await fetchBinanceSymbols();
                preFetchDataForSymbol(currentSymbol);
            }
            start();
        }
        
        window.onload = initializeApp;
    </script>
</body>
</html>


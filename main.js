document.addEventListener('DOMContentLoaded', () => {
            // --- ハンバーガーメニュー制御 ---
            const hamburgerBtn = document.getElementById('hamburger-btn');
            const hamburgerIcon = document.getElementById('hamburger-icon');
            const navLinks = document.getElementById('nav-links');
            const menuOverlay = document.getElementById('menu-overlay');
            const allLinks = document.querySelectorAll('.nav-links a');

            function toggleMenu() {
                navLinks.classList.toggle('active');
                menuOverlay.classList.toggle('active');
                
                if (navLinks.classList.contains('active')) {
                    hamburgerIcon.textContent = 'close';
                } else {
                    hamburgerIcon.textContent = 'menu';
                }
            }
            hamburgerBtn.addEventListener('click', toggleMenu);
            menuOverlay.addEventListener('click', toggleMenu);
            allLinks.forEach(item => {
                item.addEventListener('click', () => {
                    if (navLinks.classList.contains('active')) toggleMenu();
                });
            });

            // --- ギャラリーの動的読み込み ---
            const slider = document.getElementById('drag-slider');
            const galleryData = [
                { url: "images/大林1.webp" },
                { url: "images/玉井1.webp" },
                { url: "images/大林2.webp" },
                { url: "images/玉井2.webp" },
                { url: "images/大林3.webp" },
                { url: "images/玉井3.webp" },
                { url: "images/大林4.webp" },
                { url: "images/玉井4.webp" }
            ];

            async function loadDynamicGallery() {
                for (let data of galleryData) {
                    const exists = await checkImageExists(data.url);
                    if (exists) {
                        const itemDiv = document.createElement('div');
                        itemDiv.className = 'gallery-item';
                        
                        const img = document.createElement('img');
                        img.src = data.url;
                        img.alt = 'ギャラリー画像';
                        img.loading = 'lazy';
                        img.addEventListener('dragstart', (e) => e.preventDefault());
                        
                        itemDiv.appendChild(img);
                        
                        slider.appendChild(itemDiv);
                    }
                }
            }

            function checkImageExists(url) {
                return new Promise((resolve) => {
                    const img = new Image();
                    img.onload = () => resolve(true);
                    img.onerror = () => resolve(false);
                    img.src = url;
                });
            }

            loadDynamicGallery();

            // --- ギャラリーのドラッグ用プログラム ---
            let isDown = false; let startX; let scrollLeft;
            slider.addEventListener('mousedown', (e) => { isDown = true; slider.classList.add('active'); slider.style.scrollSnapType = 'none'; startX = e.pageX - slider.offsetLeft; scrollLeft = slider.scrollLeft; });
            slider.addEventListener('mouseleave', () => { if (!isDown) return; isDown = false; slider.classList.remove('active'); slider.style.scrollSnapType = 'x mandatory'; });
            document.addEventListener('mouseup', () => { if (!isDown) return; isDown = false; slider.classList.remove('active'); slider.style.scrollSnapType = 'x mandatory'; });
            slider.addEventListener('mousemove', (e) => { if (!isDown) return; e.preventDefault(); const x = e.pageX - slider.offsetLeft; const walk = (x - startX) * 2; slider.scrollLeft = scrollLeft - walk; });
            
            let isDragging = false;
            slider.addEventListener('mousemove', () => { if(isDown) isDragging = true; });
            slider.addEventListener('mouseup', () => { setTimeout(() => isDragging = false, 50); });
            // 動的に追加される要素へのイベント委譲は不要だが、リンクがある場合はSlider全体で調整
            slider.addEventListener('click', (e) => {
                if(isDragging && e.target.closest('a')) {
                    e.preventDefault();
                }
            });

            // --- FAQ（アコーディオン）の開閉プログラム ---
            const faqItems = document.querySelectorAll('.faq-item');
            faqItems.forEach(item => {
                item.addEventListener('click', () => { item.classList.toggle('active'); });
            });

            // ==========================================
            // ▼ たまちゃんチャットボット ▼
            // ==========================================
            const chatButton = document.getElementById('chat-button');
            const chatWindow = document.getElementById('chat-window');
            const chatClose = document.getElementById('chat-close');
            
            if (chatButton && chatClose) {
                chatButton.addEventListener('click', () => { 
                    chatWindow.classList.toggle('active'); 
                });
                chatClose.addEventListener('click', () => { 
                    chatWindow.classList.remove('active'); 
                });
            }

            // ▼ 教えていただいた最新のGAS URLを設定！ ▼
            const gasUrl = "https://script.google.com/macros/s/AKfycby6THg5PeEHYWWwxFV9VvY7kJ3MAMwoEuaJNs_EK_VZWv9alxqsi25RxDQ2wikkI1-H/exec";
            let chatHistory = [];

            window.sendChat = async function() {
                const inputEl = document.getElementById('chat-input');
                const sendBtn = document.getElementById('chat-send');
                const text = inputEl.value.trim();
                if (!text) return;

                // ▼ 連打防止：入力欄とボタンをロック
                inputEl.disabled = true;
                sendBtn.disabled = true;

                appendMessage("user", text);
                inputEl.value = "";

                chatHistory.push({ role: 'user', text: text });
                if (chatHistory.length > 20) chatHistory.shift(); 

                const loadingId = appendMessage("bot", "考え中たま...");

                const fallbackPrompt = "あなたはパーソナルジム「たまフィット」の公式マスコット『たまちゃん』です。元気よく、語尾に「〜たま！」をつけて答えてください。";
                const basePrompt = (typeof SYSTEM_PROMPT !== 'undefined') ? SYSTEM_PROMPT : fallbackPrompt;

                let historyText = chatHistory.map(m => `${m.role === 'user' ? 'あなた' : 'たまちゃん'}: ${m.text}`).join('\n');

                const fullPrompt = `
${basePrompt}

【直近の会話履歴】
${historyText}

【ユーザーの最新の質問】
${text}

上記を踏まえて、短く簡潔に、優しく返信してあげてたま！
markdown記号（**など）は使わないでたま。
`;

                try {
                    const response = await fetch(gasUrl, {
                        method: "POST",
                        headers: { "Content-Type": "text/plain" },
                        body: JSON.stringify({
                            contents: [{ parts: [{ text: fullPrompt }] }] 
                        })
                    });
                    
                    const data = await response.json();
                    
                    if (data.error) {
                        console.error("API Error:", data.error);
                        updateMessage(loadingId, `エラーが発生したたま... (${data.error.message})`);
                        return;
                    }

                    let botText = "ごめんたま、うまく答えられないたま...";
                    if (data.candidates && data.candidates[0].content.parts[0].text) {
                        botText = data.candidates[0].content.parts[0].text;
                        botText = botText.replace(/\*\*/g, "").replace(/\*/g, "・").replace(/#/g, "");
                    }

                    updateMessage(loadingId, botText);
                    
                    chatHistory.push({ role: 'model', text: botText });
                    if (chatHistory.length > 20) chatHistory.shift();

                } catch (e) {
                    console.error("Chatbot Error:", e);
                    updateMessage(loadingId, "通信エラーが発生したたま...。通信環境を確認してもう一度送ってたま！");
                } finally {
                    // ▼ ロック解除：返答が来たら（またはエラーでも）元に戻す
                    inputEl.disabled = false;
                    sendBtn.disabled = false;
                    inputEl.focus(); 
                }
            };

            function appendMessage(role, text) {
                const chatBody = document.getElementById('chat-body');
                const msgDiv = document.createElement('div');
                msgDiv.className = `chat-msg ${role}`;
                msgDiv.innerHTML = text.replace(/\n/g, '<br>'); 
                const msgId = "msg-" + Date.now();
                msgDiv.id = msgId;
                chatBody.appendChild(msgDiv);
                chatBody.scrollTop = chatBody.scrollHeight;
                return msgId;
            }

            function updateMessage(id, text) {
                const msgDiv = document.getElementById(id);
                if(msgDiv) {
                    msgDiv.innerHTML = text.replace(/\n/g, '<br>');
                    const chatBody = document.getElementById('chat-body');
                    chatBody.scrollTop = chatBody.scrollHeight;
                }
            }
        });

// ==========================================
// ▼ 料金表のアコーディオン（合計金額用） ▼
// ==========================================
window.toggleTotal = function(btn) {
    const tr = btn.closest('tr');
    if (!tr) return;
    const nextTr = tr.nextElementSibling;
    
    if (nextTr && nextTr.classList.contains('total-row')) {
        nextTr.classList.toggle('show');
        
        if (nextTr.classList.contains('show')) {
            btn.innerHTML = '▲ 閉じる';
        } else {
            btn.innerHTML = '▼ 合計額を見る';
        }
    }
};
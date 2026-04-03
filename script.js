async function loadData() {
    try {
        const response = await fetch('data.json');
        const data = await response.json();
        
        // Update wallet address
        const walletSpan = document.getElementById('wallet-addr');
        if (walletSpan && data.config && data.config.wallet) {
            walletSpan.innerText = data.config.wallet;
            walletSpan.classList.remove('loading-blinker');
        }
        
        // Update links
        if (data.config && data.config.links) {
            document.getElementById('mexc-link').href = data.config.links.mexc || '#';
            document.getElementById('bybit-link').href = data.config.links.bybit || '#';
            document.getElementById('binance-link').href = data.config.links.binance || '#';
        }

        // Update news
        const newsContainer = document.getElementById('news-container');
        newsContainer.innerHTML = '';
        
        if (data.news && data.news.length > 0) {
            data.news.forEach(item => {
                const a = document.createElement('a');
                a.className = 'news-item';
                a.href = item.link;
                a.target = '_blank';
                
                a.innerHTML = `
                    <div class="news-date">[+] ${item.date} // TELEGRAM </div>
                    <div class="news-title">> ${item.title}</div>
                `;
                newsContainer.appendChild(a);
            });
        } else {
            newsContainer.innerHTML = '<p>NO DATA IN DATABASE.</p>';
        }

    } catch (e) {
        console.log("No dynamic data yet, using fallback UI");
        document.getElementById('news-container').innerHTML = '<p>ERROR: DATABASE OFFLINE.</p>';
    }
}

document.addEventListener('DOMContentLoaded', loadData);

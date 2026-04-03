async function loadData() {
    try {
        const response = await fetch('data.json');
        const data = await response.json();
        
        // Обновляем кошелек
        document.getElementById('wallet-addr').innerText = data.config.wallet;
        
        // Обновляем новости
        const newsContainer = document.getElementById('news-container');
        newsContainer.innerHTML = '';
        
        data.news.forEach(item => {
            const div = document.createElement('div');
            div.className = 'news-item';
            div.style.marginBottom = '1rem';
            div.style.paddingBottom = '1rem';
            div.style.borderBottom = '1px solid rgba(255,255,255,0.05)';
            div.innerHTML = `
                <div style="font-size: 0.8rem; opacity: 0.5;">${item.time}</div>
                <div style="font-weight: 600;">${item.title}</div>
            `;
            newsContainer.appendChild(div);
        });

    } catch (e) {
        console.log("No dynamic data yet, using fallback UI");
    }
}

document.addEventListener('DOMContentLoaded', loadData);

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
            const a = document.createElement('a');
            a.className = 'news-item';
            a.href = item.link;
            a.target = '_blank';
            a.style.display = 'block';
            a.style.marginBottom = '1rem';
            a.style.paddingBottom = '1rem';
            a.style.borderBottom = '1px solid rgba(255,255,255,0.05)';
            a.style.textDecoration = 'none';
            a.style.color = 'inherit';
            a.style.cursor = 'pointer';
            a.innerHTML = `
                <div style="font-size: 0.8rem; opacity: 0.5;">${item.date} ↗️ Telegram</div>
                <div style="font-weight: 600; margin-top: 5px;">${item.title}</div>
            `;
            // Add hover effect
            a.onmouseover = () => a.style.color = '#afff00';
            a.onmouseout = () => a.style.color = 'inherit';
            newsContainer.appendChild(a);
        });

    } catch (e) {
        console.log("No dynamic data yet, using fallback UI");
    }
}

document.addEventListener('DOMContentLoaded', loadData);

from bs4 import BeautifulSoup
import requests
import json
import sys
import io
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def get_wired_articles():
    url = 'https://www.wired.com/category/big-story/'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        'Content-Type': 'application/json'
    }

    try:
        resp = requests.get(url, headers=headers)
        page = BeautifulSoup(resp.text, 'html.parser')
        data = page.find_all('div', class_='SummaryItemWrapper-iwvBff lakSzb summary-item summary-item--has-margin-spacing summary-item--has-border summary-item--article summary-item--no-icon summary-item--text-align-left summary-item--layout-placement-side-by-side-desktop-only summary-item--layout-position-image-left summary-item--layout-proportions-33-66 summary-item--side-by-side-align-top summary-item--side-by-side-image-right-mobile-true summary-item--standard SummaryItemWrapper-iGxRII djdwgT summary-list__item')
        results = []
        for item in data:
                results.append({
                    'title': item.find('h3',class_='SummaryItemHedBase-hiFYpQ dzwliP summary-item__hed').text.strip(),
                    'url':f'https://www.wired.com{item.find('a',class_='SummaryItemHedLink-civMjp ejgyuy summary-item-tracking__hed-link summary-item__hed-link').get('href')}',
                    'img': item.find('img').get('src'),
                    'brief': '',
                    'created_at': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),
                    'category': 'news',
                    'source': 'wired'
                })
        return results

    except Exception as e:
        print(f"Error fetching wired articles: {e}")
        return []

if __name__ == '__main__':
    articles = get_wired_articles()
    print(json.dumps(articles, ensure_ascii=False, indent=2))
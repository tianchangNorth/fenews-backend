import requests
import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def get_juejin_articles():
    url = 'https://api.juejin.cn/recommend_api/v1/article/recommend_all_feed?aid=2608&uuid=7353547692041569828&spider=0'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        'Content-Type': 'application/json'
    }

    body = {
        'client_type': 2608,
        'cursor': "0",
        'id_type': 2,
        'limit': 20,
        'sort_type': 200
    }

    try:
        resp = requests.post(url, headers=headers, data=json.dumps(body))
        items = resp.json()['data']
        results = []

        for item in items:
            if 'item_info' in item and 'article_info' in item['item_info']:
                info = item['item_info']['article_info']
                results.append({
                    'title': info.get('title', ''),
                    'url': f"https://juejin.cn/post/{info.get('article_id')}",
                    'img': info.get('cover_image', ''),
                    'brief': info.get('brief_content', ''),
                    'created_at': info.get('ctime'),
                    'category':'technology',
                    'source': 'juejin'
                })

        return results

    except Exception as e:
        print(f"Error fetching Juejin articles: {e}")
        return []

if __name__ == '__main__':
    articles = get_juejin_articles()
    print(json.dumps(articles, ensure_ascii=False, indent=2))

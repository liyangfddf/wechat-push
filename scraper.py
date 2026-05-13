"""
网页抓取模块 - 从 xianbao.fun 获取最新信息
"""
import json
import requests
from bs4 import BeautifulSoup


def fetch_deals() -> list:
    """
    抓取 xianbao.fun 的最新信息
    返回格式: [{"id": "...", "title": "...", "price": "...", "url": "...", "time": "...", "source": "..."}, ...]
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }

    try:
        resp = requests.get("https://new.xianbao.fun/", headers=headers, timeout=15)
        resp.raise_for_status()
        resp.encoding = "utf-8"
    except Exception as e:
        print(f"[错误] 抓取网页失败: {e}")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    deals = []

    # 尝试解析页面中的信息条目
    # xianbao.fun 的页面结构可能会变化，以下为常见选择器
    items = soup.select("a[href*='deal'], .deal-item, .list-item, article, .item")

    if not items:
        # 备用方案: 尝试查找所有包含链接的主要内容块
        items = soup.select("main a, .content a, .list a, #content a")

    for item in items:
        try:
            title = item.get_text(strip=True)
            if not title or len(title) < 4:
                continue

            link = item.get("href", "")
            if link and not link.startswith("http"):
                link = "https://new.xianbao.fun" + link

            deal_id = link if link else title
            deals.append({
                "id": deal_id,
                "title": title[:200],
                "url": link,
            })
        except Exception:
            continue

    # 如果上面没抓到，尝试 API 方式
    if not deals:
        deals = _try_api()

    return deals


def _try_api() -> list:
    """尝试通过 API 获取数据"""
    api_urls = [
        "https://new.xianbao.fun/api/deals",
        "https://new.xianbao.fun/api/latest",
        "https://new.xianbao.fun/api/v1/deals",
    ]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
        "Referer": "https://new.xianbao.fun/",
    }

    for api_url in api_urls:
        try:
            resp = requests.get(api_url, headers=headers, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                if isinstance(data, list):
                    return _parse_api_data(data)
                elif isinstance(data, dict) and "data" in data:
                    return _parse_api_data(data["data"])
        except Exception:
            continue

    return []


def _parse_api_data(data: list) -> list:
    """解析 API 返回的数据"""
    deals = []
    for item in data:
        if not isinstance(item, dict):
            continue
        deal = {
            "id": str(item.get("id", item.get("url", ""))),
            "title": item.get("title", item.get("name", "")),
            "url": item.get("url", item.get("link", "")),
            "price": item.get("price", ""),
            "source": item.get("source", item.get("platform", "")),
            "time": item.get("time", item.get("created_at", "")),
        }
        if deal["title"]:
            deals.append(deal)
    return deals

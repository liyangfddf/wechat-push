"""
微信推送助手 - 定时抓取 xianbao.fun 并推送到微信
"""
import json
import time
import os
from datetime import datetime

from config import TARGET_URL, INTERVAL_SECONDS, MAX_PUSH_COUNT, SENT_RECORD_FILE
from scraper import fetch_deals
from notifier import send_wechat


def load_sent_ids() -> set:
    """加载已推送的 ID 记录"""
    if os.path.exists(SENT_RECORD_FILE):
        try:
            with open(SENT_RECORD_FILE, "r", encoding="utf-8") as f:
                return set(json.load(f))
        except Exception:
            return set()
    return set()


def save_sent_ids(sent_ids: set):
    """保存已推送的 ID 记录（只保留最近 500 条）"""
    ids_list = list(sent_ids)[-500:]
    with open(SENT_RECORD_FILE, "w", encoding="utf-8") as f:
        json.dump(ids_list, f, ensure_ascii=False)


def format_message(deals: list) -> str:
    """格式化推送内容（Markdown）"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [f"## 最新信息 ({now})\n"]

    for i, deal in enumerate(deals, 1):
        title = deal.get("title", "无标题")
        url = deal.get("url", "")
        price = deal.get("price", "")
        source = deal.get("source", "")

        line = f"**{i}. {title}**"
        if price:
            line += f"  💰 {price}"
        if source:
            line += f"  📦 {source}"
        if url:
            line += f"\n  🔗 [查看详情]({url})"

        lines.append(line)

    lines.append(f"\n---\n共 {len(deals)} 条新信息 | 来源: {TARGET_URL}")
    return "\n\n".join(lines)


def check_and_push():
    """检查新信息并推送"""
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 开始抓取...")

    # 获取最新信息
    deals = fetch_deals()
    if not deals:
        print("未获取到任何信息")
        return

    print(f"获取到 {len(deals)} 条信息")

    # 过滤已推送的
    sent_ids = load_sent_ids()
    new_deals = [d for d in deals if d["id"] not in sent_ids]

    if not new_deals:
        print("没有新信息，跳过推送")
        return

    # 只推送最新的 N 条
    to_push = new_deals[:MAX_PUSH_COUNT]
    print(f"发现 {len(new_deals)} 条新信息，推送 {len(to_push)} 条")

    # 格式化并推送
    content = format_message(to_push)
    title = f"闲报速递: {len(to_push)}条新信息"

    success = send_wechat(title, content)

    # 记录已推送的 ID
    if success:
        for deal in to_push:
            sent_ids.add(deal["id"])
        save_sent_ids(sent_ids)


def run_once():
    """执行一次（测试用）"""
    print("=" * 50)
    print("  微信推送助手 - 单次执行")
    print("=" * 50)
    check_and_push()


def run_loop():
    """定时循环执行"""
    print("=" * 50)
    print("  微信推送助手 - 定时运行")
    print(f"  目标: {TARGET_URL}")
    print(f"  间隔: {INTERVAL_SECONDS} 秒")
    print(f"  推送方式: 请确认已配置 config.py")
    print("  按 Ctrl+C 停止")
    print("=" * 50)

    while True:
        try:
            check_and_push()
        except Exception as e:
            print(f"[错误] 执行出错: {e}")

        print(f"下次检查: {INTERVAL_SECONDS}秒后")
        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "once":
        run_once()
    else:
        run_loop()

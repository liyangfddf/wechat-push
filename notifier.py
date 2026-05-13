"""
微信推送模块 - 支持 Server酱 和 pushplus
"""
import requests
from config import SERVERCHAN_KEY, PUSHPLUS_TOKEN, PUSH_METHOD


def send_wechat(title: str, content: str) -> bool:
    """发送微信消息"""
    if PUSH_METHOD == "serverchan":
        return _send_serverchan(title, content)
    elif PUSH_METHOD == "pushplus":
        return _send_pushplus(title, content)
    else:
        print(f"[错误] 未知推送方式: {PUSH_METHOD}")
        return False


def _send_serverchan(title: str, content: str) -> bool:
    """通过 Server酱 推送到微信"""
    if not SERVERCHAN_KEY:
        print("[错误] 未配置 SERVERCHAN_KEY")
        return False

    url = f"https://sctapi.ftqq.com/{SERVERCHAN_KEY}.send"
    data = {
        "title": title[:100],
        "desp": content,
    }

    try:
        resp = requests.post(url, data=data, timeout=10)
        result = resp.json()
        if result.get("code") == 0:
            print("[成功] Server酱推送成功")
            return True
        else:
            print(f"[失败] Server酱返回: {result}")
            return False
    except Exception as e:
        print(f"[错误] Server酱推送失败: {e}")
        return False


def _send_pushplus(title: str, content: str) -> bool:
    """通过 pushplus 推送到微信"""
    if not PUSHPLUS_TOKEN:
        print("[错误] 未配置 PUSHPLUS_TOKEN")
        return False

    url = "https://www.pushplus.plus/send"
    data = {
        "token": PUSHPLUS_TOKEN,
        "title": title[:100],
        "content": content,
        "template": "markdown",
    }

    try:
        resp = requests.post(url, json=data, timeout=10)
        result = resp.json()
        if result.get("code") == 200:
            print("[成功] pushplus推送成功")
            return True
        else:
            print(f"[失败] pushplus返回: {result}")
            return False
    except Exception as e:
        print(f"[错误] pushplus推送失败: {e}")
        return False

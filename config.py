"""
配置文件 - 本地运行在此填写；GitHub Actions 部署时使用环境变量（secrets）
"""
import os

# ============ 微信推送配置 ============
# 方式1: Server酱 (https://sct.ftqq.com/) - 免费版每天5条
SERVERCHAN_KEY = os.getenv("SERVERCHAN_KEY", "SCT349358TRz6Ny0RPDD6dsehjhr4T4PSu")

# 方式2: pushplus (https://www.pushplus.plus/) - 免费版每天200条
PUSHPLUS_TOKEN = os.getenv("PUSHPLUS_TOKEN", "")

# 选择推送方式: "serverchan" 或 "pushplus"
PUSH_METHOD = "serverchan"

# ============ 抓取配置 ============
# 目标网址
TARGET_URL = "https://new.xianbao.fun/"

# 定时间隔（秒），默认 300 秒 = 5 分钟
INTERVAL_SECONDS = 300

# 最多推送条数（每次抓取后只推送最新的 N 条）
MAX_PUSH_COUNT = 10

# 已推送记录文件（避免重复推送）
SENT_RECORD_FILE = "sent_ids.json"

"""OpenClaw設定"""
import os
from pathlib import Path

# .envファイルを読み込む
_env_path = Path(__file__).parent / ".env"
if _env_path.exists():
    for _line in _env_path.read_text().splitlines():
        _line = _line.strip()
        if _line and not _line.startswith("#") and "=" in _line:
            _key, _val = _line.split("=", 1)
            _val = _val.strip().strip('"').strip("'")
            os.environ.setdefault(_key.strip(), _val)

# SUZURI API
SUZURI_API_BASE = "https://suzuri.jp/api/v1"
SUZURI_TOKEN = os.environ.get("SUZURI_TOKEN", "")

# Hugging Face
HF_TOKEN = os.environ.get("HF_TOKEN", "")
HF_MODEL = "stabilityai/stable-diffusion-xl-base-1.0"

# デザイン保存先
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "designs")

# SUZURIアイテムID → 内部キーのマッピング
# ※実際のIDはSUZURI APIの GET /items で確認して更新すること
SUZURI_ITEM_IDS = {
    "tshirt": 1,
    "hoodie": 7,
    "tote_bag": 18,
    "mug": 13,
    "sticker": 17,
    "phone_case": 28,
}

# アイテム別画像サイズ (幅, 高さ)
ITEM_SIZES = {
    "tshirt": (2520, 2992),
    "hoodie": (2520, 2992),
    "tote_bag": (1969, 1969),
    "mug": (3102, 1260),
    "sticker": (630, 630),
    "phone_case": (1616, 2721),
}

# トリブン（利益）設定
TRIBUN = {
    "tshirt": 400,
    "hoodie": 600,
    "tote_bag": 300,
    "mug": 300,
    "sticker": 200,
    "phone_case": 500,
}

# アイテムセット（ローテーション用）
ITEM_SETS = [
    ["tshirt", "sticker", "tote_bag"],
    ["tshirt", "mug", "phone_case"],
    ["hoodie", "sticker", "tote_bag"],
    ["tshirt", "hoodie", "mug"],
    ["tshirt", "sticker", "mug", "phone_case"],
    ["hoodie", "tote_bag", "phone_case"],
]

# データベース
DB_PATH = os.path.join(os.path.dirname(__file__), "openclaw.db")

# 自動運用設定
DAILY_DESIGNS = 3          # 1日あたりの生成数
SCHEDULE_HOUR = 9          # 毎日何時に実行するか
RETRY_MAX = 3              # エラー時のリトライ回数
RETRY_DELAY_SEC = 60       # リトライ間隔（秒）

# 整合性チェック
assert ITEM_SIZES.keys() == SUZURI_ITEM_IDS.keys(), \
    "ITEM_SIZES and SUZURI_ITEM_IDS must have identical keys"
assert TRIBUN.keys() == SUZURI_ITEM_IDS.keys(), \
    "TRIBUN and SUZURI_ITEM_IDS must have identical keys"

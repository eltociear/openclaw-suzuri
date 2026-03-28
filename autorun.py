"""OpenClaw 完全自動運用スクリプト

cronに登録してこのファイルを実行するだけで、
毎日自動でデザイン生成→SUZURI全商品公開が行われる。

crontab例:
  0 9 * * * cd /path/to/openclaw-suzuri && /usr/bin/python3 autorun.py >> openclaw.log 2>&1
"""
import logging
import os
import sys
import random
import time
from datetime import datetime
from pathlib import Path

# プロジェクトルートをパスに追加
sys.path.insert(0, str(Path(__file__).parent))

from config import DAILY_DESIGNS, SUZURI_TOKEN, HF_TOKEN
from pipeline import run_pipeline
from prompts import SITUATIONS

# .envファイルがあれば読み込む（python-dotenvなしでも動く簡易版）
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, val = line.split("=", 1)
            os.environ.setdefault(key.strip(), val.strip())

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(Path(__file__).parent / "openclaw.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("openclaw.autorun")

# アイテムセット（ローテーション）
ITEM_SETS = [
    ["tshirt", "sticker", "tote_bag"],
    ["tshirt", "mug", "phone_case"],
    ["hoodie", "sticker", "tote_bag"],
    ["tshirt", "hoodie", "mug"],
    ["tshirt", "sticker", "mug", "phone_case"],
    ["hoodie", "tote_bag", "phone_case"],
]


def preflight_check() -> bool:
    """実行前チェック"""
    ok = True
    if not os.environ.get("SUZURI_TOKEN") and not SUZURI_TOKEN:
        logger.error("SUZURI_TOKEN is not set")
        ok = False
    if not os.environ.get("HF_TOKEN") and not HF_TOKEN:
        logger.error("HF_TOKEN is not set")
        ok = False
    return ok


def main():
    logger.info("=" * 50)
    logger.info(f"OpenClaw autorun started: {datetime.now().isoformat()}")
    logger.info(f"Generating {DAILY_DESIGNS} designs")
    logger.info("=" * 50)

    if not preflight_check():
        logger.error("Preflight check failed. Set tokens in .env or environment.")
        sys.exit(1)

    success = 0
    failed = 0

    for i in range(DAILY_DESIGNS):
        try:
            item_types = random.choice(ITEM_SETS)

            logger.info(f"[{i+1}/{DAILY_DESIGNS}] Generating... (items: {', '.join(item_types)})")

            design_id = run_pipeline(
                situation=None,  # ランダム
                item_types=item_types,
                upload=True,     # 自動でSUZURIに公開
            )

            success += 1
            logger.info(f"[{i+1}/{DAILY_DESIGNS}] Success: design_id={design_id}")

            # HuggingFace APIレート制限対策
            if i < DAILY_DESIGNS - 1:
                wait = random.randint(30, 60)
                logger.info(f"Waiting {wait}s before next generation...")
                time.sleep(wait)

        except Exception as e:
            failed += 1
            logger.error(f"[{i+1}/{DAILY_DESIGNS}] Failed: {e}")
            time.sleep(10)

    logger.info("=" * 50)
    logger.info(f"OpenClaw autorun complete: {success} success, {failed} failed")
    logger.info("=" * 50)


if __name__ == "__main__":
    main()

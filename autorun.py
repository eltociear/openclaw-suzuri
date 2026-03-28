"""OpenClaw 完全自動運用スクリプト

cronに登録してこのファイルを実行するだけで、
毎日自動でデザイン生成→SUZURI全商品公開が行われる。

crontab例:
  0 9 * * * cd /path/to/openclaw-suzuri && /usr/bin/python3 autorun.py >> openclaw.log 2>&1
"""
import logging
import random
import sys
import time
from datetime import datetime
from pathlib import Path

# プロジェクトルートをパスに追加
sys.path.insert(0, str(Path(__file__).parent))

from config import DAILY_DESIGNS, SUZURI_TOKEN, HF_TOKEN, ITEM_SETS
from pipeline import run_pipeline

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(Path(__file__).parent / "openclaw.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("openclaw.autorun")


def preflight_check() -> bool:
    """実行前チェック"""
    ok = True
    if not SUZURI_TOKEN:
        logger.error("SUZURI_TOKEN is not set")
        ok = False
    if not HF_TOKEN:
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
                item_types=item_types,
                upload=True,
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

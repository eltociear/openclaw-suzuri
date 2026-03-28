"""定期実行スケジューラ"""
from __future__ import annotations
import random
import time
import logging

from prompts import random_prompt, SITUATIONS
from pipeline import run_pipeline
from config import DAILY_DESIGNS, ITEM_SETS

logger = logging.getLogger(__name__)


def daily_run(count: int = DAILY_DESIGNS, upload: bool = True):
    """日次バッチ: ランダムなシチュエーションでOpenClaw猫を生成"""
    logger.info(f"=== Daily run started: {count} designs ===")

    for i in range(count):
        try:
            item_types = random.choice(ITEM_SETS)
            logger.info(f"[{i+1}/{count}] Generating random OpenClaw design ({', '.join(item_types)})")

            design_id = run_pipeline(
                item_types=item_types,
                upload=upload,
            )

            logger.info(f"[{i+1}/{count}] Done: design_id={design_id}")

            if i < count - 1:
                wait = random.randint(30, 60)
                logger.info(f"Waiting {wait}s for rate limit...")
                time.sleep(wait)

        except Exception as e:
            logger.error(f"[{i+1}/{count}] Failed: {e}")
            time.sleep(10)

    logger.info("=== Daily run complete ===")


def category_run(category: str | None = None, upload: bool = True):
    """カテゴリ集中生成（例: seasonal, funny, japanese_culture）"""
    if category is None:
        category = random.choice(list(SITUATIONS.keys()))

    situations = SITUATIONS[category]
    logger.info(f"=== Category run: {category} ({len(situations)} situations) ===")

    for i, situation in enumerate(situations[:5]):
        try:
            item_types = random.choice(ITEM_SETS)
            logger.info(f"[{i+1}] OpenClaw: {situation}")

            run_pipeline(
                situation=situation,
                style_index=i,
                item_types=item_types,
                upload=upload,
            )

            if i < len(situations) - 1:
                time.sleep(30)

        except Exception as e:
            logger.error(f"Failed for '{situation}': {e}")
            time.sleep(10)

    logger.info("=== Category run complete ===")


if __name__ == "__main__":
    import sys

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

    upload = "--no-upload" not in sys.argv

    if "--category" in sys.argv:
        category = None
        for arg in sys.argv[1:]:
            if arg in SITUATIONS:
                category = arg
                break
        category_run(category=category, upload=upload)
    else:
        count = DAILY_DESIGNS
        for arg in sys.argv[1:]:
            if arg.isdigit():
                count = int(arg)
                break
        daily_run(count=count, upload=upload)

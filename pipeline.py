"""デザイン生成 → SUZURI アップロード 完全自動パイプライン

OpenClaw: ロブスターを被った猫のデザインを自動生成し、
SUZURIに全アイテム公開状態でアップロードする。
人間の操作は一切不要（トークン設定後）。
"""
from __future__ import annotations
import functools
import logging
import time
from datetime import datetime

from config import TRIBUN, ITEM_SIZES, SUZURI_ITEM_IDS, RETRY_MAX, RETRY_DELAY_SEC
from image_generator import ImageGenerator
from suzuri_client import SuzuriClient
from prompts import build_prompt, random_prompt
from db import (
    init_db, save_design, save_product,
    update_design_material_id, update_product_published,
)

logger = logging.getLogger(__name__)


def run_pipeline(
    situation: str | None = None,
    style_index: int | None = None,
    item_types: list[str] | None = None,
    name: str | None = None,
    upload: bool = True,
):
    """デザイン生成 → SUZURI全商品公開 の完全自動処理

    Args:
        situation: シチュエーション（Noneならランダム）
        style_index: スタイル番号（0-9、Noneならランダム）
        item_types: 対象アイテム（デフォルト: 全アイテム）
        name: デザイン名
        upload: SUZURIにアップロード（デフォルト: True = 完全自動）
    """
    init_db()

    # 1. プロンプト生成
    if situation:
        prompt = build_prompt(situation, style_index)
    else:
        prompt, situation, _ = random_prompt()

    if item_types is None:
        item_types = list(ITEM_SIZES.keys())

    if name is None:
        short_situation = situation.replace(" ", "_")[:30]
        name = f"openclaw_{short_situation}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    logger.info(f"Pipeline start: {situation}")
    logger.info(f"Prompt: {prompt[:80]}...")

    # 2. 画像生成（リトライ付き）
    generator = ImageGenerator()
    saved_files = _retry(
        functools.partial(generator.generate_and_save, prompt, item_types, name),
        "Image generation",
    )

    # 3. DB保存
    base_path = list(saved_files.values())[0]
    design_id = save_design(name, prompt, base_path)

    for item_type in item_types:
        tribun = TRIBUN.get(item_type, 300)
        save_product(design_id, item_type, saved_files[item_type], tribun)

    logger.info(f"Design saved: id={design_id}")

    # 4. SUZURIアップロード — 全アイテムを公開状態で一括作成
    if upload:
        client = SuzuriClient()

        material = _retry(
            functools.partial(
                client.create_material_with_all_products,
                image_path=base_path,
                title=f"OpenClaw - {situation}",
                description=(
                    f"OpenClaw: Lobster Cat - {situation}.\n"
                    "AI generated design by OpenClaw, "
                    "the world's first AI agent design-only store."
                ),
                item_types=item_types,
            ),
            "SUZURI upload",
        )

        update_design_material_id(design_id, material["id"])

        # 返却されたproductsから各アイテムの実際のproduct IDを取得
        suzuri_products = {}
        for p in material.get("products", []):
            item = p.get("item", {})
            suzuri_products[item.get("id")] = p.get("id")

        for item_type in item_types:
            item_id = SUZURI_ITEM_IDS.get(item_type)
            product_id = suzuri_products.get(item_id)
            update_product_published(design_id, item_type, product_id)

        logger.info(f"SUZURI published: material_id={material['id']}, items={len(item_types)}")

    logger.info(f"Pipeline complete: {name}")
    return design_id


def _retry(func, label: str):
    """リトライ付き実行"""
    for attempt in range(1, RETRY_MAX + 1):
        try:
            return func()
        except Exception as e:
            logger.warning(f"{label} attempt {attempt}/{RETRY_MAX} failed: {e}")
            if attempt == RETRY_MAX:
                logger.error(f"{label} failed after {RETRY_MAX} attempts")
                raise
            time.sleep(RETRY_DELAY_SEC)


if __name__ == "__main__":
    import sys

    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    situation = None
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            situation = arg
            break

    no_upload = "--no-upload" in sys.argv
    run_pipeline(situation=situation, upload=not no_upload)

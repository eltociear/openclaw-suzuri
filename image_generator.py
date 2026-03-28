"""Hugging Face Inference APIによる画像生成"""
from __future__ import annotations
import logging
import os
from datetime import datetime

from huggingface_hub import InferenceClient
from PIL import Image

from config import HF_TOKEN, HF_MODEL, OUTPUT_DIR, ITEM_SIZES

logger = logging.getLogger(__name__)


class ImageGenerator:
    def __init__(self, token: str | None = None, model: str | None = None):
        self.client = InferenceClient(
            model=model or HF_MODEL,
            token=token or HF_TOKEN,
        )

    def generate(self, prompt: str, negative_prompt: str | None = None) -> Image.Image:
        """プロンプトから画像を生成

        Args:
            prompt: 生成プロンプト（英語推奨）
            negative_prompt: ネガティブプロンプト

        Returns:
            PIL Image
        """
        if negative_prompt is None:
            from prompts import NEGATIVE_PROMPT
            negative_prompt = NEGATIVE_PROMPT

        image = self.client.text_to_image(
            prompt=prompt,
            negative_prompt=negative_prompt,
            width=1024,
            height=1024,
        )
        return image

    def resize_for_item(self, image: Image.Image, item_type: str) -> Image.Image:
        """アイテム種別に合わせてリサイズ（透過PNG、中央配置）

        Args:
            image: 元画像
            item_type: アイテムキー (tshirt, hoodie, etc.)

        Returns:
            リサイズ済みPIL Image (RGBA)
        """
        if item_type not in ITEM_SIZES:
            raise ValueError(f"Unknown item_type: {item_type!r}. Valid: {list(ITEM_SIZES)}")

        target_w, target_h = ITEM_SIZES[item_type]

        # 透過キャンバスを作成
        canvas = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))

        # アスペクト比を保ってリサイズ（contain方式）
        img = image.convert("RGBA")
        ratio = min(target_w / img.width, target_h / img.height)
        new_w = int(img.width * ratio)
        new_h = int(img.height * ratio)
        img = img.resize((new_w, new_h), Image.LANCZOS)

        # 中央配置
        x = (target_w - new_w) // 2
        y = (target_h - new_h) // 2
        canvas.paste(img, (x, y), img)

        return canvas

    def generate_and_save(
        self, prompt: str, item_types: list[str] | None = None, name: str | None = None
    ) -> dict[str, str]:
        """画像を生成し、ベース画像を保存

        SUZURIのresizeModeに任せるため、アイテム別リサイズは行わない。
        ベース画像（1024x1024）をそのままアップロード用に使用する。

        Args:
            prompt: 生成プロンプト
            item_types: 対象アイテムリスト（デフォルト: 全アイテム）
            name: ファイル名プレフィックス

        Returns:
            {item_type: file_path} の辞書（全てベース画像を指す）
        """
        if item_types is None:
            item_types = list(ITEM_SIZES.keys())

        if name is None:
            name = datetime.now().strftime("%Y%m%d_%H%M%S")

        os.makedirs(OUTPUT_DIR, exist_ok=True)

        # 画像生成
        logger.info(f"Generating image: {prompt[:60]}...")
        base_image = self.generate(prompt)

        # ベース画像を保存
        base_path = os.path.join(OUTPUT_DIR, f"{name}_base.png")
        base_image.save(base_path)
        logger.info(f"Base image saved: {base_path}")

        # 全アイテムがベース画像を共有（SUZURI側のresizeModeで調整）
        saved = {item_type: base_path for item_type in item_types}

        return saved

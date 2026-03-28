"""SUZURI APIクライアント"""
from __future__ import annotations
import base64
import logging
import os

import requests

from config import SUZURI_API_BASE, SUZURI_TOKEN, SUZURI_ITEM_IDS, TRIBUN

logger = logging.getLogger(__name__)

MAX_IMAGE_BYTES = 50 * 1024 * 1024  # 50 MB


class SuzuriClient:
    def __init__(self, token: str | None = None):
        self.token = token or SUZURI_TOKEN
        self.base_url = SUZURI_API_BASE
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        })

    def _encode_image(self, image_path: str) -> str:
        """画像をdata URIにエンコード"""
        size = os.path.getsize(image_path)
        if size > MAX_IMAGE_BYTES:
            raise ValueError(f"Image too large: {size} bytes (max {MAX_IMAGE_BYTES})")
        with open(image_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode()
        return f"data:image/png;base64,{image_data}"

    def get_user(self) -> dict:
        """現在のユーザー情報を取得"""
        resp = self.session.get(f"{self.base_url}/user")
        resp.raise_for_status()
        return resp.json()["user"]

    def get_items(self) -> list:
        """利用可能なアイテム一覧を取得"""
        resp = self.session.get(f"{self.base_url}/items")
        resp.raise_for_status()
        return resp.json()["items"]

    def create_material_with_all_products(
        self,
        image_path: str,
        title: str,
        description: str = "",
        item_types: list[str] | None = None,
    ) -> dict:
        """デザインをアップロードし、指定アイテム全てを公開状態で作成

        1回のAPIコールで画像アップロード + 全アイテム商品作成 + 公開 + トリブン設定が完了。

        Args:
            image_path: PNG画像のパス
            title: デザインタイトル
            description: 説明文
            item_types: 作成するアイテムリスト（デフォルト: 全アイテム）

        Returns:
            作成されたmaterial情報（products含む）
        """
        if item_types is None:
            item_types = list(SUZURI_ITEM_IDS.keys())

        texture = self._encode_image(image_path)

        # 全アイテムを公開状態で一括作成（トリブンはアイテム別に設定）
        products = []
        for item_type in item_types:
            item_id = SUZURI_ITEM_IDS.get(item_type)
            if item_id is None:
                logger.warning(f"Unknown item_type: {item_type}, skipping")
                continue
            products.append({
                "itemId": item_id,
                "published": True,
                "resizeMode": "contain",
                "tribun": TRIBUN.get(item_type, 300),
            })

        payload = {
            "texture": texture,
            "title": title,
            "description": description,
            "products": products,
        }

        resp = self.session.post(f"{self.base_url}/materials", json=payload)
        resp.raise_for_status()
        return resp.json()["material"]

    def create_material(
        self,
        image_path: str,
        title: str,
        description: str = "",
        products: list[dict] | None = None,
    ) -> dict:
        """デザインをアップロードして商品を作成（低レベルAPI）

        注意: productsを指定しない場合、商品は作成されない。
        通常は create_material_with_all_products を使用すること。
        """
        texture = self._encode_image(image_path)

        payload = {
            "texture": texture,
            "title": title,
            "description": description,
        }
        if products:
            payload["products"] = products

        resp = self.session.post(f"{self.base_url}/materials", json=payload)
        resp.raise_for_status()
        return resp.json()["material"]

    def get_products(self, user_name: str, offset: int = 0, limit: int = 48) -> list:
        """商品一覧を取得"""
        resp = self.session.get(
            f"{self.base_url}/products",
            params={"userName": user_name, "offset": offset, "limit": limit},
        )
        resp.raise_for_status()
        return resp.json()["products"]

    def get_materials(self, offset: int = 0, limit: int = 48) -> list:
        """マテリアル（デザイン）一覧を取得"""
        resp = self.session.get(
            f"{self.base_url}/materials",
            params={"offset": offset, "limit": limit},
        )
        resp.raise_for_status()
        return resp.json()["materials"]

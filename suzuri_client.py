"""SUZURI APIクライアント"""
import base64
import requests
from config import SUZURI_API_BASE, SUZURI_TOKEN, SUZURI_ITEM_IDS, TRIBUN


class SuzuriClient:
    def __init__(self, token: str = None):
        self.token = token or SUZURI_TOKEN
        self.base_url = SUZURI_API_BASE
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        })

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
        item_types: list[str] = None,
    ) -> dict:
        """デザインをアップロードし、指定アイテム全てを公開状態で作成

        これ1回のAPIコールで:
        - 画像アップロード
        - 全アイテムの商品作成
        - 全商品を公開状態に
        - トリブン（利益）設定
        が完了する。

        Args:
            image_path: PNG画像のパス
            title: デザインタイトル
            description: 説明文
            item_types: 作成するアイテムリスト（デフォルト: 全アイテム）

        Returns:
            作成されたmaterial情報
        """
        if item_types is None:
            item_types = list(SUZURI_ITEM_IDS.keys())

        with open(image_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode()

        texture = f"data:image/png;base64,{image_data}"

        # 全アイテムを公開状態で一括作成
        products = []
        for item_type in item_types:
            item_id = SUZURI_ITEM_IDS.get(item_type)
            if item_id is None:
                continue
            products.append({
                "itemId": item_id,
                "published": True,
                "resizeMode": "contain",
            })

        # トリブンは最も高い値を設定（全商品共通）
        price = max(TRIBUN.get(t, 300) for t in item_types)

        payload = {
            "texture": texture,
            "title": title,
            "description": description,
            "price": price,
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
        price: int = 300,
        products: list[dict] = None,
    ) -> dict:
        """デザインをアップロードして商品を作成（低レベルAPI）"""
        with open(image_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode()

        texture = f"data:image/png;base64,{image_data}"

        payload = {
            "texture": texture,
            "title": title,
            "description": description,
            "price": price,
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

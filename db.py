"""SQLiteデータベース管理"""
import sqlite3
from config import DB_PATH


def init_db():
    """テーブル・インデックス作成"""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS designs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                prompt TEXT NOT NULL,
                base_image_path TEXT,
                suzuri_material_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                design_id INTEGER REFERENCES designs(id),
                item_type TEXT NOT NULL,
                image_path TEXT,
                suzuri_product_id INTEGER,
                tribun INTEGER DEFAULT 300,
                published BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_products_design_id ON products (design_id)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_products_published ON products (published)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_products_design_item ON products (design_id, item_type)")


def save_design(name: str, prompt: str, base_image_path: str) -> int:
    """デザイン情報を保存"""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            "INSERT INTO designs (name, prompt, base_image_path) VALUES (?, ?, ?)",
            (name, prompt, base_image_path),
        )
        return cur.lastrowid


def save_product(design_id: int, item_type: str, image_path: str, tribun: int) -> None:
    """商品情報を保存"""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO products (design_id, item_type, image_path, tribun) VALUES (?, ?, ?, ?)",
            (design_id, item_type, image_path, tribun),
        )


def update_product_published(design_id: int, item_type: str, suzuri_product_id: int) -> None:
    """SUZURI公開後に更新"""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "UPDATE products SET published = 1, suzuri_product_id = ? WHERE design_id = ? AND item_type = ?",
            (suzuri_product_id, design_id, item_type),
        )


def update_design_material_id(design_id: int, material_id: int) -> None:
    """SUZURIマテリアルID更新"""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "UPDATE designs SET suzuri_material_id = ? WHERE id = ?",
            (material_id, design_id),
        )


def get_all_designs() -> list[dict]:
    """全デザイン取得"""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT * FROM designs ORDER BY created_at DESC").fetchall()
        return [dict(r) for r in rows]

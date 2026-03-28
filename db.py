"""SQLiteデータベース管理"""
import sqlite3
from config import DB_PATH


def init_db():
    """テーブル作成"""
    conn = sqlite3.connect(DB_PATH)
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
    conn.commit()
    conn.close()


def save_design(name: str, prompt: str, base_image_path: str) -> int:
    """デザイン情報を保存"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.execute(
        "INSERT INTO designs (name, prompt, base_image_path) VALUES (?, ?, ?)",
        (name, prompt, base_image_path),
    )
    design_id = cur.lastrowid
    conn.commit()
    conn.close()
    return design_id


def save_product(design_id: int, item_type: str, image_path: str, tribun: int):
    """商品情報を保存"""
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO products (design_id, item_type, image_path, tribun) VALUES (?, ?, ?, ?)",
        (design_id, item_type, image_path, tribun),
    )
    conn.commit()
    conn.close()


def update_product_published(design_id: int, item_type: str, suzuri_product_id: int):
    """SUZURI公開後に更新"""
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "UPDATE products SET published = 1, suzuri_product_id = ? WHERE design_id = ? AND item_type = ?",
        (suzuri_product_id, design_id, item_type),
    )
    conn.commit()
    conn.close()


def update_design_material_id(design_id: int, material_id: int):
    """SUZURIマテリアルID更新"""
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "UPDATE designs SET suzuri_material_id = ? WHERE id = ?",
        (material_id, design_id),
    )
    conn.commit()
    conn.close()


def get_all_designs() -> list[dict]:
    """全デザイン取得"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM designs ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

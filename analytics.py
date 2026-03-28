"""売上・パフォーマンス分析"""
import sqlite3
from collections import defaultdict
from config import DB_PATH, TRIBUN


def get_stats() -> dict:
    """全体の統計情報を取得"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    total_designs = conn.execute("SELECT COUNT(*) as c FROM designs").fetchone()["c"]
    total_products = conn.execute("SELECT COUNT(*) as c FROM products").fetchone()["c"]
    published = conn.execute("SELECT COUNT(*) as c FROM products WHERE published = 1").fetchone()["c"]

    # アイテム別集計
    item_counts = conn.execute(
        "SELECT item_type, COUNT(*) as c FROM products GROUP BY item_type"
    ).fetchall()

    # 推定トリブン合計（公開済み商品）
    tribun_rows = conn.execute(
        "SELECT item_type, tribun FROM products WHERE published = 1"
    ).fetchall()
    total_potential_tribun = sum(r["tribun"] for r in tribun_rows)

    conn.close()

    return {
        "total_designs": total_designs,
        "total_products": total_products,
        "published_products": published,
        "items_by_type": {r["item_type"]: r["c"] for r in item_counts},
        "total_potential_tribun": total_potential_tribun,
    }


def get_design_history(limit: int = 20) -> list[dict]:
    """デザイン履歴を取得"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT d.*, COUNT(p.id) as product_count "
        "FROM designs d LEFT JOIN products p ON d.id = p.design_id "
        "GROUP BY d.id ORDER BY d.created_at DESC LIMIT ?",
        (limit,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def print_report():
    """レポートをコンソール出力"""
    stats = get_stats()
    history = get_design_history(10)

    print("\n" + "=" * 50)
    print("  OpenClaw Analytics Report")
    print("=" * 50)
    print(f"\nTotal designs:    {stats['total_designs']}")
    print(f"Total products:   {stats['total_products']}")
    print(f"Published:        {stats['published_products']}")
    print(f"Potential tribun: ¥{stats['total_potential_tribun']:,}")

    if stats["items_by_type"]:
        print("\n--- Items by type ---")
        for item_type, count in sorted(stats["items_by_type"].items()):
            print(f"  {item_type}: {count}")

    if history:
        print("\n--- Recent designs ---")
        for d in history:
            status = "✓" if d.get("suzuri_material_id") else "-"
            print(f"  [{status}] {d['name']} ({d['product_count']} products) - {d['created_at']}")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    print_report()

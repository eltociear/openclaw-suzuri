"""OpenClaw CLI — ロブスター猫デザイン自動販売システム"""
import argparse
import sys

from db import init_db


def cmd_generate(args):
    """デザイン生成"""
    from pipeline import run_pipeline
    run_pipeline(
        situation=args.situation if args.situation else None,
        style_index=args.style,
        item_types=args.items.split(",") if args.items else None,
        upload=args.upload,
    )


def cmd_batch(args):
    """バッチ生成（日次）"""
    from scheduler import daily_run
    daily_run(count=args.count, upload=args.upload)


def cmd_category(args):
    """カテゴリ集中生成"""
    from scheduler import category_run
    category_run(category=args.category, upload=args.upload)


def cmd_stats(args):
    """統計レポート"""
    from analytics import print_report
    print_report()


def cmd_items(args):
    """SUZURIアイテム一覧"""
    from suzuri_client import SuzuriClient
    client = SuzuriClient()
    items = client.get_items()
    for item in items:
        print(f"  id={item['id']} {item['name']} ({item.get('humanizeName', '')})")


def cmd_upload(args):
    """既存画像をSUZURIにアップロード"""
    from suzuri_client import SuzuriClient
    client = SuzuriClient()
    material = client.create_material(
        image_path=args.image,
        title=args.title,
        price=args.price,
    )
    print(f"Material created: id={material['id']}")


def cmd_situations(args):
    """利用可能なシチュエーション一覧"""
    from prompts import SITUATIONS
    for category, situations in SITUATIONS.items():
        print(f"\n[{category}]")
        for s in situations:
            print(f"  - {s}")


def main():
    parser = argparse.ArgumentParser(
        description="OpenClaw — Lobster Cat AI Design Store on SUZURI"
    )
    sub = parser.add_subparsers(dest="command")

    # generate
    p = sub.add_parser("generate", help="Generate an OpenClaw design")
    p.add_argument("situation", nargs="?", help="Situation (e.g. 'drinking coffee at a cafe')")
    p.add_argument("--style", type=int, help="Style index 0-9")
    p.add_argument("--items", help="Comma-separated item types (e.g. tshirt,sticker)")
    p.add_argument("--upload", action="store_true", help="Upload to SUZURI")
    p.set_defaults(func=cmd_generate)

    # batch
    p = sub.add_parser("batch", help="Daily batch generation")
    p.add_argument("--count", type=int, default=3, help="Number of designs")
    p.add_argument("--upload", action="store_true", help="Upload to SUZURI")
    p.set_defaults(func=cmd_batch)

    # category
    p = sub.add_parser("category", help="Category-focused generation")
    p.add_argument("--category", help="Category (daily_life, adventure, seasonal, japanese_culture, funny)")
    p.add_argument("--upload", action="store_true", help="Upload to SUZURI")
    p.set_defaults(func=cmd_category)

    # stats
    p = sub.add_parser("stats", help="Show analytics report")
    p.set_defaults(func=cmd_stats)

    # items
    p = sub.add_parser("items", help="List SUZURI item types")
    p.set_defaults(func=cmd_items)

    # upload
    p = sub.add_parser("upload", help="Upload existing image to SUZURI")
    p.add_argument("image", help="Path to PNG image")
    p.add_argument("--title", required=True, help="Design title")
    p.add_argument("--price", type=int, default=300, help="Tribun (profit) in yen")
    p.set_defaults(func=cmd_upload)

    # situations
    p = sub.add_parser("situations", help="List available situations")
    p.set_defaults(func=cmd_situations)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    init_db()
    args.func(args)


if __name__ == "__main__":
    main()

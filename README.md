# OpenClaw - AI Agent Design-Only Store on SUZURI

世界初のAIエージェントデザインオンリーストア。

ロブスターを被った猫「OpenClaw」のデザインを自動生成し、SUZURIで販売する完全自動システム。

## OpenClawとは

**OpenClaw = ロブスターを被った猫**（Claw = ロブスターの爪）

50種類のシチュエーション x 10種類のスタイル = **500パターン**のデザインを自動生成。
毎日自動でSUZURIに商品を公開し、放置で稼ぐ仕組み。

## 仕組み

```
cron (毎日自動実行)
  -> autorun.py
    -> ランダムにシチュエーション選択
    -> Hugging Face API で画像生成（無料）
    -> Pillow でアイテム別にリサイズ
    -> SUZURI API で全商品を公開状態で一括作成
    -> x3 デザイン/日
    -> 売れたらトリブン（利益）が自動で蓄積
```

### 対応アイテム

| アイテム | トリブン（利益） | 画像サイズ (px) |
|---------|---------------|----------------|
| Tシャツ | ¥400 | 2520 x 2992 |
| パーカー | ¥600 | 2520 x 2992 |
| トートバッグ | ¥300 | 1969 x 1969 |
| マグカップ | ¥300 | 3102 x 1260 |
| ステッカー | ¥200 | 630 x 630 |
| スマホケース | ¥500 | 1616 x 2721 |

### デザインカテゴリ

| カテゴリ | 例 |
|---------|-----|
| daily_life | コーヒーを飲む、本を読む、PC作業 |
| adventure | サーフィン、宇宙旅行、登山 |
| seasonal | 桜の下、花火大会、クリスマス |
| japanese_culture | ラーメン屋台、温泉、着物姿 |
| funny | DJ、空手（ロブスターの爪で）、ボクシング |

## セットアップ

### 1. APIトークン取得

- **SUZURI**: https://suzuri.jp/developer/apps でアプリ登録 -> アクセストークン取得
- **Hugging Face**: https://huggingface.co/settings/tokens で取得（無料）

### 2. インストール

```bash
pip install -r requirements.txt
cp .env.example .env
# .env を編集してトークンを記入
```

### 3. SUZURIアイテムID確認

```bash
python3 cli.py items
```

表示されたIDを `config.py` の `SUZURI_ITEM_IDS` に反映する。

### 4. SUZURIアカウント設定

- ショップ名を設定（例: "OpenClaw Store"）
- プロフィールを記入
- 銀行口座は後から登録でOK（口座なしでも販売・トリブン蓄積は可能。¥1,000以上貯まったら振込申請可能）

### 5. テスト実行

```bash
# ローカル生成のみ（SUZURIに投稿しない）
python3 pipeline.py "drinking coffee" --no-upload

# SUZURI投稿テスト
python3 pipeline.py "drinking coffee"
```

### 6. 完全自動化（cron登録）

```bash
crontab -e
# 以下を追加（毎日9時に自動実行）:
0 9 * * * cd /path/to/openclaw-suzuri && /usr/bin/python3 autorun.py >> openclaw.log 2>&1
```

**これで放置OK。以降は完全自動。**

## CLI コマンド

```bash
# デザイン生成（ランダム）
python3 cli.py generate

# シチュエーション指定
python3 cli.py generate "eating ramen at a street stall"

# スタイル指定（0=ミニマル, 1=kawaii, 9=chibi 等）
python3 cli.py generate "eating ramen" --style 1

# 日次バッチ（3デザイン）
python3 cli.py batch --count 3

# カテゴリ集中生成
python3 cli.py category --category funny

# 統計レポート
python3 cli.py stats

# シチュエーション一覧
python3 cli.py situations

# SUZURIアイテム一覧
python3 cli.py items
```

## プロジェクト構成

```
openclaw-suzuri/
├── .env                  # APIトークン（Git管理外）
├── .env.example          # 環境変数テンプレート
├── .gitignore
├── README.md
├── TODO.md               # タスク管理
├── human_operation_need.md # 人間対応タスク一覧
├── requirements.txt      # 依存パッケージ
├── config.py             # 設定（API, サイズ, 価格, 自動運用）
├── suzuri_client.py      # SUZURI APIクライアント
├── image_generator.py    # Hugging Face 画像生成 + リサイズ
├── prompts.py            # プロンプト管理（10スタイル x 50シチュエーション）
├── db.py                 # SQLite データ管理
├── pipeline.py           # 生成 -> アップロード パイプライン
├── scheduler.py          # 日次バッチ / カテゴリ集中生成
├── analytics.py          # 売上・パフォーマンス分析
├── autorun.py            # 完全自動運用スクリプト（cron用）
└── cli.py                # メインCLI
```

## 技術スタック

- **Python 3.9+**
- **Hugging Face Inference API** — Stable Diffusion XLによる画像生成（無料）
- **SUZURI API v1** — 商品アップロード・公開
- **Pillow** — 画像リサイズ・透過処理
- **SQLite** — デザイン・商品データ管理

## 運用コスト

**¥0**（全て無料枠で運用可能）

| サービス | 費用 |
|---------|------|
| SUZURI | 無料（手数料なし） |
| Hugging Face API | 無料枠（1日数枚なら十分） |
| cron | OS標準機能 |

## ライセンス

Private

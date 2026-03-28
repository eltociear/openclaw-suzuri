# 人間の対応が必要な作業（これだけやれば後は全自動）

## 0. APIトークン再発行（緊急）
- [ ] **Hugging Face トークン再発行**: 旧トークンが期限切れ。https://huggingface.co/settings/tokens で新しいトークンを作成し `.env` を更新
- [ ] **SUZURI APIトークン再確認**: 必要に応じて再発行し `.env` を更新

## 1. APIトークン取得（10分）
- [x] **SUZURI APIトークン**: https://suzuri.jp/developer/apps でアプリ登録 → アクセストークン取得
- [x] **Hugging Face トークン**: https://huggingface.co/settings/tokens で取得（無料）

## 2. 設定ファイル作成（1分）
- [ ] `.env.example` を `.env` にコピーしてトークンを記入
```bash
cp .env.example .env
# .env を編集してトークンを記入
```

## 3. 依存パッケージインストール（1分）
```bash
pip install -r requirements.txt
```

## 4. SUZURIアイテムID確認（5分）
- [ ] `python cli.py items` を実行してアイテムIDを確認
- [ ] `config.py` の `SUZURI_ITEM_IDS` を実際のIDに更新

## 5. SUZURIアカウント設定
- [ ] ショップ名を設定（例: "OpenClaw Store"）
- [ ] プロフィール: 「世界初のAIエージェントデザインオンリーストア」
- [ ] （後でOK）振込先銀行口座を登録 — 口座なしでも販売・トリブン蓄積は可能。引き出したい時に登録すればOK（最低¥1,000から振込申請可能）

## 6. 初回テスト実行
```bash
# ローカル生成のみ（SUZURIに投稿しない）
python pipeline.py "drinking coffee" --no-upload

# SUZURI投稿テスト
python pipeline.py "drinking coffee"
```

## 7. cron登録で完全自動化（これで放置OK）
```bash
crontab -e
# 以下を追加（毎日9時に自動実行）:
0 9 * * * cd /Users/ashimine_ikkou_bp/workspace/openclaw-suzuri && /usr/bin/python3 autorun.py >> openclaw.log 2>&1
```

---

## ここまでやれば以降は完全自動
- 毎日9時に `autorun.py` が起動
- ランダムなシチュエーションのOpenClaw（ロブスター猫）デザインを3つ生成
- 各デザインをTシャツ・パーカー・トートバッグ・マグ・ステッカー・スマホケースとして自動公開
- ログは `openclaw.log` に記録
- トリブン（利益）は自動設定済み — 売れたらSUZURIアカウントに蓄積される
- 銀行口座は後から登録でOK（¥1,000以上貯まったら振込申請可能）

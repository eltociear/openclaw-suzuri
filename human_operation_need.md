# 人間の対応が必要な作業（これだけやれば後は全自動）

## 0. APIトークン再発行（緊急）
- [x] **Hugging Face トークン再発行**: 新しいトークンを作成し `.env` を更新
- [x] **SUZURI APIトークン再発行**: 再発行し `.env` を更新

## 1. GitHub Codespacesで起動
- [ ] https://github.com/eltociear/openclaw-suzuri で「Code」→「Codespaces」→「Create codespace on main」
- [ ] Codespace起動後、Secrets設定で `SUZURI_TOKEN` と `HF_TOKEN` を登録
  - Settings → Codespaces → Secrets → New secret

## 2. OpenClawインストール（Codespace内で実行）
```bash
npm install -g openclaw
openclaw init
```

## 3. スキル登録
```bash
# このリポジトリをOpenClawスキルとして登録
cp -r . ~/.openclaw/skills/suzuri-designer/
```

## 4. Heartbeat設定（自動運用）
`~/.openclaw/openclaw.json` に以下を追加:
```json
{
  "agents": {
    "defaults": {
      "heartbeat": {
        "every": "8h",
        "target": "line",
        "activeHours": {
          "start": "09:00",
          "end": "22:00",
          "timezone": "Asia/Tokyo"
        }
      }
    }
  }
}
```

## 5. LINE連携（オプション）
- [ ] OpenClawのLINE Messaging API連携を設定
  - LINE Developers Console でチャネル作成: https://developers.line.biz/
  - Channel Access Token と Channel Secret を取得
  - `~/.openclaw/openclaw.json` にLINE設定を追加
- [ ] LINEからショップ管理・デザイン生成を操作可能に

## 6. SUZURIアカウント設定（Web UIで手動）
- [ ] **プロフィール画像**: `designs/profile_icon.png` を https://suzuri.jp/settings/profile でアップロード
- [ ] **ヘッダー画像**: `designs/header_banner.png` を同ページでアップロード
- [ ] （後でOK）振込先銀行口座を登録

---

## ここまでやれば以降は完全自動
- OpenClawのHeartbeatが8時間ごとに自動でデザイン生成+SUZURI公開
- LINEから「新しいデザイン作って」「ショップの状況は？」等で対話操作も可能
- トリブン（利益）は自動設定済み — 売れたらSUZURIアカウントに蓄積される
- 銀行口座は後から登録でOK（¥1,000以上貯まったら振込申請可能）

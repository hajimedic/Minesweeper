# マインスイーパー (Minesweeper)
[![GitHub Release](https://img.shields.io/github/v/release/hajimedic/Minesweeper)](https://github.com/hajimedic/minesweeper/releases)

Pythonで実装されたシンプルなマインスイーパーゲームです。

## 概要

このプロジェクトは、クラシックなマインスイーパーゲームをPythonとPygameを使って実装したものです。

## 必要条件

- Python 3.x
- Pygame

## インストール方法

```bash
# 依存パッケージのインストール
pip install -r requirements.txt
```

## 使い方

```bash
python main.py
```

## ゲームの操作方法

- **左クリック**: セルを開く
- **右クリック**: フラグを立てる/取り除く
- **数字セルをクリック**: 周囲のフラグ数が数字と一致している場合、残りのセルを自動的に開放

## 難易度

ゲーム起動時に難易度選択メニューが表示されます。以下の3つの難易度から選択できます：

- **初級 (Beginner)**: 9x9のグリッド、10個の地雷
- **中級 (Intermediate)**: 16x16のグリッド、40個の地雷
- **上級 (Expert)**: 16x30のグリッド、99個の地雷
## ゲームの特徴

- 難易度選択メニュー
- ゲーム終了時の再スタートボタン
- チョード機能（数字とフラグが一致する場合の自動開放）

## プロジェクト構成

- `minesweeper.py` - ゲームのコアロジック
- `game_ui.py` - ゲームのグラフィカルインターフェース
- `main.py` - ゲームの実行ファイル
- `requirements.txt` - 必要なPythonパッケージ
- `.github/workflows/` - GitHub Actions による自動リリース設定

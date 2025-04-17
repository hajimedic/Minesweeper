from game_ui import MinesweeperUI

def main():
    # UIインスタンスを作成して起動（初期状態ではゲームなし）
    ui = MinesweeperUI()
    
    print("マインスイーパーを起動しました！")
    print("起動時に難易度を選択できます")
    print("左クリック: セルを開く")
    print("右クリック: フラグを立てる/取り除く")
    print("ゲーム終了後は再スタートボタンで難易度選択画面に戻れます")
    
    ui.start()

if __name__ == "__main__":
    main()
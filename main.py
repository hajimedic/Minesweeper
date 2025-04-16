from minesweeper import Minesweeper
from game_ui import MinesweeperUI

def main():
    # ゲームの難易度設定
    # 初級: 9x9のグリッド、10個の地雷
    # 中級: 16x16のグリッド、40個の地雷
    # 上級: 16x30のグリッド、99個の地雷
    
    # ここでは初級レベルで設定
    width = 9
    height = 9
    mines = 10
    
    # ゲームインスタンスを作成
    game = Minesweeper(width, height, mines)
    
    # UIを作成して起動
    ui = MinesweeperUI(game)
    
    print("マインスイーパーを起動しました！")
    print("左クリック: セルを開く")
    print("右クリック: フラグを立てる/取り除く")
    print("ウィンドウを閉じるとゲームを終了します")
    
    ui.start()

if __name__ == "__main__":
    main()
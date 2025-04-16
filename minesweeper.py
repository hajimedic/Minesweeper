import random
import time

class Minesweeper:
    def __init__(self, width=10, height=10, mines=10):
        self.width = width
        self.height = height
        self.mines = mines
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.revealed = [[False for _ in range(width)] for _ in range(height)]
        self.flagged = [[False for _ in range(width)] for _ in range(height)]
        self.game_over = False
        self.victory = False
        self.place_mines()
        self.calculate_numbers()
        
    def place_mines(self):
        # ランダムに地雷を配置
        mines_placed = 0
        while mines_placed < self.mines:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if self.board[y][x] != -1:  # -1は地雷を表す
                self.board[y][x] = -1
                mines_placed += 1
                
    def calculate_numbers(self):
        # 各セルの周囲の地雷数を計算
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == -1:  # 地雷のセルはスキップ
                    continue
                
                # 周囲8方向の地雷をカウント
                mine_count = 0
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if (0 <= nx < self.width and 
                            0 <= ny < self.height and 
                            self.board[ny][nx] == -1):
                            mine_count += 1
                            
                self.board[y][x] = mine_count
    
    def reveal(self, x, y):
        # すでに公開済みまたはゲーム終了時は何もしない
        if self.revealed[y][x] or self.game_over or self.flagged[y][x]:
            return
        
        # セルを公開
        self.revealed[y][x] = True
        
        # 地雷を踏んだ場合はゲームオーバー
        if self.board[y][x] == -1:
            self.game_over = True
            return
        
        # 周囲に地雷がない場合、隣接するセルを再帰的に公開
        if self.board[y][x] == 0:
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if (0 <= nx < self.width and 
                        0 <= ny < self.height and 
                        not self.revealed[ny][nx]):
                        self.reveal(nx, ny)
        
        # ゲームクリア条件をチェック
        self.check_victory()
    
    def toggle_flag(self, x, y):
        # すでに公開済みまたはゲーム終了時は何もしない
        if self.revealed[y][x] or self.game_over:
            return
        
        # フラグを切り替え
        self.flagged[y][x] = not self.flagged[y][x]
    
    def check_victory(self):
        # 地雷以外のすべてのセルが公開されたらゲームクリア
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] != -1 and not self.revealed[y][x]:
                    return  # まだ公開されていないセルがある
        
        self.victory = True
        self.game_over = True
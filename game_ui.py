import pygame
import sys
from minesweeper import Minesweeper

class MinesweeperUI:
    def __init__(self, game, cell_size=30):
        self.game = game
        self.cell_size = cell_size
        
        # ウィンドウのサイズを設定
        self.width = game.width * cell_size
        self.height = game.height * cell_size
        
        # 色の定義
        self.colors = {
            'gray': (192, 192, 192),
            'white': (255, 255, 255),
            'red': (255, 0, 0),
            'black': (0, 0, 0),
            'blue': (0, 0, 255),
            'green': (0, 128, 0),
            'dark_red': (128, 0, 0),
            'dark_blue': (0, 0, 128),
            'dark_green': (0, 128, 0),
            'brown': (128, 128, 0),
            'purple': (128, 0, 128),
            'cyan': (0, 128, 128),
            'border': (128, 128, 128)
        }
        
        # 数字の色
        self.number_colors = [
            self.colors['blue'],        # 1
            self.colors['green'],       # 2
            self.colors['red'],         # 3
            self.colors['dark_blue'],   # 4
            self.colors['dark_red'],    # 5
            self.colors['cyan'],        # 6
            self.colors['black'],       # 7
            self.colors['gray']         # 8
        ]
        
        # Pygameの初期化
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("マインスイーパー")
        self.font = pygame.font.SysFont('Arial', 18)
        self.large_font = pygame.font.SysFont('Arial', 24, bold=True)
    
    def draw_board(self):
        self.screen.fill(self.colors['gray'])
        
        # 各セルを描画
        for y in range(self.game.height):
            for x in range(self.game.width):
                rect = pygame.Rect(
                    x * self.cell_size, 
                    y * self.cell_size, 
                    self.cell_size, 
                    self.cell_size
                )
                
                # セルの背景色を決定
                if self.game.revealed[y][x]:
                    if self.game.board[y][x] == -1:  # 地雷
                        pygame.draw.rect(self.screen, self.colors['red'], rect)
                        self.draw_mine(x, y)
                    else:
                        pygame.draw.rect(self.screen, self.colors['white'], rect)
                        if self.game.board[y][x] > 0:
                            self.draw_number(x, y, self.game.board[y][x])
                else:
                    pygame.draw.rect(self.screen, self.colors['gray'], rect)
                    if self.game.flagged[y][x]:
                        self.draw_flag(x, y)
                
                # セルの境界線
                pygame.draw.rect(self.screen, self.colors['border'], rect, 1)
        
        # ゲーム終了メッセージ
        if self.game.game_over:
            overlay = pygame.Surface((self.width, self.height))
            overlay.set_alpha(128)
            overlay.fill(self.colors['black'])
            self.screen.blit(overlay, (0, 0))
            
            if self.game.victory:
                text = self.large_font.render("クリア！おめでとう！", True, self.colors['white'])
            else:
                text = self.large_font.render("ゲームオーバー", True, self.colors['white'])
            
            text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
            self.screen.blit(text, text_rect)
    
    def draw_number(self, x, y, number):
        text = self.font.render(str(number), True, self.number_colors[number - 1])
        text_rect = text.get_rect(center=(
            x * self.cell_size + self.cell_size // 2,
            y * self.cell_size + self.cell_size // 2
        ))
        self.screen.blit(text, text_rect)
    
    def draw_mine(self, x, y):
        # 地雷を描画（円で表現）
        center = (
            x * self.cell_size + self.cell_size // 2,
            y * self.cell_size + self.cell_size // 2
        )
        radius = self.cell_size // 4
        pygame.draw.circle(self.screen, self.colors['black'], center, radius)
    
    def draw_flag(self, x, y):
        # フラグを描画（三角形で表現）
        flag_x = x * self.cell_size + self.cell_size // 4
        flag_y = y * self.cell_size + self.cell_size // 4
        
        points = [
            (flag_x, flag_y),
            (flag_x, flag_y + self.cell_size // 2),
            (flag_x + self.cell_size // 2, flag_y + self.cell_size // 4)
        ]
        
        pygame.draw.polygon(self.screen, self.colors['red'], points)
    
    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return False
        
        if event.type == pygame.MOUSEBUTTONDOWN and not self.game.game_over:
            pos_x, pos_y = event.pos
            board_x = pos_x // self.cell_size
            board_y = pos_y // self.cell_size
            
            if 0 <= board_x < self.game.width and 0 <= board_y < self.game.height:
                if event.button == 1:  # 左クリック
                    self.game.reveal(board_x, board_y)
                elif event.button == 3:  # 右クリック
                    self.game.toggle_flag(board_x, board_y)
        
        return True
    
    def start(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                running = self.handle_event(event)
            
            self.draw_board()
            pygame.display.flip()
            clock.tick(30)
        
        pygame.quit()
        sys.exit()
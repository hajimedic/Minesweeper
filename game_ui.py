import pygame
import sys
from minesweeper import Minesweeper

class MinesweeperUI:
    def __init__(self, cell_size=30):
        # 初期状態ではゲームインスタンスなし
        self.game = None
        self.cell_size = cell_size
        
        # 基本サイズ（メニュー用）
        self.base_width = 300
        self.base_height = 400
        
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
            'border': (128, 128, 128),
            'button': (100, 150, 200),
            'button_hover': (130, 180, 230),
            'bg': (240, 240, 240)
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
        
        # 難易度設定
        self.difficulties = {
            'beginner': {'width': 9, 'height': 9, 'mines': 10, 'label': 'Beginner (9x9, 10 mines)'},
            'intermediate': {'width': 16, 'height': 16, 'mines': 40, 'label': 'Intermediate (16x16, 40 mines)'},
            'expert': {'width': 30, 'height': 16, 'mines': 99, 'label': 'Expert (30x16, 99 mines)'}
        }
        
        # ゲームの状態
        self.game_started = False
        
        # Pygameの初期化
        pygame.init()
        self.screen = pygame.display.set_mode((self.base_width, self.base_height))
        pygame.display.set_caption("Minesweeper")
        self.font = pygame.font.SysFont('Arial', 18)
        self.large_font = pygame.font.SysFont('Arial', 24, bold=True)
        self.title_font = pygame.font.SysFont('Arial', 32, bold=True)
        
        # ボタンの初期化
        self.setup_buttons()
    
    def setup_buttons(self):
        button_width = 220
        button_height = 50
        button_margin = 20
        
        # メインメニュー用ボタン
        self.difficulty_buttons = []
        for i, (diff_key, diff_data) in enumerate(self.difficulties.items()):
            y_pos = 150 + i * (button_height + button_margin)
            button = {
                'rect': pygame.Rect(self.base_width // 2 - button_width // 2, y_pos, button_width, button_height),
                'text': diff_data['label'],
                'hover': False,
                'difficulty': diff_key
            }
            self.difficulty_buttons.append(button)
        
        # ゲームプレイ時のリスタートボタン
        self.restart_button = {
            'rect': pygame.Rect(0, 0, 120, 40),  # 位置は後で調整
            'text': "Restart",
            'hover': False
        }
    
    def start_game(self, difficulty):
        # 選択された難易度でゲームを開始
        diff_data = self.difficulties[difficulty]
        self.game = Minesweeper(diff_data['width'], diff_data['height'], diff_data['mines'])
        self.game_started = True
        
        # ウィンドウサイズを調整
        self.width = self.game.width * self.cell_size
        self.height = self.game.height * self.cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        
        # リスタートボタンの位置を調整
        self.restart_button['rect'] = pygame.Rect(
            self.width // 2 - 60, 
            self.height // 2 + 40, 
            120, 40
        )
    
    def draw_menu(self):
        self.screen.fill(self.colors['bg'])
        
        # タイトルを描画
        title = self.title_font.render("Minesweeper", True, self.colors['black'])
        title_rect = title.get_rect(center=(self.base_width // 2, 80))
        self.screen.blit(title, title_rect)
        
        # 難易度選択ボタンを描画
        info = self.font.render("Select difficulty:", True, self.colors['black'])
        info_rect = info.get_rect(center=(self.base_width // 2, 130))
        self.screen.blit(info, info_rect)
        
        for button in self.difficulty_buttons:
            button_color = self.colors['button_hover'] if button['hover'] else self.colors['button']
            pygame.draw.rect(self.screen, button_color, button['rect'], border_radius=5)
            pygame.draw.rect(self.screen, self.colors['black'], button['rect'], 2, border_radius=5)
            
            button_text = self.font.render(button['text'], True, self.colors['black'])
            text_rect = button_text.get_rect(center=button['rect'].center)
            self.screen.blit(button_text, text_rect)
    
    def draw_board(self):
        if not self.game_started:
            self.draw_menu()
            return
            
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
                text = self.large_font.render("Victory! Congratulations!", True, self.colors['white'])
            else:
                text = self.large_font.render("Game Over", True, self.colors['white'])
            
            text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
            self.screen.blit(text, text_rect)
            
            # 再スタートボタン描画
            self.draw_restart_button()
    
    def draw_restart_button(self):
        button_color = self.colors['button_hover'] if self.restart_button['hover'] else self.colors['button']
        pygame.draw.rect(self.screen, button_color, self.restart_button['rect'], border_radius=5)
        pygame.draw.rect(self.screen, self.colors['black'], self.restart_button['rect'], 2, border_radius=5)
        
        button_text = self.font.render(self.restart_button['text'], True, self.colors['black'])
        text_rect = button_text.get_rect(center=self.restart_button['rect'].center)
        self.screen.blit(button_text, text_rect)
    
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
    
    def restart_game(self):
        # メニュー画面に戻る
        self.game_started = False
        self.game = None
        self.screen = pygame.display.set_mode((self.base_width, self.base_height))
        
        # ボタンのホバー状態をリセット
        self.restart_button['hover'] = False
        for button in self.difficulty_buttons:
            button['hover'] = False
    
    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos_x, pos_y = event.pos
            
            # メニュー画面での処理
            if not self.game_started:
                if event.button == 1:  # 左クリック
                    for button in self.difficulty_buttons:
                        if button['rect'].collidepoint(pos_x, pos_y):
                            self.start_game(button['difficulty'])
                            return True
            
            # ゲーム終了時、再スタートボタンのクリック処理
            elif self.game.game_over and event.button == 1:
                if self.restart_button['rect'].collidepoint(pos_x, pos_y):
                    self.restart_game()
                    return True
            
            # ゲームプレイ中のクリック処理
            elif not self.game.game_over:
                board_x = pos_x // self.cell_size
                board_y = pos_y // self.cell_size
                
                if 0 <= board_x < self.game.width and 0 <= board_y < self.game.height:
                    if event.button == 1:  # 左クリック
                        self.game.reveal(board_x, board_y)
                    elif event.button == 3:  # 右クリック
                        self.game.toggle_flag(board_x, board_y)
        
        # マウス移動処理（ボタンのホバー効果）
        if event.type == pygame.MOUSEMOTION:
            if not self.game_started:
                for button in self.difficulty_buttons:
                    button['hover'] = button['rect'].collidepoint(event.pos)
            elif self.game and self.game.game_over:
                self.restart_button['hover'] = self.restart_button['rect'].collidepoint(event.pos)
        
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
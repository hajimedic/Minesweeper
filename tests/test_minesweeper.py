import pytest

from minesweeper import Minesweeper

def test_init():
    game = Minesweeper(width=10, height=10, mines=10)
    assert game.width == 10
    assert game.height == 10
    assert game.mines == 10
    assert not game.game_over
    assert not game.victory

def test_place_mines():
    game = Minesweeper(width=10, height=10, mines=15)

    mine_count = sum(1 for y in range(10) for x in range(10) if game.board[y][x] == -1)
    assert mine_count == 15

def test_calculate_numbers():
    game = Minesweeper(width=3, height=3, mines=0)
    # ランダムな配置を上書き
    game.board = [
        [-1,  0,  0],
        [ 0, -1,  0],
        [ 0,  0,  0]
    ]
    game.calculate_numbers()

    assert game.board[0][0] == -1
    assert game.board[0][1] == 2
    assert game.board[0][2] == 1

    assert game.board[1][0] == 2
    assert game.board[1][1] == -1
    assert game.board[1][2] == 1

    assert game.board[2][0] == 1
    assert game.board[2][1] == 1
    assert game.board[2][2] == 1

@pytest.fixture
def game_3x3_custom_board():
    game = Minesweeper(width=3, height=3, mines=0) # mines=0 to prevent random mines
    # テスト用の盤面をセットアップ
    game.board = [
        [-1, 0, 0],
        [ 0, 0, 0],
        [ 0, 0, 0]
    ]
    game.calculate_numbers()
    return game

def test_reveal_empty_cell():
    game = Minesweeper(width=5, height=5, mines=0)
    game.reveal(2, 2)
    assert game.revealed[2][2] is True
    # 地雷がない場合、すべてが明らかになりクリアとなるはず
    for y in range(5):
        for x in range(5):
            assert game.revealed[y][x] is True
    assert game.victory is True
    assert game.game_over is True

def test_reveal_mine_game_over(game_3x3_custom_board):
    game_3x3_custom_board.reveal(0, 0)
    assert game_3x3_custom_board.revealed[0][0] is True
    assert game_3x3_custom_board.game_over is True
    assert game_3x3_custom_board.victory is False

def test_reveal_number_cell(game_3x3_custom_board):
    game_3x3_custom_board.reveal(0, 1)
    assert game_3x3_custom_board.revealed[1][0] is True
    assert game_3x3_custom_board.revealed[0][0] is False # 地雷は開かれない
    assert game_3x3_custom_board.game_over is False

def test_reveal_with_flag():
    game = Minesweeper(width=3, height=3, mines=0)
    game.flagged[0][0] = True
    game.reveal(0, 0)
    assert game.revealed[0][0] is False # フラグがある場合は開かれない

def test_toggle_flag():
    game = Minesweeper(width=3, height=3, mines=0)
    assert game.flagged[1][1] is False
    game.toggle_flag(1, 1)
    assert game.flagged[1][1] is True
    game.toggle_flag(1, 1)
    assert game.flagged[1][1] is False

def test_toggle_flag_revealed_cell():
    game = Minesweeper(width=3, height=3, mines=0)
    game.board[1][1] = 1
    game.reveal(1, 1)
    assert game.revealed[1][1] is True
    game.toggle_flag(1, 1)
    assert game.flagged[1][1] is False # 開かれているセルにはフラグを設定できない

def test_chord_reveal(game_3x3_custom_board):
    game_3x3_custom_board.reveal(0, 1) # 数字(1)のセルを開ける
    assert game_3x3_custom_board.revealed[1][0] is True

    game_3x3_custom_board.toggle_flag(0, 0) # 地雷セルにフラグを立てる

    # さらに同じ数字セル(0,1)を開くアクションでコード(周囲の一括展開)を実行
    game_3x3_custom_board.reveal(0, 1)

    # 対象周囲のセルがすべて開かれることを確認
    assert game_3x3_custom_board.revealed[0][0] is False # フラグを立てたセルは開かれない
    assert game_3x3_custom_board.revealed[0][1] is True
    assert game_3x3_custom_board.revealed[1][1] is True
    assert game_3x3_custom_board.revealed[2][0] is True
    assert game_3x3_custom_board.revealed[2][1] is True

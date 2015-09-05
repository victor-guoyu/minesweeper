from minesweeper.models.board import Board


class Game:

    def __init__(self, game_id):
        self.game_id = game_id
        self.board = Board()

    def open_cell(self, x, y):
        if not self.board.game_over:
            return self.board.open_cell(x, y)

    def mark_cell(self, x, y):
        if not self.board.game_over:
            return self.board.mark_cell(x, y)

    def is_game_over(self):
        return self.board.game_over

    def get_user_board(self):
        return self.board.user_board

    def is_win(self):
        return self.board.check_win()

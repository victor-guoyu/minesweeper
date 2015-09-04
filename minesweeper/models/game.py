class Game:

    def __init__(self, game_id, board):
        self.game_id = game_id
        self.board = board

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

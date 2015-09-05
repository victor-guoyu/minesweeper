from random import randint
from enum import Enum


class Directions(Enum):
    TOP_LEFT = 1
    TOP_CENTER = 2
    TOP_RIGHT = 3
    MIDDLE_LEFT = 4
    MIDDLE_RIGHT = 5
    BOTTOM_LEFT = 6
    BOTTOM_CENTER = 7
    BOTTOM_RIGHT = 8


class Position:
    def __init__(self, x, y):
        self.x = x  # x coordinate
        self.y = y  # y coordinate


class Cell:

    def __init__(self, position):
        self.state = False  # is this cell contain mine or not
        self.revealed = False  # whether the user has opened the cell or not
        self.marked = False  # whether the user marked the zone containing a mine
        self.cell_value = 0  # int represent number of mine in surrounding cell
        self.position = position

    def __json__(self, request):
        return dict(
            state=self.state,
            revealed=self.revealed,
            marked=self.marked,
            value=self.cell_value,
            x=self.position.x,
            y=self.position.y
        )


class Board:

    def __init__(self):
        self.grid_size = 15
        self.number_of_mines = 30
        self.__marked_cells = 0
        self.__revealed_cells = 0
        self.game_over = False
        self.__game_board = []
        self.user_board = []

        for i in range(self.grid_size):
            self.__game_board.append([])
            self.user_board.append([])
            for j in range(self.grid_size):
                position = Position(i, j)
                self.__game_board[i].append(Cell(position))
                self.user_board[i].append(Cell(position))

        self.__place_mines()
        self.__place_number()
        self.print_map()

    def mark_cell(self, x, y):
        if self.__marked_cells >= self.number_of_mines:
            return
        self.__game_board[x][y].marked = not self.__game_board[x][y].marked
        self.__update_user_board()
        self.__marked_cells += 1
        return self.user_board

    def open_cell(self, x, y):
        cell = self.__game_board[x][y]
        if cell.revealed:
            return
        if cell.state:
            # game over
            self.game_over = True
            self.__reveal_everything()
        else:
            cell.revealed = True
            self.__revealed_cells += 1
            self.__is_cell_value_zero(cell)
            self.__update_user_board()

        return self.user_board

    def check_win(self):
        if self.__revealed_cells + self.__marked_cells == self.grid_size * self.grid_size:
            # game over
            self.game_over = True
            self.__reveal_everything()
            return True
        else:
            # the game is still going
            return False

    def __reveal_everything(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.__game_board[i][j].revealed = True

        self.user_board = self.__game_board

    def __update_user_board(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                cell = self.__game_board[i][j]
                if cell.marked or cell.revealed:
                    self.user_board[i][j] = cell

    def __is_cell_value_zero(self, cell):
        if cell.cell_value == 0:
            self.__open_neighbours(cell)

    def __open_neighbours(self, cell):
        neighbours = self.__get_neighbours(cell)
        for i in neighbours:
            if not i.revealed:
                i.revealed = True
                self.__revealed_cells += 1
                self.__is_cell_value_zero(i)

    def __get_neighbours(self, cell):
        neighbours = [
            self.__get_adjacent_cell(cell, Directions.TOP_LEFT),
            self.__get_adjacent_cell(cell, Directions.TOP_CENTER),
            self.__get_adjacent_cell(cell, Directions.TOP_RIGHT),
            self.__get_adjacent_cell(cell, Directions.MIDDLE_LEFT),
            self.__get_adjacent_cell(cell, Directions.MIDDLE_RIGHT),
            self.__get_adjacent_cell(cell, Directions.BOTTOM_LEFT),
            self.__get_adjacent_cell(cell, Directions.BOTTOM_CENTER),
            self.__get_adjacent_cell(cell, Directions.BOTTOM_RIGHT)]

        return filter(None, neighbours)

    def __cell_position_precondition(self, position):
        if 0 <= position.x <= self.grid_size - 1 \
                and 0 <= position.y <= self.grid_size - 1:
            return True
        else:
            return False

    # return the adjacent cell  of given cell and direction
    # if not exist return none
    def __get_adjacent_cell(self, cell, direction):
        adj_cell_pos = self.__get_relative_position(cell.position, direction)
        if not self.__cell_position_precondition(adj_cell_pos):
            return None
        else:
            return self.__game_board[adj_cell_pos.x][adj_cell_pos.y]

    def __place_mines(self):
        bomb_counter = self.number_of_mines
        while bomb_counter > 0:
            row = randint(0, self.grid_size-1)
            col = randint(0, self.grid_size-1)
            if not self.__game_board[row][col].state:
                self.__game_board[row][col].state = True
                bomb_counter -= 1

    def __place_number(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                current_cell = self.__game_board[i][j]
                neighbours = self.__get_neighbours(current_cell)
                current_cell.cell_value = self.__bomb_count(neighbours)

    @staticmethod
    def __bomb_count(neighbours):
        count = 0
        for cell in neighbours:
            if cell.state:
                count += 1
        return count

    @staticmethod
    def __get_relative_position(position, direction):
        if direction == Directions.TOP_LEFT:
            return Position(position.x - 1, position.y - 1)

        if direction == Directions.TOP_CENTER:
            return Position(position.x - 1, position.y)

        if direction == Directions.TOP_RIGHT:
            return Position(position.x - 1, position.y + 1)

        if direction == Directions.MIDDLE_LEFT:
            return Position(position.x, position.y - 1)

        if direction == Directions.MIDDLE_RIGHT:
            return Position(position.x, position.y + 1)

        if direction == Directions.BOTTOM_LEFT:
            return Position(position.x + 1, position.y - 1)

        if direction == Directions.BOTTOM_CENTER:
            return Position(position.x + 1, position.y)

        if direction == Directions.BOTTOM_RIGHT:
            return Position(position.x + 1, position.y + 1)

    def print_map(self):
        print('\n'.join([''.join(['{:4}'.format(item.state)
                                  for item in row]) for row in self.__game_board]))

        print('=============================================================')
        print('\n'.join([''.join(['{:4}'.format(item.cell_value)
                                  for item in row]) for row in self.__game_board]))

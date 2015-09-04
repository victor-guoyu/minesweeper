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


class Cell:

    def __init__(self, xcor, ycor):
        self.state = False  # is this cell contain mine or not
        self.revealed = False  # whether the user has opened the cell or not
        self.marked = False  # whether the user marked the zone containing a mine
        self.cell_value = 0  # int represent number of mine in surrounding cell
        self.xcor = xcor  # x coordinate
        self.ycor = ycor  # y coordinate


class Board:

    def __init__(self):
        self.grid_size = 15
        self.number_of_mines = 30
        self.game_over = False
        self.__game_board = []
        self.user_board = []

        for i in range(self.grid_size):
            self.__game_board.append([])
            self.user_board.append([])
            for j in range(self.grid_size):
                self.__game_board[i].append(Cell(i, j))
                self.user_board[i].append(Cell(i, j))

        self.__place_mines()
        self.__place_number()

    def mark_cell(self, x, y):
        self.__game_board[x][y].marked = not self.__game_board[x][y].marked
        self.__update_user_board()
        return self.user_board

    def open_cell(self, x, y):
        cell = self.__game_board[x][y]
        cell.revealed = True
        if cell.state:
            # game over
            self.game_over = True
        else:
            self.__is_cell_value_zero(cell)

        self.__update_user_board()
        return self.user_board

    def __update_user_board(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                cell = self.__game_board[i][j]
                if cell.marked and cell.revealed:
                    self.user_board[i][j] = cell

    def __is_cell_value_zero(self, cell):
        if cell.cell_value == 0:
            self.__open_neighbours(cell)

    def __open_neighbours(self, cell):
        neighbours = self.__get_neighbours(cell)
        for i in neighbours:
            if not i.revealed:
                i.revealed = True
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

    def __cell_position_precondition(self, cell, direction):
        if 0 <= cell.xcor <= self.grid_size - 1 \
                and 0 <= cell.ycor <= self.grid_size - 1 \
                and isinstance(direction, Directions):
            return True
        else:
            return False

    # return the adjacent cell  of given cell and direction
    # if not exist return none
    def __get_adjacent_cell(self, cell, direction):
        if not self.__cell_position_precondition(cell, direction):
            return None

        if direction == Directions.TOP_LEFT:
            return self.__game_board[cell.xcor - 1][cell.ycor - 1]

        if direction == Directions.TOP_CENTER:
            return self.__game_board[cell.xcor][cell.ycor - 1]

        if direction == Directions.TOP_RIGHT:
            return self.__game_board[cell.xcor + 1][cell.ycor - 1]

        if direction == Directions.MIDDLE_LEFT:
            return self.__game_board[cell.xcor - 1][cell.ycor]

        if direction == Directions.MIDDLE_RIGHT:
            return self.__game_board[cell.xcor + 1][cell.ycor]

        if direction == Directions.BOTTOM_LEFT:
            return self.__game_board[cell.xcor - 1][cell.ycor + 1]

        if direction == Directions.BOTTOM_CENTER:
            return self.__game_board[cell.xcor][cell.ycor + 1]

        if direction == Directions.BOTTOM_RIGHT:
            return self.__game_board[cell.xcor + 1][cell.ycor + 1]

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

    def print_map(self):
        print('\n'.join([''.join(['{:4}'.format(item.state)
                                  for item in row]) for row in self.__game_board]))

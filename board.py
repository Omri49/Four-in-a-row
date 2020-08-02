

class Board:
    """ Other then a graphical board, the board as a string exists so the game will know how to read
    it, as it isn't allowed to access the GUI."""
    COLUMN_HEIGHT = 5

    def __init__(self):
        """ Creates the board and the last move played on it """
        self.__board = [['-', '-', '-', '-', '-', '-', '-'],
                        ['-', '-', '-', '-', '-', '-', '-'],
                        ['-', '-', '-', '-', '-', '-', '-'],
                        ['-', '-', '-', '-', '-', '-', '-'],
                        ['-', '-', '-', '-', '-', '-', '-'],
                        ['-', '-', '-', '-', '-', '-', '-']]
        self.__last_move = None

    def __str__(self):
        """
        Gives a visual representation of the board
        """
        return '\n'.join(map(str, self.__board))

    def get_board(self):
        """ Gets the board representation."""
        return self.__board

    def make_move(self, disc, col):
        """ Presents the move on the board, returns True if it was successful so the game function
        will be aware that the move is indeed legal. It simply goes up the column and sees when
        the spot is clear. Also sets the last move played."""
        counter = self.COLUMN_HEIGHT
        while self.__board[counter][col] != '-':  # goes down the row!
            counter -= 1
        if counter < 0:  # bigger then the column length
            return False
        self.__board[counter][col] = disc
        self.set_last_move(counter, col)
        return True

    def set_last_move(self, row, col):
        """ Knowing the last move reduces the amount of checks i need to make to determine if there
        is a winner by a lot. By knowing the final disc, I must only check sequences it exists in."""
        self.__last_move = row, col

    def get_last_move(self):
        return self.__last_move

    def reset(self):
        """ Resets the board to its original position."""
        self.__board = [['-', '-', '-', '-', '-', '-', '-'],
                        ['-', '-', '-', '-', '-', '-', '-'],
                        ['-', '-', '-', '-', '-', '-', '-'],
                        ['-', '-', '-', '-', '-', '-', '-'],
                        ['-', '-', '-', '-', '-', '-', '-'],
                        ['-', '-', '-', '-', '-', '-', '-']]
        self.__last_move = None

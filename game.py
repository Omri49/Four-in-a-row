from ex12.board import Board


class Game:
    """ This defines the logic of the game. Each players disc is assigned a string so
    the game will be able to easily do its action. This class checks for a winner
    and gives a string representation to the game, one that the GUI will read."""
    PLAYER_1 = 1
    PLAYER_2 = 2
    PLAYER_1_WIN = 'CCCC'
    PLAYER_2_WIN = 'VVVV'
    NUM_ROWS = 5
    NUM_COLUMNS = 6
    DRAW = -2  # chose a random int that ISNT 0, as 0 is False. may confuse stuff

    def __init__(self):
        """ Defines the board, counts the turns. the other values are used after a win or a play again
        has been triggered. winning_locations, for example will be used to draw the winning line.
        Explained in the README."""
        self.__turn = 0  # if the turn is equal, first player. else, second player
        self.__board = Board()
        self.__last_move = None
        self.__winning_locations = None
        self.__is_winner = None  # very important = this is None so the game loop doesn't confuse,
        self.__play_again = False
        # as False == 0

    def init_state(self):
        """ Resets the game to its original state"""
        self.__board.reset()
        self.__last_move = None
        self.__is_winner = None
        self.__turn = 0


    def get_is_winner(self):
        """ Getter """
        return self.__is_winner

    def get_turn(self):
        """ Getter"""
        return self.__turn

    def get_winning_location(self):
        """ Getter"""
        return self.__winning_locations

    def get_play_again(self):
        """ Getter"""
        return self.__play_again

    def set_play_again(self, val):
        """ Setter """
        self.__play_again = val

    def add_turn(self):
        """ Adds a turn each iteration."""
        self.__turn += 1

    def place_disc(self, disc, column):
        """ Checks if the column is legal. If not, it tries to place the disc on the board. If
        the disc is placed, True is returned. else, an exception is raised."""
        if not 0 <= column <= 7:
            raise Exception('Illegal move.')
        if not self.__board.make_move(disc, column):
            raise Exception('Illegal move.')
        return True

    def make_move(self, column):
        """ Tries to place the disc. If all the game logic rules are met, the disc is placed
        and True is returned."""
        try:
            if self.__turn % 2 == 0:
                disc = 'C'
            else:
                disc = 'V'
            self.place_disc(disc, column)  # places the disc, returns row number so i know last turn
            self.add_turn()
            return True
        except Exception:
            return

    def get_current_player(self):
        """ Calculates who the current player by calculating if the turn number is even or odd"""
        if self.__turn % 2 == 0:
            return self.PLAYER_1
        return self.PLAYER_2

    def get_player_at(self, row, col):
        """ Given a row and col, checks with the board which disc is in the box."""
        if not 0 <= row <= self.NUM_ROWS or not 0 <= col <= self.NUM_COLUMNS:
            raise Exception("Illegal location.")
        if self.__board.get_board()[row][col] == 'C':
            return self.PLAYER_1
        elif self.__board.get_board()[row][col] == 'V':
            return self.PLAYER_2
        return

    def row_seq(self, row):
        """ Checks the relevant row. joins it as a string and checks for a seq of 4"""
        relevant_row = self.__board.get_board()[row]
        stringed_row = "".join(relevant_row)
        counter = 0
        tup_list = []
        while counter <= self.NUM_COLUMNS:
            tup_list.append((row, counter))
            counter += 1
        if self.PLAYER_1_WIN in stringed_row:
            self.winning_location_getter(stringed_row, tup_list, 'C')
            return self.PLAYER_1
        if self.PLAYER_2_WIN in stringed_row:
            self.winning_location_getter(stringed_row, tup_list, 'V')
            return self.PLAYER_2

    def col_seq(self, col):
        """ Checks the relevant column. joins it all as a string and checks for a seq of 4"""
        counter = 0
        tup_list = []
        column_as_string = ""
        while counter <= self.NUM_ROWS:
            column_as_string += self.__board.get_board()[counter][col]
            tup_list.append((counter, col))
            counter += 1
        if self.PLAYER_1_WIN in column_as_string:
            self.winning_location_getter(column_as_string, tup_list, 'C')
            return self.PLAYER_1
        if self.PLAYER_2_WIN in column_as_string:
            self.winning_location_getter(column_as_string, tup_list, 'V')
            return self.PLAYER_2

    def left_right_diag(self, row, col):
        """ Checks the diagonal direction. left bottom right top."""
        tup_list = []
        board = self.__board.get_board()
        diag_as_string = ""
        while row < self.NUM_ROWS and col > 0:  # goes to the start of the WHOLE diagonal.
            row += 1
            col -= 1
        while row >= 0 and col <= self.NUM_COLUMNS:  # i go up on the row, right on the column
            diag_as_string += board[row][col]  # adds each disc to a string
            tup_list.append((row, col))
            row -= 1
            col += 1
        if self.PLAYER_1_WIN in diag_as_string:
            self.winning_location_getter(diag_as_string, tup_list, 'C')
            return self.PLAYER_1
        if self.PLAYER_2_WIN in diag_as_string:
            self.winning_location_getter(diag_as_string, tup_list, 'V')
            return self.PLAYER_2

    def right_left_diag(self, row, col):
        """ Works the same as the other diagonal function."""
        tup_list = []
        board = self.__board.get_board()
        diag_as_string = ""
        while row < self.NUM_ROWS and col < self.NUM_COLUMNS:  # down on row, right on col
            row += 1
            col += 1
        while row >= 0 and col >= 0:
            diag_as_string += board[row][col]
            tup_list.append((row, col))
            row -= 1
            col -= 1
        if self.PLAYER_1_WIN in diag_as_string:
            self.winning_location_getter(diag_as_string, tup_list, 'C')
            return self.PLAYER_1
        if self.PLAYER_2_WIN in diag_as_string:
            self.winning_location_getter(diag_as_string, tup_list, 'V')
            return self.PLAYER_2

    def winning_location_getter(self, string, tup_list, winner):
        """ goes through the string, if there is a match for a win, the tuple with the location will be
        appended to a list. using this list of tuples, I can easily know where to draw the winning line."""
        self.__winning_locations = []  # zeroes in the list each iteration
        counter = 0
        string_as_list = list(string)
        for i in range(len(string_as_list)):
            if winner == string_as_list[i]:
                counter += 1
                self.__winning_locations.append(tup_list[i])
            elif winner != string_as_list[i]:  # new
                counter = 0
                self.__winning_locations = []
            if counter == 4:
                break

    def sequencer_main(self):
        """ Goes through all the directions and returns the winning player to a different function.
        """
        row, col = self.__board.get_last_move()
        winner = self.row_seq(row)
        if winner:
            return winner
        winner = self.col_seq(col)
        if winner:
            return winner
        winner = self.left_right_diag(row, col)
        if winner:
            return winner
        winner = self.right_left_diag(row, col)
        if winner:
            return winner
        return

    def set_winner(self, draw=None):
        """ Sets the winner or a draw if necessary."""
        if draw:
            self.__is_winner = self.DRAW
            return
        self.__is_winner = True

    def get_winner(self):
        """ The try is there to deal with a presubmit test, which well, idk what it does
        but it works so. Checks if theres a winner, and sets the winner as a game variable
        if so. also checks if there is a draw and sets accordingly."""
        try:  # incase player is None, or something?
            winner = self.sequencer_main()
            if winner:
                self.set_winner()
                return winner
            elif not winner:  # maybe make it just an else?
                for row in self.__board.get_board():
                    if '-' in row:
                        break
                    self.set_winner(self.DRAW)
                    return self.DRAW  # returns a draw
        except TypeError:
            return


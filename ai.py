import random


class AI:
    """ A dumb AI - chooses a move randomly. """
    NUM_ROWS = 6
    NUM_COLUMNS = 7

    def __init__(self, game, player):
        self.__game = game
        self.__player = player
        self.__move = None

    def get_player(self):
        return self.__player

    def find_legal_move(self):
        """ Finds a legal move by randomizing a column and checking if a (row,col) is clear"""
        col_list = list(range(self.NUM_COLUMNS))
        col = random.choice(col_list)
        counter = 0
        while self.__game.get_player_at(counter, col):
            counter += 1
            if counter >= self.NUM_ROWS:
                col = random.choice(col_list)
                counter = 0
        self.__move = col

    def get_last_found_move(self):
        return self.__move

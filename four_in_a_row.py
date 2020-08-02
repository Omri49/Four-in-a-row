from ex12.game import Game
from ex12.ai import AI
from ex12.gui import GUI
from ex12.starting_menu import Menu

P_V_P = 1
AI_V_P = 2
P_V_AI = 3
AI_V_AI = 4
DRAW = -2


def player_decider(main_menu):
    """ This will call game_loop with the proper player configurations"""
    game_type = main_menu.get_player_type()
    if game_type == P_V_P:
        return 1, 2
    elif game_type == AI_V_P:
        ai_1 = AI(game, 1)
        return ai_1, 2
    elif game_type == P_V_AI:
        ai_2 = AI(game, 2)
        return 1, ai_2
    else:
        ai_1 = AI(game, 1)
        ai_2 = AI(game, 2)
        return ai_1, ai_2


def game_loop(player_1, player_2, gui, game):
    """ The main loop function. Each iteration it defines the current player
    and checks if there is a winner. IF the AIs turn is up, does the turn."""
    if game.get_current_player() == 1:  # PLAYER 1
        player = player_1
        current = 1
    else:
        player = player_2
        current = 2
    if game.get_is_winner():
        if game.get_is_winner() == DRAW:
            gui.framer()
            return True  # if game is winner, current gets sent. else, draw
        if current == 2:  # new - to fix the turns
            current = 1
        else:
            current = 2
        gui.framer(current)
        return True
    if isinstance(player, AI):
        if gui.circle_done:
            if current == player.get_player():
                #gui.revert_circle_done()
                player.find_legal_move()
                move = player.get_last_found_move()
                gui.game_binder(move)
    gui.return_root().after(100, game_runner, player_1, player_2, gui, game)


def game_runner(player_1, player_2, gui, game):
    """ Creating an outer function and an inner function makes it siginificantly easier """
    if game_loop(player_1, player_2, gui, game):
        play_again(player_1, player_2, gui, game)


def play_again(player_1, player_2, gui, game):
    """  Checks if 'yes' has been pressed in the GUI, resets the game then
        calls game_runner again. It will call itself again using AFTER aslong as the player hasn't pressed
        a button. """
    if gui.yes_pressed:
        game.init_state()  # resets the game
        gui.reset_yes()  # resets the yes. maybe change it to gui init state?
        game_runner(player_1, player_2, gui, game)
    else:
        gui.return_root().after(100, play_again, player_1, player_2, gui, game)
        # checks if yes has been pressed every once and a while


if __name__ == '__main__':
    """ Defines the main."""
    game = Game()
    menu = Menu()
    players = player_decider(menu)
    gui = GUI(game)
    game_runner(players[0], players[1], gui, game)
    gui.mainloop()




import tkinter as tk

class GUI:
    """ This class defines the GUI. its buttons, its actions and all the relation with
    the game."""
    P_V_P = 1
    AI_V_P = 2
    P_V_AI = 3
    AI_V_AI = 4
    NUM_ROWS = 6
    NUM_COLUMNS = 7
    SCREEN_EDGE = 700  # coordinate for bottom
    DRAW = -2
    WIDTH = 700
    HEIGHT = 600

    def __init__(self, game):
        """ GUI init takes in a game object so the game logic is connected. Creates a list of buttons,
        defines values that will be used in future functions, defines a root."""
        self.__canvas = None
        self.__root = tk.Tk()
        self.__root.attributes('-fullscreen', True)
        self.__old_root = None
        self.__disc = None
        self.col_dict = None
        self.__button_list = []
        self.__game = game
        self.game_definer()
        self.yes_pressed = False
        self.circle_done = True


    def init_state(self):
        """ Reverts the game to its starting position incase a player wishes to play again"""
        self.game_definer()

    def revert_circle_done(self):
        self.circle_done = False

    def return_root(self):
        return self.__root

    def reset_yes(self):
        """ After a player chose to play again, makes it so it won't start automatically again."""
        self.yes_pressed = False

    def update_canvas(self):
        """ Updates the canvas."""
        self.__canvas.update()

    def game_definer(self):
        """ Builds the playing board using 4 functions, each one responsible for a different part
        of the GUI"""
        self.canvas_builder()
        self.create_buttons()
        self.line_create()
        self.column_dictionary()

    def canvas_builder(self):
        """ Builds the canvas according to the colors of my choice. Packs it as well."""
        canvas_width = self.WIDTH
        canvas_height = self.HEIGHT
        canvas = tk.Canvas(self.__root, width=canvas_width, height=canvas_height, bg='deep sky blue')
        canvas.pack()
        self.__canvas = canvas

    def line_create(self):
        """ Creates lines throughout the canvas to create a grid"""
        self.__canvas.create_line(5, 0, 5, self.SCREEN_EDGE, fill='red')  # the first line
        for i in range(1, self.NUM_COLUMNS+1):
            self.__canvas.create_line(100*i, 0, 100*i, self.SCREEN_EDGE, fill='red')
            self.__canvas.create_line(0, i*100, self.SCREEN_EDGE, 100*i, fill='red')

    def column_dictionary(self):
        """ Each column has a dictionary value so the GUI has a concept of depth. The GUI
        has no idea what is in it, but it does know it has limited space using the dictionary.
        Basically used to know where the next disc should fall."""
        col_dict = {}
        for i in range(self.NUM_COLUMNS):
            col_dict[i] = 0
        self.col_dict = col_dict

    def place_buttons(self):
        """ Places the buttons used in the game in my chosen locations."""
        for i in range(len(self.__button_list)):
            self.__button_list[i].place(x=300 + i*100, y=600)

    def create_buttons(self):
        """ Creates all my relevant buttons and places them. this is later used to re-create them
        after unbining it while a move is being played. If victory has been achieved, the buttons
        will not be respawned"""
        if not self.__game.get_winner():  # if victory is achieved, i dont want it to respawn the buttons
            button_1 = tk.Button(self.__root, text="Column 0", command=lambda: self.game_binder(0))  # lambda so it doesnt
            button_2 = tk.Button(self.__root, text="Column 1", command=lambda: self.game_binder(1))  # call it yo
            button_3 = tk.Button(self.__root, text="Column 2", command=lambda: self.game_binder(2))
            button_4 = tk.Button(self.__root, text="Column 3", command=lambda: self.game_binder(3))
            button_5 = tk.Button(self.__root, text="Column 4", command=lambda: self.game_binder(4))
            button_6 = tk.Button(self.__root, text="Column 5", command=lambda: self.game_binder(5))
            button_7 = tk.Button(self.__root, text="Column 6", command=lambda: self.game_binder(6))
            self.__button_list = [button_1, button_2, button_3, button_4, button_5, button_6, button_7]
            self.place_buttons()

    def button_disabler(self):
        """ unbinds the button from doing anything. it will be unbound when a ball is still being dropped"""
        for button in self.__button_list:
            button.unbind('<Button-1>', str(button))

    def game_binder(self, column):
        """ This function basically binds the game with the GUI. Triggered by a button press
        or an AI, it checks with the game if a certain move is legal. If it is, it will visualize
        this move using GUI methods. once the circle is done dropping, a turn will be added and the next
        player will play."""
        if self.__game.make_move(column):
            self.revert_circle_done()   # so the ai doesnt do shit
            self.button_disabler()
            self.draw_circle(column)
            #self.__game.add_turn()
            self.create_buttons()  # adds the turn ONLY when the circle is done falling!
            self.circle_done = True
            return True
        else:
            return

    def winner(self):
        """ If there is a winner, a winning line is drawn."""
        winner = self.__game.get_winner()
        if winner:
            if winner == self.DRAW:  # no line if theres a draw
                return
            tup_list = self.__game.get_winning_location()
            self.draw_winning_line(tup_list)

    def smooth_motion(self, column, x_1, x_2, color):
        """ Calculates the target location of a disc. it does so by checking how many discs
        have been placed in each column. Then, while the discs location is smaller than the target
        location, it progresses it slowly."""
        target_location = [x_1-100, 100 * (self.NUM_ROWS - self.col_dict[column]),
                           x_2-100, 100 * (self.NUM_ROWS - self.col_dict[column])-100]
        while self.__canvas.coords(self.__disc) <= target_location:
            self.__canvas.update()  # updates the canvas each iteration so you can see it fall
            coords_list = self.__canvas.coords(self.__disc)
            y_1 = coords_list[1]
            y_2 = coords_list[3]
            new_disc = self.__canvas.create_oval(x_1, y_1+0.75, x_2, y_2+0.75, fill=color)
            self.__canvas.delete(self.__disc)  # deletes the old disc so it disappears
            self.__disc = new_disc  # defines the new location to be the disc

    def draw_circle(self, column):
        """ Circle is drawn. parameters are the bound of the boxes, this can be gotten as a formula
        from the previous loop. won't be a big problem. i have to connect them to a function, and change
        the filling for each user!"""
        x_1 = 100 + (column * 100)
        x_2 = column * 100
        if self.__game.get_turn() % 2 == 0:
            disc = self.__canvas.create_oval(100 + (column * 100), 0, column * 100,
                                         self.NUM_ROWS - self.col_dict[column] - 1 * 100,
                                         fill='yellow')
            color = "yellow"
        else:  # colors the discs accordingly
            disc = self.__canvas.create_oval(100 + (column * 100), 0, column * 100,
                                         self.NUM_ROWS - self.col_dict[column] - 1 * 100,
                                         fill='red')
            color = "red"
        self.__disc = disc
        self.col_dict[column] += 1
        self.smooth_motion(column, x_1, x_2, color)
        self.winner()  # checks for a victory

    def draw_winning_line(self, tup_list):
        """ Takes in a tup_list which contains a list of the coordinates of the winning discs.
        It calculates the appropriate edge to be drawn then draws it."""
        for item in tup_list:
            x_1 = item[1] * 100 + 100
            x_2 = item[0] * 100
            y_1 = item[1] * 100
            y_2 = item[0] * 100 + 100
            self.__canvas.create_line(x_1, x_2, y_1, y_2, width=15, fill='green')

    def quit_game(self, root):  # new
        """ Destroys the root if the user has chosen to quit the game"""
        root.destroy()

    def play_again(self):  # new
        """ Reverts the board to its original position if the player chose to play again. It will destroy
        the previous root after a certain amount of time as I need the four_in_a_row file to use
        an old root method one last time."""
        self.yes_pressed = True
        self.__canvas.delete("all")  # wipes the canvas
        self.__old_root = self.__root  # so i can kill the old root
        self.__root = tk.Tk()  # new root
        self.__root.attributes('-fullscreen', True)
        self.__game.init_state()  # redoes the game (needs to happen twice due to buttons)
        self.init_state()  # redoes the gui
        self.__old_root.after(500, self.quit_game, self.__old_root)  # kills the old root after half a sec

    def framer(self, player=None):
        """ Creates a frame that asks the player if he wishes to play again. If he doesn't,
        the root is destroyed. If he does, play again he shall."""
        self.__root.wm_title('GAME OVER')
        if not player:
            label = tk.Label(self.__root, text='An unfortunate draw. Would you like to play again?')
        else:
            label = tk.Label(self.__root, text='Congratulations Player ' + str(player) +
                                               '! Would you like to play again?')
        label.place(relx=0.4, rely=0.4)
        button_yes = tk.Button(self.__root, text='yes', command=self.play_again)
        button_no = tk.Button(self.__root, text='nope', command=lambda: self.quit_game(self.__root))
        button_yes.place(relx=0.45, rely=0.45)
        button_no.place(relx=0.55, rely=0.45)

    def mainloop(self):
        self.__root.mainloop()

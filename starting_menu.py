import tkinter as tk


class Menu:
    """ This starting menu exists so I wont have to withdraw the main root and pause all actions
    on it. I don't think it makes sense to start with a root withdrawn, so the GUI will only be
    activated when the player is ready to play."""
    P_V_P = 1
    AI_V_P = 2
    P_V_AI = 3
    AI_V_AI = 4

    def __init__(self):
        """ Starts with a default type, a root and initiates the GUI."""
        self.__player_type = 0
        self.__root = tk.Tk()
        self.starting_menu()

    def starting_menu(self):
        """ Defines the starting menu and its buttons."""
        first_choice = tk.Label(self.__root, width="40", height="10", bg="red")
        second_choice = tk.Label(self.__root, width="40", height="10", bg="green")
        button_ai_1 = tk.Button(self.__root, text='Ai vs Player', command=lambda: self.player_type(self.AI_V_P))
        button_ai_2 = tk.Button(self.__root, text='Player vs Ai', command=lambda: self.player_type(self.P_V_AI))
        button_human_1 = tk.Button(self.__root, text='Player vs Player', command=lambda: self.player_type(self.P_V_P))
        button_human_2 = tk.Button(self.__root, text='Ai vs Ai', command=lambda: self.player_type(self.AI_V_AI))
        first_choice.rowconfigure(10, weight=1)  # allows me to place in the middle
        second_choice.rowconfigure(10, weight=1)
        first_choice.rowconfigure(11, weight=1)  # allows me to place in the middle
        second_choice.rowconfigure(11, weight=1)
        first_choice.grid(row=10, column=5, rowspan=2)
        second_choice.grid(row=10, column=6, rowspan=2)
        button_ai_1.grid(row=10, column=5)
        button_ai_2.grid(row=10, column=6)
        button_human_1.grid(row=11, column=5)
        button_human_2.grid(row=11, column=6)
        self.root_mainloop()

    def root_mainloop(self):
        self.__root.mainloop()

    def player_type(self, type):
        """ According to the type given from the button, sets the type.
        The root will be destroyed 10ms after this button is pressed so the
        player type will be able to 'reach' the game. """
        self.__player_type = type
        self.__root.after(10, self.destroy)  # it destroys the window in justtt a little bit

    def get_player_type(self):
        """ Returns the type."""
        return self.__player_type

    def destroy(self):
        self.__root.destroy()




# gui/gui.py

import tkinter as tk
from tkinter import messagebox
from threading import Thread
from game import Game
from agent import Agent

class MinesweeperGUI:
    def __init__(self, settings, dispatcher):
        self.dispatcher = dispatcher
        self.root = tk.Tk()
        self.root.title("Minesweeper")
        self.game = Game(settings, dispatcher)
        self.agent = Agent(dispatcher)
        self.buttons = {}
        self.create_widgets()
        self.register_events()

    def create_widgets(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack()
        for y in range(self.game.height):
            for x in range(self.game.width):
                button = tk.Button(self.frame, width=2, command=lambda x=x, y=y: self.on_cell_click(x, y))
                button.grid(row=y, column=x)
                self.buttons[(x, y)] = button
        self.assist_button = tk.Button(self.root, text="Assist", command=self.request_assistance)
        self.assist_button.pack()

    def on_cell_click(self, x, y):
        self.game.handle_click(x, y)

    def register_events(self):
        self.dispatcher.register('game_updated', self.update_cell_display)
        self.dispatcher.register('game_lost', self.on_game_lost)
        self.dispatcher.register('game_won', self.on_game_won)
        self.dispatcher.register('request_odds', self.display_odds)

    def update_cell_display(self, cell):
        button = self.buttons[(cell.x, cell.y)]
        if cell.is_mine:
            button.config(text="*", bg="red", state="disabled")
        else:
            button.config(text=str(cell.adjacent_mines), state="disabled")
        # Optionally, update probability meter here

    def on_game_lost(self, _):
        messagebox.showinfo("Game Over", "You hit a mine!")
        self.root.quit()

    def on_game_won(self, _):
        messagebox.showinfo("Congratulations", "You've cleared the minefield!")
        self.root.quit()

    def request_assistance(self):
        self.dispatcher.dispatch('request_odds', None)

    def display_odds(self, advice):
        # Highlight recommended cells
        for x, y in advice:
            button = self.buttons[(x, y)]
            button.config(bg="yellow")

    def run(self):
        self.root.mainloop()

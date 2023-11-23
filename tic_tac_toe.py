import os
import time
import tkinter as tk
from tkinter import messagebox
from random import choice

HUMAN = -1
COMP = +1
board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]

def wins(state, player):
    win_state = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]
    return [player, player, player] in win_state

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        self.choice_dialog()

    def choice_dialog(self):
        choice_var = tk.StringVar(value="X")

        choice_label = tk.Label(self.root, text="Start 'First' or 'Not':")
        choice_label.grid(row=0, column=0, columnspan=2)

        choice_radio_x = tk.Radiobutton(self.root, text="yes", variable=choice_var, value="X")
        choice_radio_o = tk.Radiobutton(self.root, text="No", variable=choice_var, value="O")

        choice_radio_x.grid(row=1, column=0)
        choice_radio_o.grid(row=1, column=1)

        start_button = tk.Button(self.root, text="Start", command=lambda: self.start_game(choice_var.get()))
        start_button.grid(row=2, column=0, columnspan=2)

    def start_game(self, player_choice):
        self.player_choice = player_choice
        self.initialize_board()

    def initialize_board(self):
        for i in range(3):
            for j in range(3):
                button = tk.Button(self.root, text="", font=('normal', 20), height=2, width=5,
                                   command=lambda row=i, col=j: self.on_button_click(row, col))
                button.grid(row=i + 3, column=j)
                self.buttons[i][j] = button

        if self.player_choice == "O":
            self.ai_turn()
            self.game_over()

    def on_button_click(self, row, col):
        if board[row][col] == 0:
            self.set_move(row, col, HUMAN)
            if not self.game_over():
                self.ai_turn()
                self.game_over()

    def set_move(self, x, y, player):
        board[x][y] = player
        self.buttons[x][y].config(text="X" if player == HUMAN else "O", state=tk.DISABLED)

    def ai_turn(self):
        depth = len(empty_cells(board))
        if depth == 0 or self.game_over():
            return

        move = minimax(board, depth, COMP)
        x, y = move[0], move[1]
        self.set_move(x, y, COMP)

    def game_over(self):
        if wins(board, HUMAN):
            messagebox.showinfo("Game Over", "You win!")
            self.reset_game()
        elif wins(board, COMP):
            messagebox.showinfo("Game Over", "Computer wins!")
            self.reset_game()
        elif len(empty_cells(board)) == 0:
            messagebox.showinfo("Game Over", "It's a draw!")
            self.reset_game()

    def reset_game(self):
        for i in range(3):
            for j in range(3):
                board[i][j] = 0
                self.buttons[i][j].config(text="", state=tk.NORMAL)

        if self.player_choice == "O":
            self.ai_turn()
            self.game_over()

def minimax(state, depth, player):
    if player == COMP:
        best = [-1, -1, float('-inf')]
    else:
        best = [-1, -1, float('inf')]

    if depth == 0 or game_over(state):
        score = evaluate(state)
        return [-1, -1, score]

    for cell in empty_cells(state):
        x, y = cell
        state[x][y] = player
        score = minimax(state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == COMP:
            best = max(best, score, key=lambda p: p[2])
        else:
            best = min(best, score, key=lambda p: p[2])

    return best

def evaluate(state):
    if wins(state, COMP):
        return +1
    elif wins(state, HUMAN):
        return -1
    else:
        return 0

def game_over(state):
    return wins(state, HUMAN) or wins(state, COMP)

def empty_cells(state):
    return [(x, y) for x in range(3) for y in range(3) if state[x][y] == 0]

def main():
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()

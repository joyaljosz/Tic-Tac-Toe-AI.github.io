import os

import streamlit as st
import time
from random import choice

HUMAN = -1
COMP = +1
board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]

def evaluate(state):
    if wins(state, COMP):
        return +1
    elif wins(state, HUMAN):
        return -1
    else:
        return 0


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


def game_over(state):
    return wins(state, HUMAN) or wins(state, COMP)


def empty_cells(state):
    return [(x, y) for x in range(3) for y in range(3) if state[x][y] == 0]


def valid_move(x, y):
    return (x, y) in empty_cells(board)


def set_move(x, y, player):
    if valid_move(x, y):
        board[x][y] = player
        return True
    return False


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


def clean():
    os.system('clear' if os.name == 'posix' else 'cls')
def render(state, c_choice, h_choice):
    chars = {-1: h_choice, +1: c_choice, 0: ' '}
    str_line = '---------------'

    print('\n' + str_line)
    for row in state:
        for cell in row:
            symbol = chars[cell]
            print(f'| {symbol} |', end='')
        print('\n' + str_line)


def ai_turn(c_choice, h_choice):
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    clean()
    print(f'Computer turn [{c_choice}]')
    render(board, c_choice, h_choice)

    if depth == 9:
        x, y = choice([(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)])
    else:
        move = minimax(board, depth, COMP)
        x, y = move[0], move[1]

    set_move(x, y, COMP)
    time.sleep(1)


def human_turn(c_choice, h_choice):
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    moves = {1: (0, 0), 2: (0, 1), 3: (0, 2), 4: (1, 0), 5: (1, 1), 6: (1, 2), 7: (2, 0), 8: (2, 1), 9: (2, 2)}

    clean()
    print(f'Human turn [{h_choice}]')
    render(board, c_choice, h_choice)

    move = -1
    while move < 1 or move > 9:
        try:
            move = int(input('Use numpad (1..9): '))
            coord = moves.get(move)
            if coord and set_move(*coord, HUMAN):
                break
            else:
                print('Bad move')
                move = -1
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (ValueError, TypeError):
            print('Bad choice')


def main():
    h_choice = ''
    c_choice = ''
    first = ''

    while h_choice not in ('O', 'X'):
        try:
            h_choice = input('Choose X or O\nChosen: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()

    c_choice = 'O' if h_choice == 'X' else 'X'

    while first not in ('Y', 'N'):
        try:
            first = input('First to start?[y/n]: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()

    while len(empty_cells(board)) > 0 and not game_over(board):
        if first == 'N':
            ai_turn(c_choice, h_choice)
            first = ''
        human_turn(c_choice, h_choice)
        ai_turn(c_choice, h_choice)

    if wins(board, HUMAN):
        clean()
        print(f'Human turn [{h_choice}]')
        render(board, c_choice, h_choice)
        print('YOU WIN!')
    elif wins(board, COMP):
        clean()
        print(f'Computer turn [{c_choice}]')
        render(board, c_choice, h_choice)
        print('YOU LOSE!')
    else:
        clean()
        render(board, c_choice, h_choice)
        print('DRAW!')

    exit()


if __name__ == '__main__':
    main()


# Streamlit UI
st.title("Tic-Tac-Toe Game")

# Sidebar for options
h_choice = st.sidebar.radio("Choose X or O", ('X', 'O'))
first = st.sidebar.radio("First to start?", ('Yes', 'No'))

c_choice = 'O' if h_choice == 'X' else 'X'

st.sidebar.text(f"You chose: {h_choice}")
st.sidebar.text(f"Computer chose: {c_choice}")

st.sidebar.text("Game Instructions:")
st.sidebar.text("Use the numpad (1..9) to make a move.")

# Main game loop
while len(empty_cells(board)) > 0 and not game_over(board):
    if first == 'No':
        ai_turn(c_choice, h_choice)
        first = ''
    human_turn(c_choice, h_choice)
    ai_turn(c_choice, h_choice)

# Display result
st.title("Game Over!")
if wins(board, HUMAN):
    st.success('You Win!')
elif wins(board, COMP):
    st.error('You Lose!')
else:
    st.info('It\'s a Draw!')

# Render the final board
render(board, c_choice, h_choice)

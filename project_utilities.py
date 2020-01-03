EPOCHS = 3
LEARNING_RATE = 1e-3

def convert_board(board, team):
    mod_board_state = []
    for row in board:
        mod_row = []
        for chip in row:
            #0 = empty space; 1 = player space; 2 = opponent space
            if chip.team == team: mod_row.append(1)
            elif chip.team == '.': mod_row.append(0)
            else: mod_row.append(2)
        mod_board_state.append(mod_row)
    return mod_board_state
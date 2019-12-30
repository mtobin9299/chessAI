import chip
import cfl
import os
import numpy as np 
from datetime import datetime

from chip import *

def play_random_turn(cf, team):
    tie = False
    while True:
        slot = cfl.chooseRandSlot(cf,team)
        if slot == -1: #board is full
            game_over = True
            tie = True
            break
        inserted = Chip(team)
        if(cf.addPiece(inserted,slot)):
            game_over = cf.checkForWin(inserted)[0]
            break
    return cf, slot, game_over, tie

def play_random_data_game():
    cf = cfl.ConnectFour()
    game_over = False
    tie = False
    red_data = []
    yellow_data = []

    while not game_over:
        #Red Turn
        pre_move_board = cf.board
        cf, slot, game_over, tie = play_random_turn(cf, 'R')
        red_data.append([pre_move_board, slot])
        if game_over:
            winner = 'R'
            break
        #Yellow Turn
        pre_move_board = cf.board
        cf, slot, game_over, tie = play_random_turn(cf, 'Y')
        yellow_data.append([pre_move_board, slot])
        if game_over: 
            winner = 'Y'
            break
    
    if tie: return ([], '-')
    return (red_data, 'R') if winner == 'R' else (yellow_data, 'Y')


def generate_random_population(num_of_games):
    training_data = []
    for _ in range(num_of_games):
        game_data, winner = play_random_data_game()
        for data in game_data:
            board_state = data[0]
            chosen_slot = data[1]
            one_hot_slot = np.zeros(7)
            one_hot_slot[chosen_slot] = 1
            training_data.append([np.array(board_state), one_hot_slot, winner])
    return training_data

def prep_training_data(training_data):
    mod_training_data = []
    for data in training_data:
        board_state = data[0]
        one_hot_slot = data[1]
        winner = data[2]

        mod_board_state = []
        for row in board_state:
            mod_row = []
            for chip in row:
                #0 = empty space; 1 = player space; 2 = opponent space
                if chip.team == winner: mod_row.append(1)
                elif chip.team == '.': mod_row.append(0)
                else: mod_row.append(2)
            mod_board_state.append(mod_row)
        mod_training_data.append([mod_board_state, one_hot_slot])
    return mod_training_data

        

def main(num_of_games=100000, model=None):
    if model is None:
        training_data = prep_training_data(generate_random_population(num_of_games))
        training_data_save = np.array(training_data)
        date_time = datetime.now().strftime("%H-%M")
        if not os.path.exists("training_data"): os.mkdir("training_data")
        filename = 'cf_training_data-' + date_time + '.npy'
        np.save('training_data\\' + filename, training_data_save)
        print(training_data_save.size)

main(100)

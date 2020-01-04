import chip
import cfLogic
import network_module
import os
import numpy as np 
import project_utilities
from datetime import datetime

from chip import *

def play_random_turn(cf, team):
    tie = False
    while True:
        slot = cfLogic.chooseRandSlot(cf,team)
        if slot == -1: #board is full
            game_over = True
            tie = True
            break
        inserted = Chip(team)
        if(cf.addPiece(inserted,slot)):
            game_over = cf.checkForWin(inserted)[0]
            break
    return cf, slot, game_over, tie

def play_model_turn(cf, team, model):
    tie = False
    converted_board = project_utilities.convert_board(cf.board, team)
    board_input = np.resize(converted_board, (1, len(converted_board[0]) * len(converted_board), 1))
    chosen_slot = np.argmax(model.predict(board_input)[0])
    played_chip = Chip(team)
    if not cf.addPiece(played_chip, chosen_slot):
        cf, chosen_slot, game_over, tie = play_random_turn(cf, team)
    else:
        game_over = cf.checkForWin(played_chip)[0]
    return cf, chosen_slot, game_over, tie

def play_data_game(model):
    cf = cfLogic.ConnectFour()
    game_over = False
    tie = False
    red_data = []
    yellow_data = []

    while not game_over:
        #Red Turn
        pre_move_board = cf.board
        if model is None: 
            cf, slot, game_over, tie = play_random_turn(cf, 'R')
        else:
            cf, slot, game_over, tie = play_model_turn(cf, 'R', model)
        red_data.append([pre_move_board, slot])
        if game_over:
            winner = 'R'
            break
        #Yellow Turn
        pre_move_board = cf.board
        if model is None: 
            cf, slot, game_over, tie = play_random_turn(cf, 'Y')
        else:
            cf, slot, game_over, tie = play_model_turn(cf, 'Y', model)
        yellow_data.append([pre_move_board, slot])
        if game_over: 
            winner = 'Y'
            break
    
    if tie: return ([], '-')
    return (red_data, 'R') if winner == 'R' else (yellow_data, 'Y')


def generate_population(num_of_games, model=None):
    training_data = []
    for i in range(num_of_games):
        if i % (num_of_games/100) == 0:
            print(str(i/num_of_games*100) + "%")
        game_data, winner = play_data_game(model)
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

        mod_board_state = project_utilities.convert_board(board_state, winner)
        mod_training_data.append([mod_board_state, one_hot_slot])
    return mod_training_data        

def main(model_name=None, num_of_games=100000):
    if model_name is not None:
        model = network_module.neural_network_model(42, 7, project_utilities.LEARNING_RATE)
        model.load(model_name)
        training_data = prep_training_data(generate_population(num_of_games, model))
    else:
        training_data = prep_training_data(generate_population(num_of_games))
    training_data_save = np.array(training_data)
    
    date_time = datetime.now().strftime("%H-%M")
    if not os.path.exists("training_data"): os.mkdir("training_data")
    filename = 'training_data-' + date_time + '.npy'
    if model_name is not None:
        filename = model_name + '_' + filename
    np.save('training_data\\' + filename, training_data_save)
    
    print("Done! Number of Instances:" + str(training_data_save.size))

main('basic1')

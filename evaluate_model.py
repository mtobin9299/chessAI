import chip
import cfLogic
import network_module
import project_utilities
import numpy as np 
import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from random import randrange
from datetime import datetime
from statistics import mean

from chip import *


def play_random_turn(cf, team):
    while True:
        slot = cfLogic.chooseRandSlot(cf,team)
        if slot == -1: #board is full
            game_over = True
            break
        inserted = Chip(team)
        if(cf.addPiece(inserted,slot)):
            game_over = cf.checkForWin(inserted)[0]
            break
    return (cf, game_over)

#Add counter to measure number of times random is defaulted to
def play_model_turn(cf, team, model):
    converted_board = project_utilities.convert_board(cf.board, team)
    board_input = np.resize(converted_board, (1, len(converted_board[0]) * len(converted_board), 1))
    chosen_slot = np.argmax(model.predict(board_input)[0])
    played_chip = Chip(team)
    if not cf.addPiece(played_chip, chosen_slot):
        cf, game_over = play_random_turn(cf, team)
    else:
        game_over = cf.checkForWin(played_chip)[0]
    return cf, game_over

def play_model_game(player, opponent):
    cf = cfLogic.ConnectFour()
    game_over = False
    moves = 0
    priority = randrange(2)
    if priority == 0 :
        player_one = player
        player_two = opponent
        is_one = True
    else:
        player_one = opponent
        player_two = player
        is_one = False

    while not game_over:
        moves += 1
        #Player One (Red) Turn
        if player_one is not None:
            cf, game_over = play_model_turn(cf, 'R', player_one)
        else:
            cf, game_over = play_random_turn(cf, 'R')
        if game_over:
            winner = 1
            break
        #Player Two (Yellow) Turn
        if player_two is not None:
            cf, game_over = play_model_turn(cf, 'Y', player_two)
        else:
            cf, game_over = play_random_turn(cf, 'Y')
        if game_over: 
            winner = 2
            break

    if (is_one and winner == 1) or (not is_one and winner != 1):
        return (True, moves) 
    else:
        return (False, moves)

def evaluate(name, test_version, num_of_games):
    model_name = name + str(test_version)
    main_model = network_module.neural_network_model(42, 7, project_utilities.LEARNING_RATE)
    main_model.load(model_name, weights_only=True)
    results = []
    for version in range(test_version, -1, -1):
        print("Version " + str(test_version) + " vs. " + str(version))
        opponent_name = name + str(version)
        if version != 0:
            # opponent_model = network_module.neural_network_model(42, 7, project_utilities.LEARNING_RATE)
            # opponent_model.load(opponent_name, weights_only=True)
            opponent_model = main_model
        else:
            opponent_model = None
        num_of_wins = 0
        num_of_moves = []
        for i in range(num_of_games):
            if i % (num_of_games/10) == 0:
                print(str(i/num_of_games*100) + "%")
            
            won, moves = play_model_game(main_model, opponent_model)
            if won: 
                num_of_wins += 1
                num_of_moves.append(moves)
        average_moves = mean(num_of_moves)
        win_rate = num_of_wins / num_of_games
        results.append([version, win_rate, average_moves])
    return results
    

def main(model_name, version, num_of_games=50000):
    results = evaluate(model_name, version, num_of_games)
    print("Total games per match up: " + str(num_of_games))
    print(model_name + str(version))
    for result in results:
        version = result[0]
        win_rate = result[1]
        moves = result[2]
        print("Vs. version " + str(version) + " | Win Rate: " + str(win_rate) + " | Avg Moves: " + str(moves) + " |")


main('basic', 1)




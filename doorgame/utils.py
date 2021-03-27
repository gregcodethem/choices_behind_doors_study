from random import shuffle

from .all_dots import all_dots_list
from .easy_dots import easy_dots_list
from .four_by_four_dots import (
    four_by_four_dots_list_hard, 
    four_by_four_dots_list_medium,
    four_by_four_dots_list_easy
    )
from config.settings import TRIAL_LIMIT
from .models import MemoryGame, MemoryGameHigh


def memory_game_bool_matrix(dot_list):
        # if dots list shorter than trial limit
    # then repeat dots list until it gets to 61
    i = 0
    while len(dot_list) < 61:
        dot_list.append(dot_list[i % len(dot_list)])
        i = i + 1

    shuffle(dot_list)
    bool_list_matrix = []
    for pattern in dot_list:
        pattern_bool = []
        for square in pattern:
            if square == '0':
                pattern_bool.append(False)
            if square == '1':
                pattern_bool.append(True)
        bool_list_matrix.append(pattern_bool)
    return bool_list_matrix


def add_memory_games(MemoryGameList, dot_list="hard"):
    if dot_list == "hard":
        bool_matrix = memory_game_bool_matrix(all_dots_list)
    elif dot_list == "easy":
        bool_matrix = memory_game_bool_matrix(easy_dots_list)

    for i in range(0, TRIAL_LIMIT):
        _MemoryGame = MemoryGame()
        bool_list = bool_matrix[i]
        _MemoryGame.box_1 = bool_list[0]
        _MemoryGame.box_2 = bool_list[1]
        _MemoryGame.box_3 = bool_list[2]
        _MemoryGame.box_4 = bool_list[3]
        _MemoryGame.box_5 = bool_list[4]
        _MemoryGame.box_6 = bool_list[5]
        _MemoryGame.box_7 = bool_list[6]
        _MemoryGame.box_8 = bool_list[7]
        _MemoryGame.box_9 = bool_list[8]

        _MemoryGame.number_of_trial = i
        _MemoryGame.initial_or_final = 'initial'
        _MemoryGame.memory_game_list = MemoryGameList

        _MemoryGame.save()

def add_four_by_four_memory_games(MemoryGameList, dot_list):
    if dot_list == "very_hard":
        bool_matrix = memory_game_bool_matrix(four_by_four_dots_list_hard)
    elif dot_list == "medium":
        bool_matrix = memory_game_bool_matrix(four_by_four_dots_list_medium)
    elif dot_list == "very_easy":
        bool_matrix = memory_game_bool_matrix(four_by_four_dots_list_easy)

    for i in range(0, TRIAL_LIMIT):
        _MemoryGame = MemoryGameHigh()
        bool_list = bool_matrix[i]
        _MemoryGame.box_1 = bool_list[0]
        _MemoryGame.box_2 = bool_list[1]
        _MemoryGame.box_3 = bool_list[2]
        _MemoryGame.box_4 = bool_list[3]
        _MemoryGame.box_5 = bool_list[4]
        _MemoryGame.box_6 = bool_list[5]
        _MemoryGame.box_7 = bool_list[6]
        _MemoryGame.box_8 = bool_list[7]
        _MemoryGame.box_9 = bool_list[8]
        _MemoryGame.box_10 = bool_list[9]
        _MemoryGame.box_11 = bool_list[10]
        _MemoryGame.box_12 = bool_list[11]
        _MemoryGame.box_13 = bool_list[12]
        _MemoryGame.box_14 = bool_list[13]
        _MemoryGame.box_15 = bool_list[14]
        _MemoryGame.box_16 = bool_list[15]


        _MemoryGame.number_of_trial = i
        _MemoryGame.initial_or_final = 'initial'
        _MemoryGame.memory_game_list = MemoryGameList

        _MemoryGame.save()

def number_of_dots_correct_calculator(memory_game_one, memory_game_two):
    number_correct = 0
    if memory_game_one.box_1 == True:
        if memory_game_two.box_1 == True:
            number_correct += 1
    if memory_game_one.box_2 == True:
        if memory_game_two.box_2 == True:
            number_correct += 1
    if memory_game_one.box_3 == True:
        if memory_game_two.box_3 == True:
            number_correct += 1
    if memory_game_one.box_4 == True:
        if memory_game_two.box_4 == True:
            number_correct += 1
    if memory_game_one.box_5 == True:
        if memory_game_two.box_5 == True:
            number_correct += 1
    if memory_game_one.box_6 == True:
        if memory_game_two.box_6 == True:
            number_correct += 1
    if memory_game_one.box_7 == True:
        if memory_game_two.box_7 == True:
            number_correct += 1
    if memory_game_one.box_8 == True:
        if memory_game_two.box_8 == True:
            number_correct += 1
    if memory_game_one.box_9 == True:
        if memory_game_two.box_9 == True:
            number_correct += 1

    return number_correct

def number_of_dots_correct_calculator_four_by_four(memory_game_one, memory_game_two):
    number_correct = 0
    if memory_game_one.box_1 == True:
        if memory_game_two.box_1 == True:
            number_correct += 1
    if memory_game_one.box_2 == True:
        if memory_game_two.box_2 == True:
            number_correct += 1
    if memory_game_one.box_3 == True:
        if memory_game_two.box_3 == True:
            number_correct += 1
    if memory_game_one.box_4 == True:
        if memory_game_two.box_4 == True:
            number_correct += 1
    if memory_game_one.box_5 == True:
        if memory_game_two.box_5 == True:
            number_correct += 1
    if memory_game_one.box_6 == True:
        if memory_game_two.box_6 == True:
            number_correct += 1
    if memory_game_one.box_7 == True:
        if memory_game_two.box_7 == True:
            number_correct += 1
    if memory_game_one.box_8 == True:
        if memory_game_two.box_8 == True:
            number_correct += 1
    if memory_game_one.box_9 == True:
        if memory_game_two.box_9 == True:
            number_correct += 1
    if memory_game_one.box_10 == True:
        if memory_game_two.box_10 == True:
            number_correct += 1
    if memory_game_one.box_11 == True:
        if memory_game_two.box_11 == True:
            number_correct += 1
    if memory_game_one.box_12 == True:
        if memory_game_two.box_12 == True:
            number_correct += 1
    if memory_game_one.box_13 == True:
        if memory_game_two.box_13 == True:
            number_correct += 1
    if memory_game_one.box_14 == True:
        if memory_game_two.box_14 == True:
            number_correct += 1
    if memory_game_one.box_15 == True:
        if memory_game_two.box_15 == True:
            number_correct += 1
    if memory_game_one.box_15 == True:
        if memory_game_two.box_15 == True:
            number_correct += 1
    if memory_game_one.box_16 == True:
        if memory_game_two.box_16 == True:
            number_correct += 1

    return number_correct


def number_of_dots_selected_calculator(memory_game):
    total_selected = 0
    if memory_game.box_1 == True:
        total_selected += 1
    if memory_game.box_2 == True:
        total_selected += 1
    if memory_game.box_3 == True:
        total_selected += 1
    if memory_game.box_4 == True:
        total_selected += 1
    if memory_game.box_5 == True:
        total_selected += 1
    if memory_game.box_6 == True:
        total_selected += 1
    if memory_game.box_7 == True:
        total_selected += 1
    if memory_game.box_8 == True:
        total_selected += 1
    if memory_game.box_9 == True:
        total_selected += 1
    return total_selected


def number_of_dots_selected_calculator_four_by_four(memory_game):
    total_selected = 0
    if memory_game.box_1 == True:
        total_selected += 1
    if memory_game.box_2 == True:
        total_selected += 1
    if memory_game.box_3 == True:
        total_selected += 1
    if memory_game.box_4 == True:
        total_selected += 1
    if memory_game.box_5 == True:
        total_selected += 1
    if memory_game.box_6 == True:
        total_selected += 1
    if memory_game.box_7 == True:
        total_selected += 1
    if memory_game.box_8 == True:
        total_selected += 1
    if memory_game.box_9 == True:
        total_selected += 1
    if memory_game.box_10 == True:
        total_selected += 1
    if memory_game.box_11 == True:
        total_selected += 1
    if memory_game.box_12 == True:
        total_selected += 1
    if memory_game.box_13 == True:
        total_selected += 1
    if memory_game.box_14 == True:
        total_selected += 1
    if memory_game.box_15 == True:
        total_selected += 1
    if memory_game.box_16 == True:
        total_selected += 1
    return total_selected


def compare_two_memory_game_classes(MemoryGameOriginal, MemoryGameChosen):
    total_dots_in_original = number_of_dots_selected_calculator_four_by_four(MemoryGameOriginal)


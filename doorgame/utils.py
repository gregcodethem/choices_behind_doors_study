from random import shuffle

from .all_dots import all_dots_list
from config.settings import TRIAL_LIMIT
from .models import MemoryGame

def memory_game_bool_matrix(dot_list):
	shuffle(dot_list)
	bool_list_matrix = []
	for pattern in dot_list:
		pattern_bool = []
		for square in pattern:
			if square == 0:
				pattern_bool.append(False)
			if square == 1:
				pattern_bool.append(True)
		bool_list_matrix.append(pattern_bool)
	return bool_list_matrix


def add_memory_games(MemoryGameList):
    bool_matrix = memory_game_bool_matrix(all_dots_list)
    for i in range(0, TRIAL_LIMIT):
        MemoryGame = MemoryGame()
        bool_list = bool_matrix[i]
        MemoryGame.box_1 = bool_list[0]
        MemoryGame.box_2 = bool_list[1]
        MemoryGame.box_3 = bool_list[2]
        MemoryGame.box_4 = bool_list[3]
        MemoryGame.box_5 = bool_list[4]
        MemoryGame.box_6 = bool_list[5]
        MemoryGame.box_7 = bool_list[6]
        MemoryGame.box_8 = bool_list[7]
        MemoryGame.box_9 = bool_list[8]

        MemoryGame.number_of_trial = i
        MemoryGame.initial_or_final = initial
        MemoryGame.memory_game_list = MemoryGameList

        MemoryGame.save()
from doorgame.utils import memory_game_bool_matrix

from doorgame.all_dots import all_dots_list
from doorgame.easy_dots import easy_dots_list

from .test_views_base import BaseTest


class MemoryGameTest(BaseTest):

	def test_memory_game_bool_matrix_small_list(self):
		expanded_matrix = memory_game_bool_matrix(easy_dots_list)
		self.assertEqual(len(expanded_matrix), 61)
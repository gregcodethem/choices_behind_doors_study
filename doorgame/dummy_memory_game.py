
class MemoryGamePrelimClassNineByNine:

	def __init__(self, prelim_turn, easy_setting):
		if prelim_turn == 1:
			if easy_setting == "easy":
				self.box_1 = True
				self.box_2 = True
				self.box_3 = True
				self.box_4 = False
				self.box_5 = False
				self.box_6 = False
				self.box_7 = False
				self.box_8 = False
				self.box_9 = False
			if easy_setting == "hard":
				self.box_1 = True
				self.box_2 = False
				self.box_3 = True
				self.box_4 = True
				self.box_5 = False
				self.box_6 = False
				self.box_7 = False
				self.box_8 = False
				self.box_9 = True
		if prelim_turn == 2:
			if easy_setting == "easy":
				self.box_1 = False
				self.box_2 = False
				self.box_3 = False
				self.box_4 = True
				self.box_5 = True
				self.box_6 = True
				self.box_7 = False
				self.box_8 = False
				self.box_9 = False
			elif easy_setting == "hard":
				self.box_1 = False
				self.box_2 = True
				self.box_3 = False
				self.box_4 = True
				self.box_5 = False
				self.box_6 = True
				self.box_7 = False
				self.box_8 = False
				self.box_9 = True


class MemoryGamePrelimClass:

	def __init__(self, prelim_turn, very_hard_setting):
		if prelim_turn == 1:
			if very_hard_setting == "very_easy":
				self.box_1 = True
				self.box_2 = True
				self.box_3 = True
				self.box_4 = True
				self.box_5 = False
				self.box_6 = False
				self.box_7 = False
				self.box_8 = False
				self.box_9 = False
				self.box_10 = False
				self.box_11 = False
				self.box_12 = False
				self.box_13 = False
				self.box_14 = False
				self.box_15 = False
				self.box_16 = False
			if very_hard_setting == "medium":
				self.box_1 = True
				self.box_2 = True
				self.box_3 = False
				self.box_4 = False
				self.box_5 = False
				self.box_6 = False
				self.box_7 = False
				self.box_8 = True
				self.box_9 = False
				self.box_10 = False
				self.box_11 = False
				self.box_12 = False
				self.box_13 = False
				self.box_14 = True
				self.box_15 = False
				self.box_16 = False
			if very_hard_setting == "very_hard":
				self.box_1 = True
				self.box_2 = False
				self.box_3 = True
				self.box_4 = True
				self.box_5 = False
				self.box_6 = False
				self.box_7 = False
				self.box_8 = False
				self.box_9 = True
				self.box_10 = False
				self.box_11 = True
				self.box_12 = False
				self.box_13 = False
				self.box_14 = False
				self.box_15 = True
				self.box_16 = False
		if prelim_turn == 2:
			if very_hard_setting == "very_easy":
				self.box_1 = False
				self.box_2 = False
				self.box_3 = False
				self.box_4 = False
				self.box_5 = True
				self.box_6 = True
				self.box_7 = True
				self.box_8 = True
				self.box_9 = False
				self.box_10 = False
				self.box_11 = False
				self.box_12 = False
				self.box_13 = False
				self.box_14 = False
				self.box_15 = False
				self.box_16 = False
			elif very_hard_setting == "medium":
				self.box_1 = False
				self.box_2 = False
				self.box_3 = True
				self.box_4 = True
				self.box_5 = False
				self.box_6 = False
				self.box_7 = False
				self.box_8 = False
				self.box_9 = False
				self.box_10 = False
				self.box_11 = False
				self.box_12 = True
				self.box_13 = True
				self.box_14 = False
				self.box_15 = False
				self.box_16 = False
			elif very_hard_setting == "very_hard":
				self.box_1 = False
				self.box_2 = False
				self.box_3 = False
				self.box_4 = True
				self.box_5 = True
				self.box_6 = True
				self.box_7 = False
				self.box_8 = False
				self.box_9 = False
				self.box_10 = False
				self.box_11 = False
				self.box_12 = True
				self.box_13 = False
				self.box_14 = True
				self.box_15 = False
				self.box_16 = True

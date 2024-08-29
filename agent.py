import random
from constants import PLAYER_PIECE, AI_PIECE, EMPTY, WINDOW_LENGTH
import math
class Connect_4_AI:

	def __init__(self, game) -> None:
		self.game = game

	def get_move(self, board, my_piece, opp_piece):
		return random.choice(range(self.game.column_count))


class Min_Max_Agent(Connect_4_AI):
	def __init__(self, game) -> None:
		super().__init__(game)

	def _evaluate_window(self, window, piece):
		score = 0
		opp_piece = PLAYER_PIECE
		if piece == PLAYER_PIECE:
			opp_piece = AI_PIECE

		if window.count(piece) == 4:
			score += 100
		elif window.count(piece) == 3 and window.count(EMPTY) == 1:
			score += 5
		elif window.count(piece) == 2 and window.count(EMPTY) == 2:
			score += 2

		if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
			score -= 4

		return score
	def _score_position(self, board, piece):
		score = 0

		## Score center column
		center_array = [int(i) for i in list(board[:, self.game.column_count//2])]
		center_count = center_array.count(piece)
		score += center_count * 3

		## Score Horizontal
		for r in range(self.game.row_count):
			row_array = [int(i) for i in list(board[r,:])]
			for c in range(self.game.column_count-3):
				window = row_array[c:c+WINDOW_LENGTH]
				score += self._evaluate_window(window, piece)

		## Score Vertical
		for c in range(self.game.column_count):
			col_array = [int(i) for i in list(board[:,c])]
			for r in range(self.game.row_count-3):
				window = col_array[r:r+WINDOW_LENGTH]
				score += self._evaluate_window(window, piece)

		## Score posiive sloped diagonal
		for r in range(self.game.row_count-3):
			for c in range(self.game.column_count-3):
				window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
				score += self._evaluate_window(window, piece)

		for r in range(self.game.row_count-3):
			for c in range(self.game.column_count-3):
				window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
				score += self._evaluate_window(window, piece)

		return score
	
	def _is_terminal_node(self, board):
		return self.game.winning_move(board, PLAYER_PIECE) or self.game.winning_move(board,AI_PIECE) or len(self.game.get_valid_locations(board)) == 0
	def minimax(self, board, depth, alpha, beta, maximizingPlayer, my_piece, opp_piece):
		valid_locations = self.game.get_valid_locations(board)
		is_terminal = self._is_terminal_node(board)
		if depth == 0 or is_terminal:
			if is_terminal:
				if self.game.winning_move(board, my_piece):
					return (None, 100000000000000)
				elif self.game.winning_move(board, opp_piece):
					return (None, -10000000000000)
				else: # Game is over, no more valid moves
					return (None, 0)
			else: # Depth is zero
				return (None, self._score_position(board, my_piece))
		if maximizingPlayer:
			value = -math.inf
			column = random.choice(valid_locations)
			for col in valid_locations:
				row = self.game.get_next_open_row(board, col)
				b_copy = board.copy()
				self.game.drop_piece(b_copy, row, col, my_piece)
				new_score = self.minimax(b_copy, depth-1, alpha, beta, False, my_piece, opp_piece)[1]
				if new_score > value:
					value = new_score
					column = col
				alpha = max(alpha, value)
				if alpha >= beta:
					break
			return column, value

		else: # Minimizing player
			value = math.inf
			column = random.choice(valid_locations)
			for col in valid_locations:
				row = self.game.get_next_open_row(board, col)
				b_copy = board.copy()
				self.game.drop_piece(b_copy, row, col, opp_piece)
				new_score = self.minimax(b_copy, depth-1, alpha, beta, True, my_piece, opp_piece)[1]
				if new_score < value:
					value = new_score
					column = col
				beta = min(beta, value)
				if alpha >= beta:
					break
			return column, value
	
	def get_move(self, board, my_piece, opp_piece):
		col, _ = self.minimax(board, 5, -math.inf, math.inf, True, my_piece, opp_piece)
		return col


		



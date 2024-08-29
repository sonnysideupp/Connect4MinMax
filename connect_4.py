
import numpy as np
import pygame
import sys
import math
from constants import BLUE, BLACK, RADIUS, RED, SQUARESIZE, YELLOW, AI_PIECE, PLAYER_PIECE
from agent import Connect_4_AI, Min_Max_Agent
import random


class Connect4:
	

	def __init__(self, row = 6, column = 7, show_board = True) -> None:
		self.board = np.zeros((row,column)) 
		self.row_count = row
		self.column_count = column
		self.width = column * SQUARESIZE
		self.height = (row+1) * SQUARESIZE

		size = (self.width, self.height)
		self.show_board = show_board

		if self.show_board:
			pygame.init()
			self.screen = pygame.display.set_mode(size)
			self.draw_board()
			pygame.display.update()
			self.font = pygame.font.SysFont('arial', 75)

	def reset(self):
		self.board = np.zeros((self.row_count,self.column_count)) 
	def __repr__(self) -> str:
		return str(np.flip(self.board, 0))
	
	def drop_piece(self, board, row, col, piece):
		board[row][col] = piece

	
	def is_valid_location(self, board, col):
		return board[self.row_count-1][col] == 0
	

	def get_next_open_row(self, board, col):
		for r in range(self.row_count):
			if board[r][col] == 0:
				return r
	def winning_move(self, board, piece):
	# Check horizontal locations for win
		for c in range(self.column_count-3):
			for r in range(self.row_count):
				if board[r][c] == piece and self.board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
					return True

		# Check vertical locations for win
		for c in range(self.column_count):
			for r in range(self.row_count-3):
				if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
					return True

		# Check positively sloped diaganols
		for c in range(self.column_count-3):
			for r in range(self.row_count-3):
				if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
					return True

		# Check negatively sloped diaganols
		for c in range(self.column_count-3):
			for r in range(3, self.row_count):
				if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
					return True
	def draw_board(self):
		for c in range(self.column_count):
			for r in range(self.row_count):
				pygame.draw.rect(self.screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
				pygame.draw.circle(self.screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
		
		for c in range(self.column_count):
			for r in range(self.row_count):		
				if self.board[r][c] == 1:
					pygame.draw.circle(self.screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), self.height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
				elif self.board[r][c] == 2: 
					pygame.draw.circle(self.screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), self.height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
		pygame.display.update()
	# player connect 4 between 2 human players
	def play_game(self):
		game_over = False
		turn = 0
		while not game_over:
 
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
		
				if event.type == pygame.MOUSEMOTION:
					pygame.draw.rect(self.screen, BLACK, (0,0, self.width, SQUARESIZE))
					posx = event.pos[0]
					if turn == 0:
						pygame.draw.circle(self.screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
					else: 
						pygame.draw.circle(self.screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
				pygame.display.update()
		
				if event.type == pygame.MOUSEBUTTONDOWN:
					pygame.draw.rect(self.screen, BLACK, (0,0, self.width, SQUARESIZE))
					#print(event.pos)
					# Ask for Player 1 Input
					if turn == 0:
						posx = event.pos[0]
						col = int(math.floor(posx/SQUARESIZE))
		
						if self.is_valid_location(self.board, col):
							row = self.get_next_open_row(self.board, col)
							self.drop_piece(self.board, row, col, 1)
		
							if self.winning_move(self.board, 1):
								label = self.font.render("Player 1 wins!!", 1, RED)
								self.screen.blit(label, (40,10))
								game_over = True
		
		
					# # Ask for Player 2 Input
					else:               
						posx = event.pos[0]
						col = int(math.floor(posx/SQUARESIZE))
		
						if self.is_valid_location(self.board, col):
							row = self.get_next_open_row(self.board, col)
							self.drop_piece(self.board, row, col, 2)
		
							if self.winning_move(self.board, 2):
								label = self.font.render("Player 2 wins!!", 1, YELLOW)
								self.screen.blit(label, (40,10))
								game_over = True
		
					# print(self)
					self.draw_board()
		
					turn += 1
					turn = turn % 2
		
					if game_over:
						pygame.time.wait(3000)
	## play connect 4 with an ai agent
	def play_game_with_ai(self, agent: Connect_4_AI):
		game_over = False
		turn = random.randint(PLAYER_PIECE, AI_PIECE)
		while not game_over:

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

				if event.type == pygame.MOUSEMOTION:
					pygame.draw.rect(self.screen, BLACK, (0,0, self.width, SQUARESIZE))
					posx = event.pos[0]
					if turn == PLAYER_PIECE:
						pygame.draw.circle(self.screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)

				pygame.display.update()

				if event.type == pygame.MOUSEBUTTONDOWN:
					pygame.draw.rect(self.screen, BLACK, (0,0, self.width, SQUARESIZE))
					#print(event.pos)
					# Ask for Player 1 Input
					if turn == PLAYER_PIECE:
						posx = event.pos[0]
						col = int(math.floor(posx/SQUARESIZE))

						game_over = self.play_move_helper(col, PLAYER_PIECE)

							
						turn = AI_PIECE

							# print(self)
						self.draw_board()


			# # Ask for Player 2 Input
			if turn == AI_PIECE and not game_over:				

				#col = random.randint(0, COLUMN_COUNT-1)
				#col = pick_best_move(board, AI_PIECE)
				col = agent.get_move(self.board, AI_PIECE, PLAYER_PIECE)

				game_over = self.play_move_helper(col, AI_PIECE)

					# print(self)
				self.draw_board()

					
				turn = PLAYER_PIECE

			if game_over:
				pygame.time.wait(3000)

	def play_move_helper(self, move, piece, ):
		if self.is_valid_location(self.board, move):
			#pygame.time.wait(500)
			row = self.get_next_open_row(self.board, move)
			self.drop_piece(self.board, row, move, piece)

			if self.winning_move(self.board, piece):
				if self.show_board:
					label = self.font.render(f"Player {piece} wins!!", 1, YELLOW)
					self.screen.blit(label, (40,10))
				
				return True
		return False
	## simulate a connect 4 between two ai agents
	def play_game_ai_vs_ai(self, agent_1: Connect_4_AI, agent_2: Connect_4_AI):
		game_over = False
		turn = PLAYER_PIECE
		while not game_over:

			if turn == PLAYER_PIECE and not game_over:				

				#col = random.randint(0, COLUMN_COUNT-1)
				#col = pick_best_move(board, AI_PIECE)
				col = agent_1.get_move(self.board, PLAYER_PIECE, AI_PIECE)

				over = self.play_move_helper(col, PLAYER_PIECE)
						
				if over: return PLAYER_PIECE

					# print(self)
				if self.show_board:
					self.draw_board()
					pygame.display.update()
					pygame.time.wait(1000)
					# pygame.time.wait(1000)

					
				turn = AI_PIECE
			if turn == AI_PIECE and not game_over:				

				#col = random.randint(0, COLUMN_COUNT-1)
				#col = pick_best_move(board, AI_PIECE)
				col = agent_2.get_move(self.board, AI_PIECE, PLAYER_PIECE)

				over = self.play_move_helper(col, AI_PIECE)
				if over: return AI_PIECE

					# print(self)
				if self.show_board:
					self.draw_board()
					pygame.display.update()
					# pygame.time.wait(1000)
					
				turn = PLAYER_PIECE

			if game_over:
				pygame.time.wait(3000)
 

	def get_valid_locations(self, board):
		valid_locations = []
		for col in range(self.column_count):
			if self.is_valid_location(board, col):
				valid_locations.append(col)
		return valid_locations
	
	def play_step(self, action):
		# 1. collect user input
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		
		# 2. move
		self._move(action) # update the head
		self.snake.insert(0, self.head)
		
		# 3. check if game over
		reward = 0
		game_over = False
		if self.is_collision() or self.frame_iteration > 100*len(self.snake):
			game_over = True
			reward = -10
			return reward, game_over, self.score

		# 4. place new food or just move
		if self.head == self.food:
			self.score += 1
			reward = 10
			self._place_food()
		else:
			self.snake.pop()
		
		# 5. update ui and clock
		self._update_ui()
		self.clock.tick(SPEED)
		# 6. return game over and score
		return reward, game_over, self.score
def main():
	connect_4 = Connect4()
	connect_4.play_game_with_ai(Min_Max_Agent(connect_4))
	# connect_4.play_game_ai_vs_ai(Min_Max_Agent(connect_4), Min_Max_Agent(connect_4))


if __name__ == '__main__':
	main()
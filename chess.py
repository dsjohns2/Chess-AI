from __future__ import print_function
import copy
import random
from colorama import Fore
import time
import sys

class square:
	def __init__(self, color, piece, occupied):
		self.is_occupied = occupied 
		self.color = color
		self.piece = piece

class game:
	def __init__(self, weights):
		self.board = [[square("b", "R", True), square("b", "N", True), square("b", "B", True), square("b", "Q", True), square("b", "K", True), square("b", "B", True), square("b", "N", True), square("b", "R", True)], 
					  [square("b", "P", True), square("b", "P", True), square("b", "P", True), square("b", "P", True), square("b", "P", True), square("b", "P", True), square("b", "P", True), square("b", "P", True)], 
					  [square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False)], 
					  [square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False)], 
					  [square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False)], 
					  [square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False)], 
					  [square("w", "P", True), square("w", "P", True), square("w", "P", True), square("w", "P", True), square("w", "P", True), square("w", "P", True), square("w", "P", True), square("w", "P", True)], 
					  [square("w", "R", True), square("w", "N", True), square("w", "B", True), square("w", "Q", True), square("w", "K", True), square("w", "B", True), square("w", "N", True), square("w", "R", True)]] 
		self.white_turn = True
		self.turns_since_capture_or_pawn_movement = 0
		self.pieces = 32
		self.weights = weights
		self.board_history = []
		self.training_set = []

	def make_move(self, human_flag):
		"""
		returns -1 if game is still in progess
				0 if game is a tie
				1 if white wins
				2 if black wins
		"""
		self.board_history.append(self.board)
		if(self.white_turn):
			legal_moves = self.get_legal_moves(self.board, "w")
		else:
			legal_moves = self.get_legal_moves(self.board, "b")

		#Check for End of Game
		game_is_over = self.game_is_over(self.board, legal_moves, self.white_turn)
		if(not (game_is_over == -1)):
			return game_is_over
		#Game Continues
		else:
			if(self.white_turn):
				random_flag = False
			else:
				random_flag = True
			move = self.pick_move(legal_moves, human_flag, random_flag)
			self.upgrade_pawns(move)
			self.board = move
			self.board = self.check_for_stalemate(self.board)
			self.white_turn = not self.white_turn
			return -1

	def game_is_over(self, board, legal_moves, white_turn):
		"""
		returns -1 if game is still in progess
				0 if game is a tie
				1 if white wins
				2 if black wins
		"""
		#Check for End of Game
		if(len(legal_moves) == 0):
			if(white_turn):
				king_color = "w"
				opposite_color = "b"
			else:
				king_color = "b"
				opposite_color = "b"

			for i in range(0, 8):
				for j in range(0, 8):
					if(board[i][j].piece == "K" and board[i][j].color == king_color):
						king_i = i
						king_j = j
			danger_squares = []
			for i in range(0, 8):
				for j in range(0, 8):
					danger_squares += self.squares_that_piece_at_i_j_can_take(board, i, j, opposite_color)
			checkmate_flag = False
			for danger_square in danger_squares:
				if(danger_square[0] == king_i and danger_square[1] == king_j):
					checkmate_flag = True

			if(checkmate_flag):
				if(white_turn):
					return 2
				else:
					return 1
			else:
				return 0
		else:
			num_pieces = 0
			for i in range(0, 8):
				for j in range(0, 8):
					if(board[i][j].is_occupied):
						num_pieces += 1
			if(num_pieces == 2):
				return 0
			else:
				return -1

	def check_for_stalemate(self, board):
		#stalemate for 50 move rule
		stalemate_flag = False
		pieces = 0
		for i in range(0, 8):
			for j in range(0, 8):
				if(board[i][j].is_occupied):
					pieces += 1

		if(self.pieces == pieces):
			self.turns_since_capture_or_pawn_movement += 1
		else:
			self.pieces = pieces
			self.turns_since_capture_or_pawn_movement = 0

		if(self.turns_since_capture_or_pawn_movement >= 100): #TODO: change back to 50
			stalemate_board = [[square("b", "K", True), square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False)], 
							  [square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False)], 
							  [square("", "", False), square("w", "K", True), square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False)], 
							  [square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False)], 
							  [square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False)], 
							  [square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False)], 
							  [square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False)], 
							  [square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False)]] 
			return stalemate_board
		else:
			return board
	
	def upgrade_pawns(self, board):
		for i in range(0, 8):
			for j in range(0, 8):
				if(board[i][j].is_occupied and board[i][j].piece == "P" and i == 0):
					board[i][j].piece = "Q"
				if(board[i][j].is_occupied and board[i][j].piece == "P" and i == 7):
					board[i][j].piece = "Q"

	def remove_moves_resulting_in_check(self, moves, king_color):
		legal_moves = [] 
		if(king_color == "w"):
			opposite_color = "b"
		else:
			opposite_color = "w"

		for move in moves:
			for i in range(0, 8):
				for j in range(0, 8):
					if(move[i][j].piece == "K" and move[i][j].color == king_color):
						king_i = i
						king_j = j
			danger_squares = []
			for i in range(0, 8):
				for j in range(0, 8):
					danger_squares += self.squares_that_piece_at_i_j_can_take(move, i, j, opposite_color)
			add_flag = True
			for danger_square in danger_squares:
				if(danger_square[0] == king_i and danger_square[1] == king_j):
					add_flag = False
			if(add_flag):
				legal_moves.append(move)
		return legal_moves

	def remove_piece(self, i, j, board):
		board[i][j].is_occupied = False
		board[i][j].color = ""
		board[i][j].piece = ""

	def add_piece(self, i, j, piece, color, board):
		board[i][j].is_occupied = True
		board[i][j].color = color
		board[i][j].piece = piece

	def white_pawn(self, board, i, j):
		"""
		board = current board state
		i,j = position of piece
		return array of (i,j) positions that piece can legally reach/take
		"""
		squares = []
		#move forward one
		if(i-1 >= 0 and not board[i-1][j].is_occupied):
			squares.append([i-1, j])
		#move forward two
		if(i==6 and not board[i-1][j].is_occupied and not board[i-2][j].is_occupied):
			squares.append([i-2, j])
		#take piece left
		if(i-1 >= 0 and j-1 >= 0 and board[i-1][j-1].is_occupied and board[i-1][j-1].color == "b"):
			squares.append([i-1, j-1])
		#take piece right
		if(i-1 >= 0 and j+1 <= 7 and board[i-1][j+1].is_occupied and board[i-1][j+1].color == "b"):
			squares.append([i-1, j+1])
		return squares
	
	def black_pawn(self, board, i, j):
		"""
		board = current board state
		i,j = position of piece
		return array of (i,j) positions that piece can legally reach/take
		"""
		squares = []
		#move forward one
		if(i+1 <= 7 and not board[i+1][j].is_occupied):
			squares.append([i+1, j])
		#move forward two
		if(i==1 and not board[i+1][j].is_occupied and not board[i+2][j].is_occupied):
			squares.append([i+2, j])
		#take piece left
		if(i+1 <= 7 and j-1 >= 0 and board[i+1][j-1].is_occupied and board[i+1][j-1].color == "w"):
			squares.append([i+1, j-1])
		#take piece right
		if(i+1 <= 7 and j+1 <= 7 and board[i+1][j+1].is_occupied and board[i+1][j+1].color == "w"):
			squares.append([i+1, j+1])
		return squares
	
	def knight(self, board, i, j):
		"""
		board = current board state
		i,j = position of piece
		return array of (i,j) positions that piece can legally reach/take
		"""
		squares = []
		if(i-1 >= 0 and j-2 >= 0 and not board[i-1][j-2].color == board[i][j].color):
			squares.append([i-1, j-2])
		if(i-2 >= 0 and j-1 >= 0 and not board[i-2][j-1].color == board[i][j].color):
			squares.append([i-2, j-1])
		if(i-1 >= 0 and j+2 <= 7 and not board[i-1][j+2].color == board[i][j].color):
			squares.append([i-1, j+2])
		if(i-2 >= 0 and j+1 <= 7 and not board[i-2][j+1].color == board[i][j].color):
			squares.append([i-2, j+1])
		if(i+1 <= 7 and j-2 >= 0 and not board[i+1][j-2].color == board[i][j].color):
			squares.append([i+1, j-2])
		if(i+2 <= 7 and j-1 >= 0 and not board[i+2][j-1].color == board[i][j].color):
			squares.append([i+2, j-1])
		if(i+1 <= 7 and j+2 <= 7 and not board[i+1][j+2].color == board[i][j].color):
			squares.append([i+1, j+2])
		if(i+2 <= 7 and j+1 <= 7 and not board[i+2][j+1].color == board[i][j].color):
			squares.append([i+2, j+1])
		return squares

	def bishop(self, board, i, j):
		"""
		board = current board state
		i,j = position of piece
		return array of (i,j) positions that piece can legally reach/take
		"""
		squares = []
		#Up-Left diagonal
		x = i-1
		y = j-1
		while(x >= 0 and y >= 0):
			if(board[x][y].is_occupied):
				if(not board[x][y].color == board[i][j].color):
					squares.append([x, y])
				break
			else:
				squares.append([x, y])
				x -= 1
				y -= 1
		#Up-Right diagonal
		x = i-1
		y = j+1
		while(x >= 0 and y <= 7):
			if(board[x][y].is_occupied):
				if(not board[x][y].color == board[i][j].color):
					squares.append([x, y])
				break
			else:
				squares.append([x, y])
				x -= 1
				y += 1
		#Down-Left diagonal
		x = i+1
		y = j-1
		while(x <= 7 and y >= 0):
			if(board[x][y].is_occupied):
				if(not board[x][y].color == board[i][j].color):
					squares.append([x, y])
				break
			else:
				squares.append([x, y])
				x += 1
				y -= 1
		#Down-Right diagonal
		x = i+1
		y = j+1
		while(x <= 7 and y <= 7):
			if(board[x][y].is_occupied):
				if(not board[x][y].color == board[i][j].color):
					squares.append([x, y])
				break
			else:
				squares.append([x, y])
				x += 1
				y += 1

		return squares

	def rook(self, board, i, j):
		"""
		board = current board state
		i,j = position of piece
		return array of (i,j) positions that piece can legally reach/take
		"""
		squares = []
		#Up
		x = i-1
		y = j
		while(x >= 0):
			if(board[x][y].is_occupied):
				if(not board[x][y].color == board[i][j].color):
					squares.append([x, y])
				break
			else:
				squares.append([x, y])
				x -= 1
		#Right
		x = i
		y = j+1
		while(y <= 7):
			if(board[x][y].is_occupied):
				if(not board[x][y].color == board[i][j].color):
					squares.append([x, y])
				break
			else:
				squares.append([x, y])
				y += 1
		#Left
		x = i
		y = j-1
		while(y >= 0):
			if(board[x][y].is_occupied):
				if(not board[x][y].color == board[i][j].color):
					squares.append([x, y])
				break
			else:
				squares.append([x, y])
				y -= 1
		#Down
		x = i+1
		y = j
		while(x <= 7):
			if(board[x][y].is_occupied):
				if(not board[x][y].color == board[i][j].color):
					squares.append([x, y])
				break
			else:
				squares.append([x, y])
				x += 1

		return squares

	def king(self, board, i, j):
		"""
		board = current board state
		i,j = position of piece
		return array of (i,j) positions that piece can legally reach/take
		"""
		squares = []
		if(i-1 >= 0 and j-1 >= 0 and not board[i-1][j-1].color == board[i][j].color):	
			squares.append([i-1, j-1])
		if(i-1 >= 0 and j+1 <= 7 and not board[i-1][j+1].color == board[i][j].color):	
			squares.append([i-1, j+1])
		if(i+1 <= 7 and j-1 >= 0 and not board[i+1][j-1].color == board[i][j].color):
			squares.append([i+1, j-1])
		if(i+1 <= 7 and j+1 <= 7 and not board[i+1][j+1].color == board[i][j].color):	
			squares.append([i+1, j+1])
		if(i-1 >= 0 and not board[i-1][j].color == board[i][j].color):	
			squares.append([i-1, j])
		if(i+1 <= 7 and not board[i+1][j].color == board[i][j].color):	
			squares.append([i+1, j])
		if(j-1 >= 0 and not board[i][j-1].color == board[i][j].color):	
			squares.append([i, j-1])
		if(j+1 <= 7 and not board[i][j+1].color == board[i][j].color):	
			squares.append([i, j+1])
		return squares


	def squares_that_piece_at_i_j_can_take(self, board, i, j, color):
		#White Pawn
		if(board[i][j].is_occupied and board[i][j].color == "w" and board[i][j].piece == "P"):
			squares = self.white_pawn(board, i, j)
		#Black Pawn
		elif(board[i][j].is_occupied and board[i][j].color == "b" and board[i][j].piece == "P"):
			squares = self.black_pawn(board, i, j)
		#Knight
		elif(board[i][j].is_occupied and board[i][j].color == color and board[i][j].piece == "N"):
			squares = self.knight(board, i, j)
		#Bishop
		elif(board[i][j].is_occupied and board[i][j].color == color and board[i][j].piece == "B"):
			squares = self.bishop(board, i, j)
		#Rook
		elif(board[i][j].is_occupied and board[i][j].color == color and board[i][j].piece == "R"):
			squares = self.rook(board, i, j)
		#Queen
		elif(board[i][j].is_occupied and board[i][j].color == color and board[i][j].piece == "Q"):
			squares = self.bishop(board, i, j)
			squares += self.rook(board, i, j)
		#King
		elif(board[i][j].is_occupied and board[i][j].color == color and board[i][j].piece == "K"):
			squares = self.king(board, i, j)
		else:
			squares = []
		return squares

	def get_legal_moves(self, board, color):
		legal_moves = []
		for i in range(0, 8):
			for j in range(0, 8):
				if(board[i][j].color == color):
					#get legal squares at i j for color
					squares = self.squares_that_piece_at_i_j_can_take(board, i, j, color)
					for elem in squares:
						new_board = copy.deepcopy(board)
						self.remove_piece(i, j, new_board)
						self.add_piece(elem[0], elem[1], board[i][j].piece, board[i][j].color, new_board)
						legal_moves.append(new_board)
		legal_moves = self.remove_moves_resulting_in_check(legal_moves, color)
		return legal_moves

	def pick_move(self, legal_moves, human_flag, random_flag):
		if(human_flag):
			while(True):
				human_move = ""
				if(self.white_turn):
					human_color = "w"
				else:
					human_color = "b"
				while(not len(human_move) == 3):
					human_move = raw_input("Type your move: ")
					piece = human_move[0]
					column = human_move[1]
					row = int(human_move[2])
				if(column == "a"):
					j = 0
				elif(column == "b"):
					j = 1
				elif(column == "c"):
					j = 2
				elif(column == "d"):
					j = 3
				elif(column == "e"):
					j = 4
				elif(column == "f"):
					j = 5
				elif(column == "g"):
					j = 6
				else:
					j = 7
				i = 8-row

				candidate_moves = []
				for k in range(0, len(legal_moves)):
					move = legal_moves[k]
					if(move[i][j].piece == piece and move[i][j].color == human_color):
						candidate_moves.append(legal_moves[k])

				if(len(candidate_moves) == 1):
					return candidate_moves[0]
				elif(len(candidate_moves) > 1):
					print("Enter the number of the move you wanted: ")
					for idx in range(0, len(candidate_moves)):
						print(idx)
						self.print_board(candidate_moves[idx], True)
					return candidate_moves[int(raw_input("Number: "))]
				else:
					print("Invalid move")

		elif(random_flag):
			return legal_moves[random.randrange(0, len(legal_moves))]
		else:
			#use learned function
			move_values = []
			for move in legal_moves:
				cur_value = self.lin_fun(move)
				move_values.append(cur_value)

			best_idx = random.randrange(0, len(legal_moves))
			best_val = move_values[best_idx]
			for i in range(0, len(move_values)):
				if(move_values[i]>best_val):
					best_val = move_values[i]
					best_idx = i
			if(len(self.board_history) > 5 and legal_moves[best_idx] == self.board_history[-4]):
				#exit move loop
				return legal_moves[random.randrange(0, len(legal_moves))]
			else:
				return legal_moves[best_idx]

	def lin_fun(self, board):
		x = self.get_x(board)
		ret_val = 0
		for i in range(0, len(self.weights)):
			ret_val += self.weights[i] * x[i]
		return ret_val

	def get_x(self, board):
		#x[0] = num white points on board
		#x[1] = num black points on board
		#x[2] = white legal moves
		#x[3] = black legal moves
		#x[4] = white center pawn points
		#x[5] = black center pawn points
		#x[6] = white center knight points
		#x[7] = black center knight points
		#x[8] = white center bishop points
		#x[9] = black center bishop points
		#x[10] = white center rook points
		#x[11] = black center rook points
		#x[12] = white center queen points
		#x[13] = black center queen points
		#x[14] = white center king points
		#x[15] = black center king points
		#x[16] = white pawn threatened level
		#x[17] = black pawn threatened level
		#x[18] = white knight threatened level
		#x[19] = black knight threatened level
		#x[20] = white bishop threatened level
		#x[21] = black bishop threatened level
		#x[22] = white rook threatened level
		#x[23] = black rook threatened level
		#x[24] = white queen threatened level
		#x[25] = black queen threatened level
		#x[26] = white king threatened level
		#x[27] = black king threatened level
		#x[] = white coverage points
		#x[] = black coverage points
		x = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		for i in range(0, 8):
			for j in range(0, 8):
				#begin points
				if(board[i][j].piece == "P"):
					points = 1
				elif(board[i][j].piece == "N"):
					points = 3
				elif(board[i][j].piece == "B"):
					points = 3
				elif(board[i][j].piece == "R"):
					points = 5
				elif(board[i][j].piece == "Q"):
					points = 9
				else:
					points = 0
				if(board[i][j].color == "w"):
					x[0] += points
				else:
					x[1] += points
				#end points
				#begin legal moves
				if(board[i][j].color == "w"):
					legal_moves = []#self.get_legal_moves(board, "w")
					x[2] += len(legal_moves)
				elif(board[i][j].color == "b"):
					legal_moves = []#self.get_legal_moves(board, "b")
					x[3] += len(legal_moves)
				#end legal moves
				#begin center points
				center_points = 0
				if(i == 0):
					center_points += 1
				elif(i == 1):
					center_points += 2
				elif(i == 2):
					center_points += 3
				elif(i == 3):
					center_points += 4
				elif(i == 4):
					center_points += 4
				elif(i == 5):
					center_points += 3
				elif(i == 6):
					center_points += 2
				else:
					center_points += 1

				if(j == 0):
					center_points += 1
				elif(j == 1):
					center_points += 2
				elif(j == 2):
					center_points += 3
				elif(j == 3):
					center_points += 4
				elif(j == 4):
					center_points += 4
				elif(j == 5):
					center_points += 3
				elif(j == 6):
					center_points += 2
				else:
					center_points += 1

				if(board[i][j].color == "w"):
					if(board[i][j].piece == "P"):
						x[4] += center_points
					elif(board[i][j].piece == "N"):
						x[6] += center_points
					elif(board[i][j].piece == "B"):
						x[8] += center_points
					elif(board[i][j].piece == "R"):
						x[10] += center_points
					elif(board[i][j].piece == "Q"):
						x[12] += center_points
					elif(board[i][j].piece == "K"):
						x[14] += center_points
				elif(board[i][j].color == "b"):
					if(board[i][j].piece == "P"):
						x[5] += center_points
					elif(board[i][j].piece == "N"):
						x[7] += center_points
					elif(board[i][j].piece == "B"):
						x[9] += center_points
					elif(board[i][j].piece == "R"):
						x[11] += center_points
					elif(board[i][j].piece == "Q"):
						x[13] += center_points
					elif(board[i][j].piece == "K"):
						x[15] += center_points
				#end center points
				#begin threatened level
				if(board[i][j].color == "w"):
					squares = self.squares_that_piece_at_i_j_can_take(board, i, j, "w")
					for square in squares:
						if(board[square[0]][square[1]].piece == "P"):
							x[17] += 1
						if(board[square[0]][square[1]].piece == "N"):
							x[19] += 1
						if(board[square[0]][square[1]].piece == "B"):
							x[21] += 1
						if(board[square[0]][square[1]].piece == "R"):
							x[23] += 1
						if(board[square[0]][square[1]].piece == "Q"):
							x[25] += 1
						if(board[square[0]][square[1]].piece == "K"):
							x[27] += 1
				elif(board[i][j].color == "b"):
					squares = self.squares_that_piece_at_i_j_can_take(board, i, j, "b")
					for square in squares:
						if(board[square[0]][square[1]].piece == "P"):
							x[16] += 1
						if(board[square[0]][square[1]].piece == "N"):
							x[18] += 1
						if(board[square[0]][square[1]].piece == "B"):
							x[20] += 1
						if(board[square[0]][square[1]].piece == "R"):
							x[22] += 1
						if(board[square[0]][square[1]].piece == "Q"):
							x[24] += 1
						if(board[square[0]][square[1]].piece == "K"):
							x[26] += 1
				#end threatened level
		return x

	def print_board(self, board, upside_down_flag):
		print(Fore.WHITE + "~~~~~~~~~~~~~~~~~")
		if(not upside_down_flag):
			for i in range(0, len(board)):
				for j in board[i]:
					if(j.color == "b"):
						print(Fore.WHITE + "|", end='')
						print(Fore.BLUE + j.piece, end='')
					elif(j.color == "w"):
						print(Fore.WHITE + "|", end='')
						print(Fore.GREEN + j.piece, end='')
					else:
						print(Fore.WHITE + "| ", end='')
				print(Fore.WHITE + "|" + str(8-i))
				print(Fore.WHITE + "~~~~~~~~~~~~~~~~~")
			print(Fore.WHITE + " a b c d e f g h ")
			print("")
		else:
			for i in [7, 6, 5, 4, 3, 2, 1, 0]:
				for k in [7, 6, 5, 4, 3, 2, 1, 0]:
					j = board[i][k]
					if(j.color == "b"):
						print(Fore.WHITE + "|", end='')
						print(Fore.BLUE + j.piece, end='')
					elif(j.color == "w"):
						print(Fore.WHITE + "|", end='')
						print(Fore.GREEN + j.piece, end='')
					else:
						print(Fore.WHITE + "| ", end='')
				print(Fore.WHITE + "|" + str(8-i))
				print(Fore.WHITE + "~~~~~~~~~~~~~~~~~")
			print(Fore.WHITE + " h g f e d c b a ")
			print("")

	def human_move(self):
		return self.make_move(True)

	def computer_move(self):
		return self.make_move(False)

	def play_game(self):
		game_is_over = -1
		while(game_is_over == -1):
			game_is_over = self.computer_move()
			#print(game_is_over)
			#self.print_board(self.board, False)
		return game_is_over

	def play_human_game(self):
		game_is_over = -1
		self.print_board(self.board, True)
		while(game_is_over == -1):
			time.sleep(1)
			if(self.white_turn):
				game_is_over = self.computer_move()
			else:
				game_is_over = self.human_move()
			self.print_board(self.board, True)
			
		return game_is_over

	def create_training_set(self):
		for i in range(0, len(self.board_history)):
			if(i % 2 == 0):
				state = self.board_history[i]
				legal_moves = self.get_legal_moves(state, "w")
				if(self.game_is_over(state, legal_moves, True) == 1):
					self.training_set.append([state, 100])
				if(self.game_is_over(state, legal_moves, True) == 2):
					self.training_set.append([state, -100])
				if(self.game_is_over(state, legal_moves, True) == 0):
					self.training_set.append([state, 0])
				if(self.game_is_over(state, legal_moves, True) == -1):
					if(i+2<len(self.board_history)):
						self.training_set.append([state, self.lin_fun(self.board_history[i+2])])
					else:
						next_state = self.board_history[i+1]
						next_state_legal_moves = self.get_legal_moves(state, "b")
						if(self.game_is_over(next_state, next_state_legal_moves, False) == 2):
							self.training_set.append([state, -100])
						else:
							self.training_set.append([state, 0])

	def shift_weights(self):
		change_constant = 0.00001
		for elem in self.training_set:
			x = self.get_x(elem[0])
			for j in range(0, len(self.weights)):
				add_to_weight = change_constant * (elem[1] - self.lin_fun(elem[0])) * x[j]
				self.weights[j] += add_to_weight

#TODO:add reading and writing weights to file
#x[0] = num white points on board
#x[1] = num black points on board
#x[2] = white legal moves
#x[3] = black legal moves
#x[4] = white center pawn points
#x[5] = black center pawn points
#x[6] = white center knight points
#x[7] = black center knight points
#x[8] = white center bishop points
#x[9] = black center bishop points
#x[10] = white center rook points
#x[11] = black center rook points
#x[12] = white center queen points
#x[13] = black center queen points
#x[14] = white center king points
#x[15] = black center king points
#x[16] = white pawn threatened level
#x[17] = black pawn threatened level
#x[18] = white knight threatened level
#x[19] = black knight threatened level
#x[20] = white bishop threatened level
#x[21] = black bishop threatened level
#x[22] = white rook threatened level
#x[23] = black rook threatened level
#x[24] = white queen threatened level
#x[25] = black queen threatened level
#x[26] = white king threatened level
#x[27] = black king threatened level

#get weights
weights_file = open("weights.txt", "r")
weights_str = weights_file.readline()
weights_str_arr = weights_str.split()
weights = []
for s in weights_str_arr:
	weights.append(float(s))
weights_file.close()

#train
for i in range(0, 0):
	print(weights)
	my_game = game(weights)
	my_game.play_game()
	my_game.create_training_set()
	my_game.shift_weights()
	weights = my_game.weights
	weights_file = open("weights.txt", "w")
	for w in weights:
		weights_file.write(str(w) + " ")
	weights_file.close()
print(weights)

#play random
white_wins = 0
black_wins = 0
draws = 0
for i in range(0, 0):
	my_game = game(weights)
	result = my_game.play_game()
	if(result == 0):
		draws += 1
	elif(result == 1):
		white_wins += 1
	elif(result == 2):
		black_wins += 1
print("white wins: ", white_wins)
print("black wins: ", black_wins)
print("draws: ", draws)

#play human
while(True):
	my_game = game(weights)
	result = my_game.play_human_game()
	if(result == 0):
		print("Draw")
	elif(result == 1):
		print("White Wins")
	elif(result == 2):
		print("Black Wins")

#TODO:
	##fine tune human moves
	##Castleing
	##enpasant
	##ml
		###how many white pieces cover other white pieces
		###points
		###num pieces
		###num available moves
		###num pieces

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
	def __init__(self):
		self.board = [[square("b", "R", True), square("b", "N", True), square("b", "B", True), square("b", "Q", True), square("b", "K", True), square("b", "B", True), square("b", "N", True), square("b", "R", True)], 
					  [square("b", "P", True), square("b", "P", True), square("b", "P", True), square("b", "P", True), square("b", "P", True), square("b", "P", True), square("b", "P", True), square("b", "P", True)], 
					  [square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False)], 
					  [square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False)], 
					  [square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False)], 
					  [square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False), square("", "", False)], 
					  [square("w", "P", True), square("w", "P", True), square("w", "P", True), square("w", "P", True), square("w", "P", True), square("w", "P", True), square("w", "P", True), square("w", "P", True)], 
					  [square("w", "R", True), square("w", "N", True), square("w", "B", True), square("w", "Q", True), square("w", "K", True), square("w", "B", True), square("w", "N", True), square("w", "R", True)]] 
		self.white_turn = True

	def make_move(self):
		if(self.white_turn):
			legal_moves = self.get_legal_moves(self.board, "w")
			legal_moves = self.remove_moves_resulting_in_check(legal_moves, "w")
			self.white_turn = not self.white_turn
		else:
			legal_moves = self.get_legal_moves(self.board, "b")
			legal_moves = self.remove_moves_resulting_in_check(legal_moves, "b")
			self.white_turn = not self.white_turn
		if(len(legal_moves) == 0):
			print("Game Over")
			sys.exit(0)
		else:
			move = self.pick_move(legal_moves)
			self.upgrade_pawns(move)
			self.board = move
	
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
		if(i-1 >= 0 and j-1 >= 0 and j+1 <= 7 and board[i-1][j-1].is_occupied and board[i-1][j-1].color == "b"):
			squares.append([i-1, j-1])
		#take piece right
		if(i-1 >= 0 and j-1 >= 0 and j+1 <= 7 and board[i-1][j+1].is_occupied and board[i-1][j+1].color == "b"):
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
		if(i+1 <= 7 and j-1 >= 0 and j+1 <= 7 and board[i+1][j-1].is_occupied and board[i+1][j-1].color == "w"):
			squares.append([i+1, j-1])
		#take piece right
		if(i+1 <= 7 and j-1 >= 0 and j+1 <= 7 and board[i+1][j+1].is_occupied and board[i+1][j+1].color == "w"):
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
		return legal_moves

	def pick_move(self, legal_moves):
		return legal_moves[random.randrange(0, len(legal_moves))]

	def print_board(self, board):
		print(Fore.WHITE + "~~~~~~~~~~~~~~~~~")
		for i in board:
			for j in i:
				if(j.color == "b"):
					print(Fore.WHITE + "|", end='')
					print(Fore.BLUE + j.piece, end='')
				elif(j.color == "w"):
					print(Fore.WHITE + "|", end='')
					print(Fore.GREEN + j.piece, end='')
				else:
					print(Fore.WHITE + "| ", end='')
			print(Fore.WHITE + "|")
			print(Fore.WHITE + "~~~~~~~~~~~~~~~~~")
		print("")

my_game = game()
for i in range(0, 1000):
	my_game.make_move()
	my_game.print_board(my_game.board)
#TODO:
##Castleing
##enpasqnt
##checkmate vs stalemate
##human move
##ml

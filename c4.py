import numpy as np
import random
import pygame
import sys
import math
from gameboard import *

# colors
BLUE = (0,0,200)
BLACK = (0,0,0)
RED = (227, 38, 54)
YELLOW = (255,255,0)

#game creation statics
WINDOW_LENGTH = 4

ROWS = 6
COLUMNS = 7

SECTION = 100
width = COLUMNS * SECTION
height = (ROWS+1) * SECTION

size = (width, height)

RADIUS = int(SECTION/2 - 5)

#players info
AGENT = 1
HUMAN = 0
NONE = 0
PLAYER_1 = 1
PLAYER_2 = 2

#connect4 bo



def get_board(bo):
	for col in range(COLUMNS):
		for row in range(ROWS):
			pygame.draw.rect(screen, BLUE, (col*SECTION, row*SECTION+SECTION, SECTION, SECTION))
			pygame.draw.circle(screen, BLACK, (int(col*SECTION+SECTION/2), int(row*SECTION+SECTION+SECTION/2)), RADIUS)
	
	for col in range(COLUMNS):
		for row in range(ROWS):		
			if bo[row][col] == PLAYER_1:
				pygame.draw.circle(screen, RED, (int(col*SECTION+SECTION/2), height-int(row*SECTION+SECTION/2)), RADIUS)
			elif bo[row][col] == PLAYER_2: 
				pygame.draw.circle(screen, YELLOW, (int(col*SECTION+SECTION/2), height-int(row*SECTION+SECTION/2)), RADIUS)
	pygame.display.update()

#moves

def best_move(bo, piece):

	valid_locs = fetch_valid_positions(bo, COLUMNS, ROWS)
	best_score = -10000
	best_col = random.choice(valid_locs)
	for col in valid_locs:
		row = fetch_next_position(bo, col, ROWS)
		board2 = bo.copy()
		drop_disc(board2, row, col, piece)
		score = point_position(bo, piece)
		if score > best_score:
			best_score = score
			best_col = col

	return best_col

def game_move(bo, piece):
	#for horizontal,vertical and sloped diagonal locations 
	for col in range(COLUMNS-3):
		for row in range(ROWS):
			if bo[row][col] == piece and bo[row][col+1] == piece and bo[row][col+2] == piece and bo[row][col+3] == piece:
				return True

	for col in range(COLUMNS):
		for row in range(ROWS-3):
			if bo[row][col] == piece and bo[row+1][col] == piece and bo[row+2][col] == piece and bo[row+3][col] == piece:
				return True

	for col in range(COLUMNS-3):
		for row in range(ROWS-3):
			if bo[row][col] == piece and bo[row+1][col+1] == piece and bo[row+2][col+2] == piece and bo[row+3][col+3] == piece:
				return True

	for col in range(COLUMNS-3):
		for row in range(3, ROWS):
			if bo[row][col] == piece and bo[row-1][col+1] == piece and bo[row-2][col+2] == piece and bo[row-3][col+3] == piece:
				return True

def evaluation_window(window, piece):
	score = 0
	opp_piece = PLAYER_1
	if piece == PLAYER_1:
		opp_piece = PLAYER_2

	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(NONE) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(NONE) == 2:
		score += 2

	if window.count(opp_piece) == 3 and window.count(NONE) == 1:
		score -= 4

	return score

def point_position(bo, piece):
	score = 0

	center_array = [int(i) for i in list(bo[:, COLUMNS//2])]
	center_count = center_array.count(piece)
	score += center_count * 3

	for row in range(ROWS):
		row_array = [int(i) for i in list(bo[row,:])]
		for col in range(COLUMNS-3):
			window = row_array[col:col+WINDOW_LENGTH]
			score += evaluation_window(window, piece)

	for col in range(COLUMNS):
		col_array = [int(i) for i in list(bo[:,col])]
		for row in range(ROWS-3):
			window = col_array[row:row+WINDOW_LENGTH]
			score += evaluation_window(window, piece)

	for row in range(ROWS-3):
		for col in range(COLUMNS-3):
			window = [bo[row+i][col+i] for i in range(WINDOW_LENGTH)]
			score += evaluation_window(window, piece)

	for row in range(ROWS-3):
		for col in range(COLUMNS-3):
			window = [bo[row+3-i][col+i] for i in range(WINDOW_LENGTH)]
			score += evaluation_window(window, piece)

	return score

def final_node(bo):
	return game_move(bo, PLAYER_1) or game_move(bo, PLAYER_2) or len(fetch_valid_positions(bo, COLUMNS, ROWS)) == 0


def minimax(bo, depth, alpha, beta, maximizingPlayer):
	valid_locs = fetch_valid_positions(bo, COLUMNS, ROWS)
	is_terminal = final_node(bo)
	if depth == 0 or is_terminal:
		if is_terminal:
			if game_move(bo, PLAYER_2):
				return (None, 100000000000000)
			elif game_move(bo, PLAYER_1):
				return (None, -10000000000000)
			else: 
				return (None, 0)
		else: # Depth is zero
			return (None, point_position(bo, PLAYER_2))
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locs)
		for col in valid_locs:
			row = fetch_next_position(bo, col, ROWS)
			copy = bo.copy()
			drop_disc(copy, row, col, PLAYER_2)
			new_score = minimax(copy, depth-1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else: 
		value = math.inf
		column = random.choice(valid_locs)
		for col in valid_locs:
			row = fetch_next_position(bo, col, ROWS)
			copy = bo.copy()
			drop_disc(copy, row, col, PLAYER_1)
			new_score = minimax(copy, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value





bo = draw_board(ROWS, COLUMNS)
log_board(bo)
game_over = False

pygame.init()

screen = pygame.display.set_mode(size)
get_board(bo)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 50)

turn = random.randint(HUMAN, AGENT)

while not game_over:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, BLACK, (0,0, width, SECTION))
			posx = event.pos[0]
			if turn == HUMAN:
				pygame.draw.circle(screen, RED, (posx, int(SECTION/2)), RADIUS)

		pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, BLACK, (0,0, width, SECTION))
			if turn == HUMAN:
				posx = event.pos[0]
				col = int(math.floor(posx/SECTION))

				if fetch_location(bo, col, ROWS):
					row = fetch_next_position(bo, col, ROWS)
					drop_disc(bo, row, col, PLAYER_1)

					if game_move(bo, PLAYER_1):
						label = myfont.render("Player 1 Won!", 1, RED)
						screen.blit(label, (40,10))
						game_over = True

					turn += 1
					turn = turn % 2

					log_board(bo)
					get_board(bo)


	if turn == AGENT and not game_over:				

		col, minimax_score = minimax(bo, 5, -math.inf, math.inf, True)

		if fetch_location(bo, col, ROWS):
			
			row = fetch_next_position(bo, col, ROWS)
			drop_disc(bo, row, col, PLAYER_2)

			if game_move(bo, PLAYER_2):
				label = myfont.render("Player 2 Won!", 1, YELLOW)
				screen.blit(label, (40,10))
				game_over = True

			log_board(bo)
			get_board(bo)

			turn += 1
			turn = turn % 2

	if game_over:
		pygame.time.wait(3000)


import numpy as np

def draw_board(rows,columns):
	bo = np.zeros((rows,columns))
	return bo

def log_board(bo):
	print(np.flip(bo, 0))


def drop_disc(bo, row, col, piece):
	bo[row][col] = piece

def fetch_location(bo, col, rows):
	return bo[rows-1][col] == 0

def fetch_valid_positions(bo,columns, rows):
	valid_locations = []
	for col in range(columns):
		if fetch_location(bo, col, rows):
			valid_locations.append(col)
	return valid_locations

def fetch_next_position(bo, col, rows):
	for row in range(rows):
		if bo[row][col] == 0:
			return row

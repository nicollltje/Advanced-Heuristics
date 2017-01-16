# board genator rush hour
# advanced heuristics
# Nicole and Nicol

import random
import csv

# open textfile to store board parameters
parameter_file = open("parameters.txt", "w")

# give the board size
board_size = 9

# full / total
filled_tiles = 0.5 * board_size*board_size

# amount of boards to generate
boards = 100

# 1 = smart (1x1)
# 2 = car (1x2)
# 3 = truck (1x3)
# 4 = long car (1x4)
# 5 = betonwagen (2x3)

i = 0
for (i in range boards):

	i += 1
	board = tostring("board"+i+".csv")
	
	outputfile = open(board, "w")

	# Horizontal / Vertical, random
	orientation_ratio = random.randrange(0.5, 5, 0.1)

	parameter_file.write(i, fill_ratio, vehicle_ratio, orientation_ratio)

	# write the board size as the first line of the csv
	outputfile.writerow(board_size)

	# position of the red car (x, y, type, orientation, id)
	y = board_size / 2
	outputfile.writerow(2, y, 2, "H", 1)

	j = 2
	for (j in range cars):
		length = 2
		x_pos = random.randrange(0, board_size, 1)
		y_pos = random.randrange(0, board_size, 1)
		vehicle_id = i
		# TODO
		orientation = "H"
		vehicle = x_pos, y_pos, length, orientation, vehicle_id
		outputfile.writerow(vehicle)
		i += 1


	for (j in range trucks):
		length = 3
		x_pos = random.randrange(0, board_size, 1)
		y_pos = random.randrange(0, board_size, 1)
		vehicle_id = i
		# TODO
		orientation = "H"
		vehicle = x_pos, y_pos, length, orientation, vehicle_id
		outputfile.writerow(vehicle)
		i += 1

# board genator rush hour
# advanced heuristics
# Nicole and Nicol

import random
import csv
import os
import sys

def pickPosition(dimension, type, orientation):

	print "**********************************************"
	print "picking NEW position"
	# give a vehicle a random position on the board
	x_pos = random.randrange(0, dimension, 1)
	y_pos = random.randrange(0, dimension, 1)

	# adjust the coordinates to make sure the vehicle does not go out of bounds
	if orientation == "H":
		if type == 2:
			x_pos = random.randrange(0, dimension - 1, 1)
		if type == 3:
			x_pos = random.randrange(0, dimension - 2, 1)
		if type == 4:
			x_pos = random.randrange(0, dimension - 3, 1)
		if type == 5:
			x_pos = random.randrange(0, dimension - 2, 1)
			y_pos = random.randrange(0, dimension - 1, 1)

	if orientation == "V":
		if type == 2:
			y_pos = random.randrange(0, dimension - 1, 1)
		if type == 3:
			y_pos = random.randrange(0, dimension - 2, 1)
		if type == 4:
			y_pos = random.randrange(0, dimension - 3, 1)
		if type == 5:
			y_pos = random.randrange(0, dimension - 2, 1)
			x_pos = random.randrange(0, dimension - 1, 1)

	print "printing positions"
	print str(x_pos) + str(y_pos)

	return [x_pos, y_pos]

def generateBoards(boards, foldername, dimension):

	os.makedirs(os.path.dirname('%s/' %(foldername)))

	# amount of boards to generate
	boards = boards

	# give the board size
	dimension = dimension

	# create an archive to check for duplicate beginning positions
	position_set = set()

	# open textfile to store board parameters
	parameter_file = open("%s/parameters%s.txt" %(foldername, foldername), "w")

	# set the filling
	filling = 0.2

	for i in range (boards):
		filled_tiles = int((dimension * dimension) * filling)
		board = "board"+str(i)+".csv"
		filename = '%s/%s' %(foldername, board)
		print board

		counter1 = 0
		counter2 = 0
		counter3 = 0
		counter4 = 0
		counter5 = 0

		with open(filename, 'wb') as csvfile:

			boardwriter = csv.writer(csvfile, delimiter=',',
									quotechar='|', quoting=csv.QUOTE_MINIMAL)

			# write the board size as the first line of the csv
			boardwriter.writerow([dimension])

			# position of the red car (x, y, type, orientation, id)
			y = dimension / 2
			boardwriter.writerow([2, y, 2, "H", 1])
			filled_tiles -= 2
			red_car = str(2)+str(y)
			position_set.add(red_car)

			j = 2
			while filled_tiles > 0:
				# picks a random orientation
				orientation = random.randrange (1, 3, 1)
				if orientation == 1:
					orientation = "H"
				else:
					orientation = "V"

				# assign id to the vehicle
				vehicle_id = j
				j += 1

				# pick a random type of vehicle that fits in the amount of space available
				if filled_tiles == 5 or filled_tiles == 4:
					type = random.randrange(1, 5, 1)
				elif filled_tiles == 3:
					type = random.randrange(1, 4, 1)
				elif filled_tiles == 2:
					type = random.randrange(1, 3, 1)
				elif filled_tiles == 1:
					type = 1
				else:
					type = random.randrange(1, 6, 1)

				if type == 1:
					counter1 += 1
					filled_tiles -= 1
				elif type == 2:
					counter2 += 1
					filled_tiles -= 2
				elif type == 3:
					counter3 += 1
					filled_tiles -= 3
				elif type == 4:
					counter4 += 1
					filled_tiles -= 4
				else:
					counter5 += 1
					filled_tiles -= 6

				start_coordinate = pickPosition(dimension, type, orientation)

				start_x = start_coordinate[0]
				start_y = start_coordinate[1]

				position = str(start_x) + str(start_y)

				i_length = len(position_set)

				f_lenght = 0



				while i_length == f_lenght:

					start_coordinate = pickPosition(dimension, type, orientation)

					start_x = start_coordinate[0]
					start_y = start_coordinate[1]

					position = str(start_x)+str(start_y)

					position_set.add(position)

					f_lenght = len(position_set)

					print i_length, f_lenght

				vehicle = start_x, start_y, type, orientation, vehicle_id
				boardwriter.writerow(vehicle)

		counters = "type1 = %d, type2 = %d, type3 = %d, type4 = %d, type5 = %d" %(counter1, counter2, counter3, counter4, counter5)
		params = "board: %d, dimension: %d, filling: %f \n %s \n \n" %(i, dimension, filling, counters)
		parameter_file.write(params)


if (len(sys.argv) != 4):
    print "improper usage. USAGE: board_generator.py dimension boards foldername"
else:
	try:
		# try and get the proper parameters from command line argument
		dimension = int(sys.argv[1])
		boards = int(sys.argv[2])
		foldername = str(sys.argv[3])

		# generate boards with given parameters
		generateBoards(boards, foldername, dimension)

	except ValueError:
		# if the imput is invalid inform the user with a print statement
		print("boards and dimension should be of type integer")



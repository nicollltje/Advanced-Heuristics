# board genator rush hour
# advanced heuristics
# Nicole and Nicol

import random
import csv
import os
import sys
import numpy as np

class Car(object):

    """
    A Car represents an object with length 2 or 3 and a certain orientation (horizontal or vertical),
    which can move around the board.
    """

    def __init__(self, x, y, type, orientation, id):

        """
        Initializes a car with a position with coordinates [x, y] on a board with a given length,
        orientation and id.
        :param x, y, length, orientation, id: All parameters are defined in a separate list.
        """

        self.x = x
        self.y = y
        self.orientation = orientation
        self.type = type
        self.id = id

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

def boardWriter(car):

	boardwriter = csv.writer(csvfile, delimiter=',',
							 quotechar='|', quoting=csv.QUOTE_MINIMAL)

	vehicle = car.x, car.y, car.type, car.orientation, car.id
	boardwriter.writerow(vehicle)

def validateCar(car, dimension):

	# get the parameters from the car object
	x = car.x
	y = car.y
	orientation = car.orientation
	type = car.type

	if type == 1:
		if board[x, y] == 0:
			pos = str(x)+str(y)
			position_list.remove(pos)
			vehicle = x, y, type, orientation, car.id
			boardwriter.writerow(vehicle)
			if orientation == "H":
				board[x,y] = "SH"
			else:
				board[x, y] = "SV"
		else:
			print "NO"

	elif type == 2 and orientation == "H":
		if x < dimension - 1:
			if board[x, y] == 0 and board[x + 1, y] == 0:
				board[x, y] = "CH"
				pos = str(x) + str(y)
				position_list.remove(pos)
				board[x + 1, y] = "CH"
				pos = str(x+1) + str(y)
				position_list.remove(pos)
		else:
			print "NO"

	elif type == 2 and orientation == "V":
		if y < dimension - 1:
			if board[x, y] == 0 and board[x, y + 1] == 0:
				board[x, y] = "CV"
				pos = str(x) + str(y)
				position_list.remove(pos)
				board[x, y + 1] = "CV"
				pos = str(x) + str(y+1)
				position_list.remove(pos)
		else:
			print "NO"

	elif type == 3 and orientation == "H":
		if x < dimension - 2:
			if board[x, y] == 0 and board[x + 1, y] == 0 and board[x + 2, y] == 0:
				board[x, y] = "TH"
				pos = str(x) + str(y)
				position_list.remove(pos)
				board[x + 1, y] = "TH"
				pos = str(x+1) + str(y)
				position_list.remove(pos)
				board[x + 2, y] = "TH"
				pos = str(x+2) + str(y)
				position_list.remove(pos)
		else:
			print "NO"

	elif type == 3 and orientation == "V":
		if y < dimension - 3:
			if board[x, y] == 0 and board[x, y + 1] == 0 and board[x, y + 2] == 0:
				board[x, y] = "TV"
				pos = str(x) + str(y)
				position_list.remove(pos)
				board[x, y + 1] = "TV"
				pos = str(x) + str(y+1)
				position_list.remove(pos)
				board[x, y + 2] = "TV"
				pos = str(x) + str(y+2)
				position_list.remove(pos)
		else:
			print "NO"

	elif type == 4:
		if x < dimension - 1 and y < dimension - 1:
			if board[x,y] == 0 and board[x+1,y] == 0 and board[x,y+1] == 0 and board[x+1,y+1] == 0:
				pos = str(x) + str(y)
				position_list.remove(pos)
				pos = str(x+1) + str(y)
				position_list.remove(pos)
				pos = str(x+1) + str(y+1)
				position_list.remove(pos)
				pos = str(x) + str(y+1)
				position_list.remove(pos)
				if orientation == "H":
					board[x,y] = "QH"
					board[x + 1,y] = "QH"
					board[x,y + 1] = "QH"
					board[x + 1,y + 1] = "QH"
				else:
					board[x, y] = "QV"
					board[x + 1, y] = "QV"
					board[x, y + 1] = "QV"
					board[x + 1, y + 1] = "QV"
		else:
			print "NO"

	elif type == 5 and orientation == "H":
		if x < dimension - 2 and y < dimension - 1:
			if board[x, y] == 0 and board[x + 1, y] == 0 and board[x + 2, y] == 0:
				if board[x, y + 1] == 0 and board[x + 1, y + 1] == 0 and board[x + 2, y + 1] == 0:
					board[x, y] = "BH"
					pos = str(x) + str(y)
					position_list.remove(pos)
					board[x, y + 1] = "BH"
					pos = str(x) + str(y+1)
					position_list.remove(pos)
					board[x + 1, y] = "BH"
					pos = str(x+1) + str(y)
					position_list.remove(pos)
					board[x + 1, y + 1] = "BH"
					pos = str(x+1) + str(y+1)
					position_list.remove(pos)
					board[x + 2, y] = "BH"
					pos = str(x+2) + str(y)
					position_list.remove(pos)
					board[x + 2, y + 1] = "BH"
					pos = str(x+2) + str(y+1)
					position_list.remove(pos)
			else:
				print "NO"
		else:
			print "NO"

	elif type == 5 and orientation == "V":
		if x < dimension - 1 and y < dimension - 2:
			if board[x, y] == 0 and board[x, y + 1] == 0 and board[x, y + 2] == 0:
				if board[x + 1, y] == 0 and board[x + 1, y + 1] == 0 and board[x + 1, y + 2] == 0:
					board[x, y] = "BV"
					pos = str(x) + str(y)
					position_list.remove(pos)
					board[x + 1, y] = "BV"
					pos = str(x+1) + str(y)
					position_list.remove(pos)
					board[x, y + 1] = "BV"
					pos = str(x) + str(y+1)
					position_list.remove(pos)
					board[x + 1, y + 1] = "BV"
					pos = str(x+1) + str(y+1)
					position_list.remove(pos)
					board[x, y + 2] = "BV"
					pos = str(x) + str(y+2)
					position_list.remove(pos)
					board[x + 1, y + 2] = "BV"
					pos = str(x+1) + str(y+2)
					position_list.remove(pos)
				else:
					print "NO"
		else:
			print "NO"

	# elif type == 6 and orientation == "H":
	# 	if board[x, y] == 0 and board[x + 1, y] == 0 and board[x + 2, y] == 0 and board[x + 3, y] == 0:
	# 		board[x, y] = id
	# 		board[x + 1, y] = id
	# 		board[x + 2, y] = id
	# 		board[x + 3, y] = id
	# 	else:
	# 		print "NO"

	# elif type == 6 and orientation == "V":
	# 	if board[x, y] == 0 and board[x, y + 1] == 0 and board[x, y + 2] == 0 and board[x, y + 3] == 0:
	# 		board[x, y] = id
	# 		board[x, y + 1] = id
	# 		board[x, y + 2] = id
	# 		board[x, y + 3] = id
	# 	else:
	# 		print "NO"

def generateBoards(boards, foldername, dimension):

	# make a folder to save the boards in
	os.makedirs(os.path.dirname('%s/' %(foldername)))

	# amount of boards to generate
	boards = boards

	# give the board size
	dimension = dimension

	# open textfile to store board parameters
	parameter_file = open("%s/zzparameters%s.txt" %(foldername, foldername), "w")

	# set the filling
	filling = 0.2

	for i in range (boards):

		# calculate the filling
		filled_tiles = int((dimension * dimension) * filling)

		# make a new file for each board
		board = "board"+str(i)+".csv"
		filename = '%s/%s' %(foldername, board)

		# set counters to keep track of how many vehicles per type are generated
		counter1 = 0
		counter2 = 0
		counter3 = 0
		counter4 = 0
		counter5 = 0
		counter6 = 0

		# set empty archive for start positions
		# position_set = set()

		# create an empty board
		board = np.zeros(shape=(dimension, dimension), dtype=object)

		with open(filename, 'wb') as csvfile:

			boardwriter = csv.writer(csvfile, delimiter=',',
									quotechar='|', quoting=csv.QUOTE_MINIMAL)

			# write the board size as the first line of the csv
			boardwriter.writerow([dimension])

			# define which types will be present on the board
			car_types = [2, 3]

			# create a list of all positions on the board
			position_list = []
			for i in range(dimension):
				for j in range(dimension):
					pos = str(i)+str(j)
					position_list.append(pos)

			# position of the red car (x, y, type, orientation, id)
			y = (dimension / 2) - 1
			x = 1

			# place red car on the board
			board[x, y] = 'CH'
			board[x + 1, y] = 'CH'

			# remove the positions of the red car from the list of available positions
			pos = str(x)+str(y)
			position_list.remove(pos)
			pos2 = str(x+1)+str(y)
			position_list.remove(pos2)

			# write the red car to the output csv file
			boardwriter.writerow([1, y, 2, "H", 1])

			# update the filled tiles
			filled_tiles -= 2

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

				# pick a vehicle type from the available vehicle types
				type = random.choice(car_types)

				# pick a random type of vehicle that fits in the amount of space available
				# if filled_tiles == 5 or filled_tiles == 4:
				# 	type = random.randrange(1, 5, 1)
				# elif filled_tiles == 3:
				# 	type = random.randrange(1, 4, 1)
				# elif filled_tiles == 2:
				# 	type = random.randrange(1, 3, 1)
				# elif filled_tiles == 1:
				# 	type = 1
				# else:
				# 	type = random.randrange(1, 6, 1)
				# pick a random starting position from the list of available positions

				start_position = random.choice(position_list)
				x_pos = int(start_position[0])
				y_pos = int(start_position[1])

				car = Car(x_pos, y_pos, type, orientation, id)
				validateCar(car, dimension)

				#start_coordinate = pickPosition(dimension, type, orientation)

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
				elif type == 5:
					counter5 += 1
					filled_tiles -= 6
				else:
					counter6 += 1
					filled_tiles -= 4

				# start_x = start_coordinate[0]
				# start_y = start_coordinate[1]
                #
				# position = str(start_x) + str(start_y)
                #
				# i_length = len(position_set)
                #
				# f_lenght = 0
                #
				# while i_length == f_lenght:
                #
				# 	start_coordinate = pickPosition(dimension, type, orientation)
                #
				# 	start_x = start_coordinate[0]
				# 	start_y = start_coordinate[1]
                #
				# 	position = str(start_x)+str(start_y)
                #
				# 	position_set.add(position)
                #
				# 	f_lenght = len(position_set)
                #
				# 	print i_length, f_lenght

				vehicle = x_pos, y_pos, type, orientation, vehicle_id
				boardwriter.writerow(vehicle)

		# write all parameters of the board into a parameter file
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

		position_list = []

		# generate boards with given parameters
		generateBoards(boards, foldername, dimension)

	except ValueError:

		# if the input is invalid inform the user with a print statement
		print boards
		print dimension
		print foldername
		print("boards and dimension should be of type integer")



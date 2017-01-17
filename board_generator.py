# board genator rush hour
# advanced heuristics
# Nicole and Nicol

import random
import csv
import os
import sys

def generateBoards(boards, foldername, dimension):

	os.makedirs(os.path.dirname('%s/' %(foldername)))

	# amount of boards to generate
	boards = boards

	# give the board size
	dimension = dimension

	for i in range (boards):
		filled_tiles = (dimension * dimension) / 5
		board = "board"+str(i)+".csv"
		filename = '%s/%s' %(foldername, board)
		print board
		params = "board: "+str(i)+" dimension: "+str(dimension)+" filled tiles: "+str(filled_tiles)+'\n'
		parameter_file.write(params)

		with open(filename, 'wb') as csvfile:

			boardwriter = csv.writer(csvfile, delimiter=',',
									quotechar='|', quoting=csv.QUOTE_MINIMAL)

			# write the board size as the first line of the csv
			boardwriter.writerow([dimension])

			# position of the red car (x, y, type, orientation, id)
			y = dimension / 2
			boardwriter.writerow([2, y, 2, "H", 1])
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

				# give a vehicle a random position on the board
				x_pos = random.randrange(0, dimension, 1)
				y_pos = random.randrange(0, dimension, 1)
				filled_tiles -= 1

				# adjust the coordinates to make sure the vehicle does not go out of bounds
				if orientation == "H":
					if type == 2:
						x_pos = random.randrange(0, dimension - 1, 1)
						filled_tiles -= 1
					if type == 3:
						x_pos = random.randrange(0, dimension - 2, 1)
						filled_tiles -= 2
					if type == 4:
						x_pos = random.randrange(0, dimension - 3, 1)
						filled_tiles -= 3
					if type == 5:
						x_pos = random.randrange(0, dimension - 2, 1)
						y_pos = random.randrange(0, dimension - 1, 1)
						filled_tiles -= 5

				if orientation == "V":
					if type == 2:
						y_pos = random.randrange(0, dimension - 1, 1)
						filled_tiles -= 1
					if type == 3:
						y_pos = random.randrange(0, dimension - 2, 1)
						filled_tiles -= 2
					if type == 4:
						y_pos = random.randrange(0, dimension - 3, 1)
						filled_tiles -= 3
					if type == 5:
						y_pos = random.randrange(0, dimension - 2, 1)
						x_pos = random.randrange(0, dimension - 1, 1)
						filled_tiles -= 5

				vehicle = x_pos, y_pos, type, orientation, vehicle_id
				boardwriter.writerow(vehicle)

if (len(sys.argv) != 4):
    print "improper usage. USAGE: board_generator.py dimension boards foldername"
else:
	try:
		# try and get the proper parameters from command line argument
		dimension = int(sys.argv[1])
		boards = int(sys.argv[2])
		foldername = str(sys.argv[3])

		# open textfile to store board parameters
		parameter_file = open("parameters.txt", "w")

		# generate boards with given parameters
		generateBoards(boards, foldername, dimension)

	except ValueError:
		# if the imput is invalid inform the user with a print statement
		print("boards and dimension should be of type integer")



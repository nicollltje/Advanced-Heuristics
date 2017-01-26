# board genator rush hour
# advanced heuristics
# Nicole and Nicol

import random
import csv
import os
import sys
import numpy as np

position_list = []

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

def resetPositionList(board, dimension):

    del position_list[:]

    for i in range(dimension):
        for j in range(dimension):
            if board[i,j] == 0:
                pos = str(i)+str(j)
                position_list.append(pos)

    print "position list length: ", len(position_list)

def validatePosition(dimension, board, type, orientation, x, y):

    if type == 1:
        print "Smart"
        if board[x, y] == 0:
            print "Position %d, %d is possible" %(x,y)
            return True

    elif type == 2 and orientation == "H":
        print "Horizontal car"
        if x < dimension - 1:
            if board[x, y] == 0 and board[x + 1, y] == 0:
                print "Positions %d, %d and %d, %d are possible" %(x, y, x+1, y)
                return True

    elif type == 2 and orientation == "V":
        print "Vertical car"
        if y < dimension - 1:
            if board[x, y] == 0 and board[x, y + 1] == 0:
                print "Positions %d, %d and %d, %d are possible" %(x, y, x, y+1)
                return True

    elif type == 3 and orientation == "H":
        print "Horizontal truck"
        if x < dimension - 2:
            if board[x, y] == 0 and board[x + 1, y] == 0 and board[x + 2, y] == 0:
                print "Positions %d, %d; %d, %d and %d, %d are possible" %(x, y, x+1, y, x+2, y)
                return True

    elif type == 3 and orientation == "V":
        print "Vertical truck"
        if y < dimension - 3:
            if board[x, y] == 0 and board[x, y + 1] == 0 and board[x, y + 2] == 0:
                print "Positions %d, %d; %d, %d and %d, %d are possible" %(x, y, x, y+1, x, y+2)
                return True

    elif type == 4:
        print "Quad"
        if x < dimension - 1 and y < dimension - 1:
            if board[x,y] == 0 and board[x+1,y] == 0 and board[x,y+1] == 0 and board[x+1,y+1] == 0:
                print "Positions %d, %d; %d, %d; %d, %d and %d, %d are possible" %(x,y,x+1,y,x,y+1,x+1,y+1)
                return True

    elif type == 5 and orientation == "H":
        print "Horizontal betonwagen"
        if x < dimension - 2 and y < dimension - 1:
            if board[x, y] == 0 and board[x + 1, y] == 0 and board[x + 2, y] == 0:
                if board[x, y + 1] == 0 and board[x + 1, y + 1] == 0 and board[x + 2, y + 1] == 0:
                    print "Positions %d, %d; %d, %d; %d, %d; %d, %d; %d, %d and %d, %d are possible" %(x,y,x+1,y,x+2,y,x,y+1,x+1,y+1,x+2,y+1)
                    return True

    elif type == 5 and orientation == "V":
        print "Vertical betonwagen"
        if x < dimension - 1 and y < dimension - 2:
            if board[x, y] == 0 and board[x, y + 1] == 0 and board[x, y + 2] == 0:
                if board[x + 1, y] == 0 and board[x + 1, y + 1] == 0 and board[x + 1, y + 2] == 0:
                    print "Positions %d, %d; %d, %d; %d, %d; %d, %d; %d, %d and %d, %d are possible" %(x,y,x,y+1,x,y+2,x+1,y,x+1,y+1,x+1,y+2)
                    return True

    return False

def validateCar(car, dimension, board, x, y):

    print "____________validating car__________________"

    # get the parameters from the car object
    orientation = car.orientation
    type = car.type

    print car.id

    valid_position = validatePosition(dimension, board, type, orientation, x, y)

    if type == 1:
        if valid_position == True:

            # remove all taken positions from list of available positions
            # pos = str(x)+str(y)
            # position_list.remove(pos)

            if orientation == "H":
                board[x,y] = "SH"
                print board.T
                return board, car

            else:
                board[x, y] = "SV"
                print board.T
                return board, car

    elif type == 2:
        if valid_position == True:
            if orientation == "H":

                #print "placing horizontal car"
                board[x, y] = "CH"
                board[x + 1, y] = "CH"
                print board.T

                # remove all taken positions from list of available positions
                # pos = str(x) + str(y)
                # position_list.remove(pos)
                # pos = str(x+1) + str(y)
                # position_list.remove(pos)

                return board, car

            else:

                #print "placing vertical car"
                board[x, y] = "CV"
                board[x, y + 1] = "CV"
                print board.T
                # remove all taken positions from list of available positions
                # pos = str(x) + str(y)
                # position_list.remove(pos)
                # pos = str(x) + str(y + 1)
                # position_list.remove(pos)

                return board, car

    elif type == 3:

        if valid_position == True:
            if orientation == "H":

                board[x, y] = "TH"
                board[x + 1, y] = "TH"
                board[x + 2, y] = "TH"
                print board.T

                # remove all taken positions from list of available positions
                # pos = str(x) + str(y)
                # position_list.remove(pos)
                # pos = str(x + 1) + str(y)
                # position_list.remove(pos)
                # pos = str(x+2) + str(y)
                # position_list.remove(pos)

                return board, car

            else:

                board[x, y] = "TV"
                board[x, y + 1] = "TV"
                board[x, y + 2] = "TV"
                print board.T

                # remove all taken positions from list of available positions
                # pos = str(x) + str(y)
                # position_list.remove(pos)
                # pos = str(x) + str(y + 1)
                # position_list.remove(pos)
                # pos = str(x) + str(y + 2)
                # position_list.remove(pos)

                return board, car

    elif type == 4:
        if valid_position == True:

            # remove all taken positions from list of available positions
            # pos = str(x) + str(y)
            # position_list.remove(pos)
            # pos = str(x+1) + str(y)
            # position_list.remove(pos)
            # pos = str(x+1) + str(y+1)
            # position_list.remove(pos)
            # pos = str(x) + str(y+1)
            # position_list.remove(pos)

            if orientation == "H":

                board[x,y] = "QH"
                board[x + 1,y] = "QH"
                board[x,y + 1] = "QH"
                board[x + 1,y + 1] = "QH"
                print board.T

                return board, car

            else:

                board[x, y] = "QV"
                board[x + 1, y] = "QV"
                board[x, y + 1] = "QV"
                board[x + 1, y + 1] = "QV"
                print board.T

                return board, car

    elif type == 5:
        if valid_position == True:

            if orientation == "H":

                board[x, y] = "BH"
                board[x, y + 1] = "BH"
                board[x + 1, y] = "BH"
                board[x + 1, y + 1] = "BH"
                board[x + 2, y] = "BH"
                board[x + 2, y + 1] = "BH"
                print board.T

                # remove all taken positions from list of available positions
                # pos = str(x) + str(y)
                # position_list.remove(pos)
                # pos = str(x) + str(y + 1)
                # position_list.remove(pos)
                # pos = str(x + 1) + str(y)
                # position_list.remove(pos)
                # pos = str(x + 1) + str(y + 1)
                # position_list.remove(pos)
                # pos = str(x + 2) + str(y)
                # position_list.remove(pos)
                # pos = str(x+2) + str(y+1)
                # position_list.remove(pos)

                return board

            elif orientation == "V":
                # set board positions
                board[x, y] = "BV"
                board[x + 1, y] = "BV"
                board[x, y + 1] = "BV"
                board[x + 1, y + 1] = "BV"
                board[x, y + 2] = "BV"
                board[x + 1, y + 2] = "BV"
                print board.T

                # remove all taken positions from list of available positions
                # pos = str(x) + str(y)
                # position_list.remove(pos)
                # pos = str(x + 1) + str(y)
                # position_list.remove(pos)
                # pos = str(x) + str(y + 1)
                # position_list.remove(pos)
                # pos = str(x + 1) + str(y + 1)
                # position_list.remove(pos)
                # pos = str(x) + str(y + 2)
                # position_list.remove(pos)
                # pos = str(x + 1) + str(y + 2)
                # position_list.remove(pos)

                return board, car


    print "Starting position %d, %d not possible; changing position" %(x,y)
    print "length postion list 2: %d" %(len(position_list))
    if len(position_list) > 0:
        pos = str(x)+str(y)
        position_list.remove(pos)
        new_position = random.choice(position_list)
        x2 = int(new_position[0])
        y2 = int(new_position[1])
        print "old pos %d, %d, new pos %d, %d" %(x,y,x2,y2)

        # TODO: change x and y into new x and y
        x = x2
        y = y2
        validateCar(car, dimension, board, x, y)
    else:
        print "No valid positions found"
        return None

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
    filling = 2

    for i in range (boards):

        # calculate the filling
        filled_tiles = int((dimension * dimension) / filling)

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

        # create an empty board
        board = np.zeros(shape=(dimension, dimension), dtype=object)

        with open(filename, 'wb') as csvfile:

            boardwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

            # write the board size as the first line of the csv
            boardwriter.writerow([dimension])

            # define which types will be present on the board
            car_types = [2, 3]



            # position of the red car (x, y, type, orientation, id)
            y = (dimension / 2) - 1
            x = 1

            # place red car on the board
            board[x, y] = 'CH'
            board[x + 1, y] = 'CH'

            resetPositionList(board, dimension)

            # remove the positions of the red car from the list of available positions
            # pos = str(x)+str(y)
            # position_list.remove(pos)
            # pos2 = str(x+1)+str(y)
            # position_list.remove(pos2)

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

                # determine which car types are available based on the amount of filled tiles
                print "tiles left: %d" %(filled_tiles)
                if filled_tiles == 5:
                    if 5 in car_types:
                        car_types.remove(5)
                    if 1 not in car_types:
                        if 4 in car_types:
                            car_types.remove(4)
                    print "car types left: ", car_types
                elif filled_tiles == 4:
                    if 5 in car_types:
                        car_types.remove(5)
                    if 1 not in car_types:
                        if 3 in car_types:
                            car_types.remove(3)
                    print "car types left: ", car_types
                elif filled_tiles == 3:
                    if 5 in car_types:
                        car_types.remove(5)
                    if 4 in car_types:
                        car_types.remove(4)
                    if 1 not in car_types:
                        if 2 in car_types:
                            car_types.remove(2)
                    print "car types left: ", car_types
                elif filled_tiles == 2:
                    if 5 in car_types:
                        car_types.remove(5)
                    if 4 in car_types:
                        car_types.remove(4)
                    if 3 in car_types:
                        car_types.remove(3)
                    print "car types left: ", car_types

                print "car types left: ", car_types

                # pick a vehicle type from the available vehicle types
                type = random.choice(car_types)
                print "Chosen vehicle: ", type

                start_position = random.choice(position_list)
                x_pos = int(start_position[0])
                y_pos = int(start_position[1])

                car = Car(x_pos, y_pos, type, orientation, vehicle_id)
                result = validateCar(car, dimension, board, x_pos, y_pos)

                if result != None:
                    print "Result from validateCar != None"
                    board = result[0]
                    car = result[1]
                    vehicle = car.x, car.y, car.type, car.orientation, car.id
                    boardwriter.writerow(vehicle)
                else:
                    print "Result from validateCar = None"
                    print "changing orientation"
                    if car.orientation == "H":
                        car.orientation ="V"
                    else:
                        car.orientation ="H"

                    resetPositionList(board, dimension)
                    result = validateCar(car, dimension, board, x_pos, y_pos)

                old_cars = []

                print "...............", car_types

                if result != None:
                    board = result[0]
                    car = result[1]
                    vehicle = car.x, car.y, car.type, car.orientation, car.id
                    boardwriter.writerow(vehicle)
                else:
                    print "changing car type"
                    while len(car_types) > 1:
                        old_type = car.type
                        old_cars.append(old_type)
                        car_types.remove(old_type)
                        print "TEMPORARY car types", car_types
                        car.type = random.choice(car_types)
                        result = validateCar(car, dimension, board, x_pos, y_pos)
                        if result != None:
                            board = result[0]
                            car = result[1]
                            vehicle = car.x, car.y, car.type, car.orientation, car.id
                            boardwriter.writerow(vehicle)

                        else:
                            print "could not place vehicle"
                            # delete the whole board and start over with the same board number.
                            # break

                for item in old_cars:
                    car_types.append(item)

                print "Check car types again...................", car_types

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

        # generate boards with given parameters
        generateBoards(boards, foldername, dimension)

    except ValueError:

        # if the input is invalid inform the user with a print statement
        print("boards and dimension should be of type integer")

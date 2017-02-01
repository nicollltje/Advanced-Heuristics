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

    # clear the position list
    del position_list[:]

    # all available positions are added to the position list
    for i in range(dimension):
        for j in range(dimension):
            if board[i, j] == 0:
                pos = str(i)+str(j)
                position_list.append(pos)

def removeTrivials():

    # No horizontal car can be placed in front of the red car, so these positions are removed from the position list
    if "32" in position_list:
        position_list.remove('32')
    if "42" in position_list:
        position_list.remove('42')
    if "52" in position_list:
        position_list.remove("52")

def checkAvailableTypes(filled_tiles, car_types):

    # based on the amount of filled tiles, some types are not possible anymore, this function removes them from the
    # list of available car types
    if filled_tiles == 5:
        if 5 in car_types:
            car_types.remove(5)
        if 1 not in car_types:
            if 4 in car_types:
                car_types.remove(4)

    elif filled_tiles == 4:
        if 5 in car_types:
            car_types.remove(5)
        if 1 not in car_types:
            if 3 in car_types:
                car_types.remove(3)

    elif filled_tiles == 3:
        if 5 in car_types:
            car_types.remove(5)
        if 4 in car_types:
            car_types.remove(4)
        if 1 not in car_types:
            if 2 in car_types:
                car_types.remove(2)

    elif filled_tiles == 2:
        if 5 in car_types:
            car_types.remove(5)
        if 4 in car_types:
            car_types.remove(4)
        if 3 in car_types:
            car_types.remove(3)

    return car_types

def validatePosition(dimension, board, type, orientation, x, y):

    # Horizontal cars can not be placed in front of the red car
    if orientation == "H":
        if y == 2:
            if x == 4 or x == 3 or x == 2:
                return False

    # for all types the board is checked if all needed positions for that type are free
    if type == 1:
        if board[x, y] == 0:
            return True

    elif type == 2 and orientation == "H":
        if x < dimension - 1:
            if board[x, y] == 0 and board[x + 1, y] == 0:
                return True

    elif type == 2 and orientation == "V":
        if y < dimension - 1:
            if board[x, y] == 0 and board[x, y + 1] == 0:
                return True

    elif type == 3 and orientation == "H":
        if x < dimension - 2:
            if board[x, y] == 0 and board[x + 1, y] == 0 and board[x + 2, y] == 0:
                return True

    elif type == 3 and orientation == "V":
        if y < dimension - 3:
            if board[x, y] == 0 and board[x, y + 1] == 0 and board[x, y + 2] == 0:
                return True

    elif type == 4:
        if x < dimension - 1 and y < dimension - 1:
            if board[x,y] == 0 and board[x+1,y] == 0 and board[x,y+1] == 0 and board[x+1,y+1] == 0:
                return True

    elif type == 5 and orientation == "H":
        if x < dimension - 2 and y < dimension - 1:
            if board[x, y] == 0 and board[x + 1, y] == 0 and board[x + 2, y] == 0:
                if board[x, y + 1] == 0 and board[x + 1, y + 1] == 0 and board[x + 2, y + 1] == 0:
                    return True

    elif type == 5 and orientation == "V":
        if x < dimension - 1 and y < dimension - 2:
            if board[x, y] == 0 and board[x, y + 1] == 0 and board[x, y + 2] == 0:
                if board[x + 1, y] == 0 and board[x + 1, y + 1] == 0 and board[x + 1, y + 2] == 0:
                    return True

    # if the positons are not free the function retruns False
    return False

def validateCar(car, dimension, board, x, y):

    # get parameters from the car
    orientation = car.orientation
    type = car.type
    car.x = x
    car.y = y

    # checks if the car can placed on the board
    valid_position = validatePosition(dimension, board, type, orientation, x, y)

    # sets the board to the vehicle encoding if the vehicle can be placed
    if type == 1:
        if valid_position == True:

            if orientation == "H":
                board[x,y] = "SH"

            else:
                board[x, y] = "SV"

            return (board, car)

    elif type == 2:
        if valid_position == True:
            if orientation == "H":

                board[x, y] = "CH"
                board[x + 1, y] = "CH"

            elif orientation == "V":

                board[x, y] = "CV"
                board[x, y + 1] = "CV"
            return (board, car)

    elif type == 3:

        if valid_position == True:

            if orientation == "H":
                board[x, y] = "TH"
                board[x + 1, y] = "TH"
                board[x + 2, y] = "TH"

            elif orientation == "V":

                board[x, y] = "TV"
                board[x, y + 1] = "TV"
                board[x, y + 2] = "TV"
            return (board, car)


    elif type == 4:
        if valid_position == True:


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

            return (board, car)

    elif type == 5:
        if valid_position == True:

            if orientation == "H":

                board[x, y] = "BH"
                board[x, y + 1] = "BH"
                board[x + 1, y] = "BH"
                board[x + 1, y + 1] = "BH"
                board[x + 2, y] = "BH"
                board[x + 2, y + 1] = "BH"

                return (board, car)

            elif orientation == "V":
                board[x, y] = "BV"
                board[x + 1, y] = "BV"
                board[x, y + 1] = "BV"
                board[x + 1, y + 1] = "BV"
                board[x, y + 2] = "BV"
                board[x + 1, y + 2] = "BV"

            return (board, car)

    # if the car can not be placed a different starting coordinate is chosen and the old starting coordinate is
    # (tempararily) removed from the position list
    if valid_position == False:
        if len(position_list) > 1:
            pos = str(x)+str(y)

            # remove old position from positon list if this is possible
            if pos in position_list:
                position_list.remove(pos)

            # pick a new position
            new_position = random.choice(position_list)
            x2 = int(new_position[0])
            y2 = int(new_position[1])

            # and rerun the function with the new position
            return validateCar(car, dimension, board, x2, y2)
        else:
            # if on no position the car could be placed the function returns false
            return False

def checkCar(car, board, dimension, car_types):

    # checks if the car can be placed on any place of the grid using the validateCar function
    result = validateCar(car, dimension, board, car.x, car.y)
    resetPositionList(board, dimension)

    # if this is possible the fucntion returns the new board and the new car with its position
    if result != False:
        theboard = result[0]
        thecar = result[1]
        return theboard, thecar

    # if the car could not be placed the orientation is changed
    else:
        if car.orientation == "H":
            car.orientation = "V"
        else:
            car.orientation = "H"
            removeTrivials()

        # a new result is calculated
        result = validateCar(car, dimension, board, car.x, car.y)
        resetPositionList(board, dimension)

        if result != False:
            theboard = result[0]
            thecar = result[1]
            return theboard, thecar

        # if the car could still not be placed the type was changed
        else:
            if car.orientation == "H":
                removeTrivials()

            while len(car_types) > 1:

                # the old cartype is removed from the list of available car types
                car_types.remove(car.type)

                # a new type is chosen
                car.type = random.choice(car_types)

                # and a new result is calculated
                result = validateCar(car, dimension, board, car.x, car.y)
                resetPositionList(board, dimension)

                if result != False:
                    theboard = result[0]
                    thecar = result[1]
                    return theboard, thecar

    # if no car with any type or orientation could be placed the function evaluates to false
    return False

def pickOrientaion():

    # picks a random orienation
    orientation = random.randrange(1, 3, 1)
    if orientation == 1:
        theorientation = "H"
        # make sure that no horizontal vehicle will be placed between the entrance and the red car
        removeTrivials()
    else:
        theorientation = "V"

    return theorientation

def generateBoards(boards, foldername, dimension):

    # make a folder to save the boards in
    os.makedirs(os.path.dirname('%s/' %(foldername)))

    # amount of boards to generate
    boardscounter = boards

    # create an archive to store boards, this helps with finding duplicate boards
    boardArchive = set()

    # give the board size
    dimension = dimension

    # open textfile to store board parameters
    parameter_file = open("%s/zzparameters%s.txt" %(foldername, foldername), "w")

    # set the filling
    filling = 0.65

    # set an iterator to keep track of the amount of valid boards that were made
    i = 0
    while i < boardscounter:

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

        # create an empty board
        board = np.zeros(shape=(dimension, dimension), dtype=object)

        # open a csv file to store the board in
        with open(filename, 'wb') as csvfile:

            boardwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

            # write the board size as the first line of the csv
            boardwriter.writerow([dimension])

            # position of the red car (x, y, type, orientation, id)
            y = (dimension / 2) - 1
            x = 1

            # place red car on the board
            board[x, y] = 'CH'
            board[x + 1, y] = 'CH'

            # remove the above positions from the position list, because no other vehicle can be placed there
            resetPositionList(board, dimension)

            # write the red car to the output csv file
            boardwriter.writerow([1, y, 2, "H", 1])

            # update the filled tiles
            filled_tiles -= 2

            # set a counter for the id of the vehicle
            j = 2

            # keep putting cars on the board until the filling is reached
            while filled_tiles > 0:

                # picks a random orientation
                orientation = pickOrientaion()

                # assign id to the vehicle
                vehicle_id = j
                j += 1

                # determines which car types can be on the board
                car_types_OG = [2, 3, 4, 5]

                # creates a list of car types the loop can chose from
                car_types = car_types_OG

                # determine which car types are available based on the amount of filled tiles
                car_types = checkAvailableTypes(filled_tiles, car_types)

                # pick a vehicle type from the available vehicle types
                type = random.choice(car_types)

                # pick a random starting positon for the car
                start_position = random.choice(position_list)
                x_pos = int(start_position[0])
                y_pos = int(start_position[1])

                # make al chosen parameters into a car object
                car = Car(x_pos, y_pos, type, orientation, vehicle_id)

                # check if it is possible to place the car on the board
                possible = checkCar(car, board, dimension, car_types)

                # if the car is possible, write it to the csv and update filled tiles and type counters
                if possible != False:
                    car = possible[1]
                    board = possible[0]
                    vehicle = car.x, car.y, car.type, car.orientation, car.id
                    boardwriter.writerow(vehicle)

                    type = car.type

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

                # reset board because no other vehicle could be placed
                else:
                    # remove the csv and start over
                    os.remove(filename)
                    i -= 1
                    break

            # create board hash to be able to check for duplicates
            hash = ""
            for xcoor in range(dimension):
                for ycoor in range(dimension):
                    hash += str(board[xcoor,ycoor])

            # add hash to set and check if the length of the set changes
            a = len(boardArchive)
            boardArchive.add(hash)
            b = len(boardArchive)

            # reset when duplicate board
            if a == b:
                # decrement the iterator
                i -= 1
                # remove the file if possible
                if os.path.isfile(filename):
                    os.remove(filename)

            # final check if the board is trivial or not, if so we reset
            if board[3,2] == 0 and board[4,2] == 0 and board[5,2] == 0:
                i -= 1
                if os.path.isfile(filename):
                    os.remove(filename)

            # once a valid board has been found increment the iterator
            i += 1

        # write all parameters of the board into a parameter file
        counters = "type1 = %d, type2 = %d, type3 = %d, type4 = %d, type5 = %d" %(counter1, counter2, counter3, counter4, counter5)
        params = "board: %d, dimension: %d, filling: %f \n %s \n \n" %(i, dimension, filling, counters)
        parameter_file.write(params)

# ensure proper usage, else inform the user with a print statement
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

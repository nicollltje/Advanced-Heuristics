# board validator
# advanced heuristics
# Nicole and Nicol

import numpy as np
import csv
import sys

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

def loadDataset(filename, cars):

    with open(filename, 'rb') as csvfile:
        lines = csv.reader(csvfile)
        dataset = list(lines)
        # the first line of the imput file is always the dimension
        dimension = dataset[0][0]
        # the rest of the lines contains the parameters needed to create car objects
        for carLine in dataset[1:]:
            car = Car(int(carLine[0]), int(carLine[1]), int(carLine[2]), carLine[3], int(carLine[4]))
            # appends all cars to a list of cars
            cars.append(car)
        return int(dimension)

def validateCar(cars, dimension):

    board = np.zeros(shape=(dimension, dimension), dtype=np.int)

    for car in cars:
        print "validating car"
        print car.x, car.y, car.type
        x = car.x
        y = car.y
        orientation = car.orientation
        type = car.type
        id = car.id

        if board[x, y] == 0:
            board[x,y] = id
            print board
        else:
            print "jdksafklsa Not possible to add this car"
            break

        if type >= 2 and orientation == "H":
            if board[x+1,y] == 0:
                board[x+1, y] = id
            if type >= 3:
                if board[x+2,y] == 0:
                    board[x + 2, y] = id
            if type == 4:
                if board[x+3,y] == 0:
                    board[x+3,y] = id
            if type == 5:
                if board[x, y+1] == 0 and board [x+1, y+1] == 0 and board[x+2, y+1] == 0:
                    board[x, y+1] =id
                    board[x+1, y+1] = id
                    board[x+2, y+1] = id
            else:
                print "Not possible to add this car"
                break

        elif type >= 2 and orientation == "V":
            if board[x,y+1] == 0:
                board[x,y+1] = id
            if type >= 3:
                if board[x, y+2] == 0:
                    board[x,y+2] = id
            if type == 4:
                if board[x, y+3] == 0:
                    board[x,y+3] = id
            if type == 5:
                if board[x +1, y] == 0 and board [x+1, y+1] == 0 and board[x+1, y+2] == 0:
                    board[x+1, y] =id
                    board[x+1, y+1] = id
                    board[x+1, y+2] = id
            else:
                print "Not possible to add this car"
                break

if (len(sys.argv) != 2):
    print "improper usage. USAGE: board_validator.py boardfile.csv"
else:
    cars = []
    filename = str(sys.argv[1])
    dimension = loadDataset(filename, cars)
    validateCar(cars, dimension)


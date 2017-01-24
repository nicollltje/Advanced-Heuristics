# board validator
# advanced heuristics
# Nicole and Nicol

import numpy as np
import csv
import sys
import os

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
        print filename
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

def validateCar(foldername):

    for file in os.listdir('%s' %(foldername)):

        cars = []
        filename = '%s/%s' %(foldername, file)
        dimension = loadDataset(filename, cars)

        board = np.zeros(shape=(dimension, dimension), dtype=np.int)

        for car in cars:
            x = car.x
            y = car.y
            orientation = car.orientation
            type = car.type
            id = car.id

            if type == 1:
                if board[x,y] == 0:
                    board[x,y] = id
                else:
                    os.remove(filename)
                    break

            elif type == 2 and orientation == "H":
                if board[x,y] == 0 and board[x+1,y] == 0:
                    board[x,y] = id
                    board[x+1,y] = id
                else:
                    os.remove(filename)
                    break

            elif type == 2 and orientation == "V":
                if board[x,y] == 0 and board[x,y+1] == 0:
                    board[x,y] = id
                    board[x,y+1] = id
                else:
                    os.remove(filename)
                    break

            elif type == 3 and orientation == "H":
                if board[x,y] == 0 and board[x+1,y] == 0 and board[x+2,y] == 0:
                    board[x,y] = id
                    board[x+1,y] = id
                    board[x+2, y] = id
                else:
                    os.remove(filename)
                    break

            elif type == 3 and orientation =="V":
                if board[x,y] == 0 and board[x,y+1] == 0 and board[x,y+2] == 0:
                    board[x,y] = id
                    board[x,y+1] = id
                    board[x,y+2] = id
                else:
                    os.remove(filename)
                    break

            elif type == 4 and orientation == "H":
                if board[x,y] == 0 and board[x+1,y] == 0 and board[x+2,y] == 0 and board[x+3,y] == 0:
                    board[x,y] = id
                    board[x+1,y] = id
                    board[x+2,y] = id
                    board[x+3,y] = id
                else:
                    os.remove(filename)
                    break

            elif type == 4 and orientation =="V":
                if board[x,y] == 0 and board[x,y+1] == 0 and board[x,y+2] == 0 and board[x,y+3] == 0:
                    board[x, y] = id
                    board[x, y+1] = id
                    board[x, y+2] = id
                    board[x, y+3] = id
                else:
                    os.remove(filename)
                    break

            elif type == 5 and orientation == "H":
                if board[x,y] == 0 and board [x+1,y] == 0 and board[x+2,y] == 0:
                    if board[x,y+1] == 0 and board[x+1,y+1] == 0 and board[x+2,y+1] == 0:
                        board[x,y] = id
                        board[x,y+1] = id
                        board[x+1,y] = id
                        board[x+1,y+1] = id
                        board[x+2,y] = id
                        board[x+2,y+1] = id
                    else:
                        os.remove(filename)
                        break
                else:
                    os.remove(filename)
                    break

            elif type == 5 and orientation =="V":
                if board[x,y] == 0 and board[x,y+1] == 0 and board[x,y+2] == 0:
                    if board[x+1,y] == 0 and board[x+1,y+1] == 0 and board[x+1,y+2] == 0:
                        board[x,y] = id
                        board[x+1,y] = id
                        board[x,y+1] = id
                        board[x+1,y+1] = id
                        board[x,y+2] = id
                        board[x+1,y+2] = id
                    else:
                        os.remove(filename)
                        break
                else:
                    os.remove(filename)
                    break

if (len(sys.argv) != 2):
    print "improper usage. USAGE: board_validator.py foldername"
else:
    # cars = []
    foldername = str(sys.argv[1])
    # dimension = loadDataset(filename, cars)
    # validateCar(cars, dimension, foldername)
    validateCar(foldername)


# Rush Hour Parametrisation
# Names (student id): Nicol Heijtbrink (10580611), Nicole Silverio (10521933)
# Course: Advanced Heuristics
# University of Amsterdam
# Time: January 2017

import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import time
import pylab
import math
import Queue as QueueClass
import copy
import csv
import sys
import os

class Car(object):

    """
    A Car represents a vehicle object with a type, a start coordinate and a certain orientation
    (horizontal or vertical), which can move around the board.
    """

    def __init__(self, x, y, type, orientation, id):

        """
        Initializes a car with a position with coordinates [x, y] on a board with a given type,
        orientation and id.
        :param x, y, length, orientation, id: All parameters are defined in a separate list.
        """

        self.x = x
        self.y = y
        self.type = type
        self.orientation = orientation
        self.id = id

class Game(object):

    """
    A Game represents a board (grid), on which Car objects can move around on.
    The grid is a 2D array of 0's and has a width and length (given by dimension parameter).
    A 0 indicates that position to be empty, while any non-zero value indicates the
    presence of a Car object (where the number indicates which the id of the vehicle).
    """

    def __init__(self, dimension, cars):

        """
        Initializes the grid and creates an empty array with width and length the size of dimension,
        to be filled with given Car objects.
        """

        self.dimension = dimension
        self.cars = cars

        # create a 2D grid consisting of 0's, with type integer
        self.grid = np.zeros(shape=(dimension, dimension), dtype=np.int)

        # keep track of the amount of horizontal and vertical vehicles
        self.horizontals = 0
        self.verticals = 0

        # keep track of amounts of different car types
        self.counter1 = 0
        self.counter2 = 0
        self.counter3 = 0
        self.counter4 = 0
        self.counter5 = 0
        self.counter6 = 0

        # add every given car to the grid
        for car in self.cars:
            self.addCarToGrid(car)

        # create seperate queues for the grid states and cars
        self.gridQueue = QueueClass.Queue(maxsize=0)
        self.carsQueue = QueueClass.Queue(maxsize=0)

        # add the current grid and cars to the corresponding queue
        self.gridQueue.put(self.grid.copy())
        self.carsQueue.put(self.cars)

        # create set to store board states
        self.state_set = set()

        # create key of starting grid state
        start = self.gridToString()

        # create dictionary of grid state (key) paired to corresponding number of performed moves (value)
        self.moves = {}

        # set start key value
        self.moves[start] = 0

        # create dictionary to be able to deduce the fastest path from the winning board
        self.path = {}

        # list that will be filled with all the board states of the fastest path
        self.all_boards_path = []

        # create a start state to check for the end of the path
        self.start_state = start

        # set starting number of iterations to 0
        self.iterations = 0

        self.solvable = "yes"

    def addCarToGrid(self, car):

        """
        Fill the board with a given Car.
        Checks orientation and starting coordinates of Car,
        then fills in the rest of the Car according to the given type.
        :param car: Car object with given x, y, type, orientation and id
        :return: a grid with the car placed on the grid.
        """

        # get coordinates of car
        x = car.x
        y = car.y

        # get the parameters from the car object
        orientation = car.orientation
        type = car.type

        # check for type
        if type == 1:
                # update type counter
                self.counter1 += 1
                self.grid[x, y] = car.id

                # update orientation counters
                if orientation == "H":
                    self.horizontals += 1

                else:
                    self.verticals += 1

        elif type == 2:

            self.counter2 += 1

            if orientation == "H":

                self.horizontals += 1

                self.grid[x, y] = car.id
                self.grid[x + 1, y] = car.id

            elif orientation == "V":

                self.verticals += 1

                self.grid[x, y] = car.id
                self.grid[x, y + 1] = car.id

        elif type == 3:

            self.counter3 += 1
            if orientation == "H":

                self.horizontals += 1

                self.grid[x, y] = car.id
                self.grid[x + 1, y] = car.id
                self.grid[x + 2, y] = car.id

            elif orientation == "V":

                self.verticals += 1

                self.grid[x, y] = car.id
                self.grid[x, y + 1] = car.id
                self.grid[x, y + 2] = car.id

        elif type == 4:

            self.counter4 += 1
            if orientation == "H":

                self.horizontals += 1

                self.grid[x, y] = car.id
                self.grid[x + 1, y] = car.id
                self.grid[x, y + 1] = car.id
                self.grid[x + 1, y + 1] = car.id

            else:

                self.verticals += 1

                self.grid[x, y] = car.id
                self.grid[x + 1, y] = car.id
                self.grid[x, y + 1] = car.id
                self.grid[x + 1, y + 1] = car.id

        elif type == 5:

            self.counter5 += 1
            if orientation == "H":

                self.horizontals += 1

                self.grid[x, y] = car.id
                self.grid[x, y + 1] = car.id
                self.grid[x + 1, y] = car.id
                self.grid[x + 1, y + 1] = car.id
                self.grid[x + 2, y] = car.id
                self.grid[x + 2, y + 1] = car.id

            elif orientation == "V":

                self.verticals += 1

                self.grid[x, y] = car.id
                self.grid[x + 1, y] = car.id
                self.grid[x, y + 1] = car.id
                self.grid[x + 1, y + 1] = car.id
                self.grid[x, y + 2] = car.id
                self.grid[x + 1, y + 2] = car.id

        elif type == 6:

            self.grid[x, y] = car.id
            self.grid[x, y + 1] = car.id
            self.grid[x, y + 2] = car.id

            self.grid[x + 1, y] = car.id
            self.grid[x + 1, y + 1] = car.id
            self.grid[x + 1, y + 2] = car.id

            self.grid[x + 2, y] = car.id
            self.grid[x + 2, y + 1] = car.id
            self.grid[x + 2, y + 2] = car.id

            self.counter6 += 1
            if orientation == "H":
                self.horizontals += 1
            else:
                self.verticals += 1

    def canMoveRight(self, car):

        """
        Checks if the location on the right of the car is within the grid and empty.
        :param car: Car object
        :return: True or False
        """

        # if orientation is not horizontal, moving to the right is not possible
        if car.orientation == "V":
            return False

        length = 0

        if car.type == 1:
            length = 1
        elif car.type == 2 or car.type == 4:
            length = 2
        else:
            length = 3

        #print length

        # check if movement to the right would place Car outside of the grid
        if car.x < (self.dimension - length):

            # check if movement to the right would cause collision between Cars
            if self.grid[car.x + length, car.y] == 0:
                if car.type == 4 or car.type == 5:
                    if self.grid[car.x + length, car.y + 1] == 0:
                        return True
                    else:
                        return False
                elif car.type == 6:
                    if self.grid[car.x + length, car.y + 1] == 0 and self.grid[car.x + length, car.y + 2] == 0:
                        return True
                    else:
                        return False
                else:
                    return True

        return False

    def canMoveLeft(self, car):

        """
        Checks if the location on the left of the car is within the grid and empty.
        :param car: Car object
        :return: True or False
        """

        # if orientation is not horizontal, moving to the left is not possible
        if car.orientation == "V":
            return False

        length = 0

        if car.type == 1:
            length = 1
        elif car.type == 2 or car.type == 4:
            length = 2
        else:
            length = 3

        # check if movement to the left would place Car outside of the grid
        if car.x > 0:

            # check if movement to the left would cause collision between Cars
            if self.grid[car.x - 1, car.y] == 0:
                if car.type == 4 or car.type == 5:
                    if self.grid[car.x - 1, car.y + 1] == 0:
                        return True
                    else:
                        return False
                elif car.type == 6:
                    if self.grid[car.x - 1, car.y + 1] == 0 and self.grid[car.x - 1, car.y + 2] == 0:
                        return True
                    else:
                        return False

                return True
        return False

    def canMoveUp(self, car):

        """
        Checks if the location above the car is within the grid and empty.
        :param car: Car object
        :return: True or False
        """

        # if orientation is not vertical, moving upwards is not possible
        if car.orientation == "H":
            return False

        length = 0

        if car.type == 1:
            length = 1
        elif car.type == 2 or car.type == 4:
            length = 2
        else:
            length = 3

        # check if upward movement would place Car outside of the grid
        if car.y > 0:

            # check if upward movement would cause collision between Cars
            if self.grid[car.x, car.y - 1] == 0:
                if car.type == 4 or car.type == 5:
                    if self.grid[car.x + 1, car.y - 1] == 0:
                        return True
                    else:
                        return False
                elif car.type == 6:
                    if self.grid[car.x + 1, car.y - 1] == 0 and self.grid[car.x + 2, car.y - 1] == 0:
                        return True
                    else:
                        return False
                return True
        return False

    def canMoveDown(self, car):

        """
        Checks if the location underneath the car is within the grid and empty.
        :param car: Car object
        :return: True or False
        """

        # if orientation is not vertical, moving downwards is not possible
        if car.orientation == "H":
            return False

        length = 0

        if car.type == 1:
            length = 1
        elif car.type == 2 or car.type == 4:
            length = 2
        else:
            length = 3

        # check if downward movement would place Car outside of the grid
        if car.y < (self.dimension - length):

            # check if downward movement would cause collision between Cars
            if self.grid[car.x, car.y + length] == 0:
                if car.type == 4 or car.type == 5:
                    if self.grid[car.x + 1, car.y + length] == 0:
                        return True
                    else:
                        return False
                elif car.type == 6:
                    if self.grid[car.x + 1, car.y + length] == 0 and self.grid[car.x + 2, car.y + length] == 0:
                        return True
                    else:
                        return False
                return True
        return False

    def moveRight(self, carId):

        """
        'Moves' a given Car one place to the right on the grid.
        Replaces the 0 on the right side next to the Car with integer idcar
        and replaces the left side of the Car with a 0.
        :return: grid (with 1 moved car compared to previous state of grid).
        """

        # obtain given car out of Car list
        car = self.cars[carId.id - 1]

        length = 0

        if car.type == 1:
            length = 1
        elif car.type == 2 or car.type == 4:
            length = 2
        else:
            length = 3

        # replace right side next to the Car with integer idcar
        self.grid[car.x + length, car.y] = car.id

        # replace the left side of the Car with a 0 (empty)
        self.grid[car.x, car.y] = 0

        if car.type == 4 or car.type == 5 or car.type == 6:
            self.grid[car.x + length, car.y + 1] = car.id
            self.grid[car.x, car.y + 1] = 0
            if car.type == 6:
                self.grid[car.x + length, car.y + 2] = car.id
                self.grid[car.x, car.y + 2] = 0


        # update x coordinate
        car.x = car.x + 1

        # update the list of Cars with moved Car
        self.cars[car.id - 1] = car

    def moveLeft(self, carId):

        """
        'Moves' a given Car 1 place to the left on the grid.
        Replaces the 0 on the left side next to the Car with integer idcar
        and replaces the right side of the Car with a 0.
        :return: grid (with 1 moved car compared to previous state of grid).
        """

        # obtain given Car out of list of Cars
        car = self.cars[carId.id - 1]

        length = 0

        if car.type == 1:
            length = 1
        elif car.type == 2 or car.type == 4:
            length = 2
        else:
            length = 3

        # replace left side next to the Car with integer idcar
        self.grid[car.x - 1, car.y] = car.id

        # replace the right side of the Car with a 0 (empty)
        self.grid[car.x + (length - 1), car.y] = 0

        if car.type == 4 or car.type == 5 or car.type == 6:
            self.grid[car.x - 1, car.y + 1] = car.id
            self.grid[car.x + (length - 1), car.y + 1] = 0
            if car.type == 6:
                self.grid[car.x - 1, car.y + 2] = car.id
                self.grid[car.x + (length - 1), car.y + 2] = 0

        # update x coordinate
        car.x = car.x - 1

        # update the list of Cars with moved Car
        self.cars[car.id - 1] = car

    def moveDown(self, carId):

        """
        'Moves' a given Car 1 place down on the grid.
        Replaces the 0 one place underneath the Car with integer idcar
        and replaces the top of the Car with a 0.
        :return: grid (with 1 moved car compared to previous state of grid).
        """

        # obtain given Car out of list of Cars
        car = self.cars[carId.id - 1]

        length = 0

        if car.type == 1:
            length = 1
        elif car.type == 2 or car.type == 4:
            length = 2
        else:
            length = 3

        # replace one place underneath the Car with integer idcar
        self.grid[car.x, car.y + length] = car.id

        # replace the top of the Car with a 0 (empty)
        self.grid[car.x, car.y] = 0

        if car.type == 4 or car.type == 5 or car.type == 6:
            self.grid[car.x + 1, car.y + length] = car.id
            self.grid[car.x + 1, car.y] = 0
            if car.type == 6:
                self.grid[car.x + 2, car.y + length] = car.id
                self.grid[car.x + 2, car.y] = 0

        # update y coordinate
        car.y = car.y + 1

        # update the list of Cars with moved Car
        self.cars[car.id - 1] = car

    def moveUp(self, carId):

        """
        'Moves' a given Car 1 place up on the grid.
        Replaces the 0 one place above the Car with integer idcar
        and replaces the bottom of the Car with a 0.
        :return: grid (with 1 moved car compared to previous state of grid).
        """

        # obtain given Car out of list of Cars
        car = self.cars[carId.id - 1]

        length = 0

        if car.type == 1:
            length = 1
        elif car.type == 2 or car.type == 4:
            length = 2
        else:
            length = 3

        # replace one place above the Car with integer idcar
        self.grid[car.x, car.y - 1] = car.id

        # replace the bottom of the Car with a 0 (empty)
        self.grid[car.x, car.y + (length - 1)] = 0

        if car.type == 4 or car.type == 5 or car.type ==6:
            self.grid[car.x + 1, car.y - 1] = car.id
            self.grid[car.x + 1, car.y + (length - 1)] = 0
            if car.type == 6:
                self.grid[car.x + 2, car.y - 1] = car.id
                self.grid[car.x + 2, car.y + (length - 1)] = 0

        # update y coordinate
        car.y = car.y - 1

        # update the list of Cars with moved Car
        self.cars[car.id - 1] = car

    def putinQueue(self):

        """
        Copies a grid and inserts it in a queue.
        Deepcopies the list of Cars and puts it in a (different) queue.
        """

        self.gridQueue.put(self.grid.copy())
        self.carsQueue.put(copy.deepcopy(self.cars))

    def gridToString(self):

        """
        Transforms the grid into a string of numbers, representing the state of the board.
        :return: String representing state of board.
        """

        # create variable to store string in
        hash = ""

        # iterate through the grid and place every integer in the hash as a char followed by a comma, creating a string
        for i in range(len(self.grid.T)):
            for j in range(len(self.grid[i])):
                hash += str(self.grid.T[i][j])
                hash += ","
        return hash

    def checkMove(self):

        """
        Checks if a move can be made by trying to put the new state in a set.
        If the length of the set does not change it means there is a duplicate.
        :return: set length (after trying to put the board state in the set)
        """

        # create variable with string of current grid state
        gridString = self.gridToString()

        # add string to set (if string is unique in the set)
        self.state_set.add(gridString)

        # return length of the set
        return len(self.state_set)

    def addToPath(self, parentString):

        """
        Links parent board with their child board in dictionary path.
        Then inserts the current grid in the queue.
        Adds 1 to the value of moves with child_string as key.
        """

        # create and set variable to current state as string
        child_string = self.gridToString()

        # set a key value pair of child_string and parentString in path, with the child being the key and
        # the parent being the value, making it possible to find previous board states
        self.path[child_string] = parentString

        # insert current grid in queue
        self.putinQueue()

        # set number of moves paired with child state to number of moves from parent state + 1
        self.moves[child_string] = 1 + self.moves[parentString]

    def queueAllPossibleMoves(self):

        """
        For every car all directions are checked. If a car can move in a certain direction it is checked if it is
        already in the archive, if so the board state will not be added to the queue. If it is a new unique board
        state after a move, setNewParent will be called to create a queueItem and put this in the priority queue
        and the move will be reset, also to be able to check the opposite direction.
        """

        # set parent_string to the string of the current board state
        parent_string = self.gridToString()

        # iterate through all the cars in self.cars and check for each direction if a move is possible
        for car in self.cars:

            # check if car can move up
            if self.canMoveUp(car):

                # length of set before moving car
                a = Game.checkMove(self)

                # move the car
                self.moveUp(car)

                # length of set after moving car
                b = Game.checkMove(self)

                # if the length of the set has changed after a move
                if a != b:

                    # call addToPath
                    self.addToPath(parent_string)

                # reset move
                self.moveDown(car)

            # do the same as for moving up
            if self.canMoveDown(car):
                a = Game.checkMove(self)
                self.moveDown(car)
                b = Game.checkMove(self)
                if a != b:
                    self.addToPath(parent_string)
                self.moveUp(car)

            # do the same as for moving up, except here you also check for the winning state
            if self.canMoveRight(car):
                a = Game.checkMove(self)
                self.moveRight(car)
                b = Game.checkMove(self)
                if a != b:
                    self.addToPath(parent_string)

                    # check if winning position has been reached. This is only checked here since the
                    # winning state can only be reached by moving the red car to the right
                    if self.grid[self.dimension - 1, self.cars[0].y] == 1:

                        # if winning state has been reached, exit the for loop
                        return False
                self.moveLeft(car)

            # do the same as for moving up
            if Game.canMoveLeft(self, car):
                a = Game.checkMove(self)
                self.moveLeft(car)
                b = Game.checkMove(self)
                if a != b:
                    self.addToPath(parent_string)
                self.moveRight(car)

    def deque(self):

        """
        Prints starting grid and initiates algorithm to solve the board.
        Prints end state of grid, number of moves, number of iterations and time needed to solve board.
        Afterwards the path to the fastest solution is deduced and saved in a list.
        """

        # start clock
        start_time = time.clock()

        # print starting grid
        # print "Starting grid:"
        starting_grid = copy.deepcopy(self.grid.T)
        # print starting_grid
        # print "\n"

        # check if board has reached the winning state, if not, keep executing body

        while self.grid[self.dimension - 1, self.cars[0].y] != 1 and self.solvable == "yes":

            if self.gridQueue.qsize() > 0:

                # obtain first grid and car from corresponding queues
                self.grid = self.gridQueue.get()
                # print "\n"
                # print self.grid.T
                self.cars = self.carsQueue.get()

                # add 1 iteration after each movement
                self.iterations += 1

                # start solving algorithm
                self.queueAllPossibleMoves()

            else:

                self.solvable = "no"

        # calculate time needed to solve board
        # time_duration = time.clock() - start_time
        # hor_ver_ratio = float(self.horizontals) / self.verticals
        while not self.gridQueue.empty():
            self.gridQueue.get()
        while not self.carsQueue.empty():
            self.carsQueue.get()

        types_ratio = "%d:%d:%d:%d:%d:%d" %(self.counter1, self.counter2, self.counter3, self.counter4, self.counter5, self.counter6)
        if self.solvable == "yes":

            print "SOLVED"
            # print "Winning position:"
            # print self.grid.T
            moves_needed = self.moves[self.gridToString()]
            # print "Number of moves needed to finish game: " + str(moves_needed)
            # print "Number of iterations: ", self.iterations
            return self.iterations, moves_needed, self.solvable, self.horizontals, self.verticals, types_ratio, self.counter1, self.counter2, self.counter3, self.counter4, self.counter5, self.counter6
        else:
            print "No solution possible"
            return self.iterations, "-", self.solvable, self.horizontals, self.verticals, types_ratio, self.counter1, self.counter2, self.counter3, self.counter4, self.counter5, self.counter6

        # print "Seconds needed to run program: ", time_duration


        # save the board states for the fastest path from start to finish
        #self.makeBestPath()

    # def makeBestPath(self):
    #
    #     """
    #     Makes a list of every board state in strings of the fastest path from the final state to the start state.
    #     Then each board state, from start to finish, will be converted from a string into a 2d array and saved in a
    #     list, to be able to visualize the path.
    #     """
    #
    #     # make a string of the winning board
    #     path_state = self.gridToString()
    #
    #     # initialise an empty list to fill with all the board states of the fastest path in strings
    #     fastest_path = []
    #
    #     # add the winning state to the list
    #     fastest_path.append(path_state)
    #
    #     # while path_state is not the start state
    #     while path_state != self.start_state:
    #
    #         # the previous board state is the value of the current board state key in self.path
    #         path_previous = self.path.get(path_state)
    #
    #         # add this state to the list
    #         fastest_path.append(path_previous)
    #
    #         # set the current board state to the previous board state
    #         path_state = path_previous
    #
    #     # add the start state to the list
    #     fastest_path.append(self.start_state)
    #
    #     # for all board states of the fastest path, but from start to finish
    #     for board_string in reversed(fastest_path):
    #
    #         # initialise an empty list to fill with the rows of the board
    #         board_path = []
    #
    #         # initialise y to zero
    #         y = 0
    #
    #         # split the board state by commas
    #         board_split = board_string.split(",")
    #
    #         # create as many rows as the dimension
    #         for i in range(1, self.dimension + 1):
    #
    #             x = self.dimension * i
    #
    #             # a row of the board is the split string, index y to x
    #             board_row = board_split[y:x]
    #
    #             # append this row to the list
    #             board_path.append(board_row)
    #
    #             # set y to x
    #             y = x
    #
    #         # make a 2d array of all the rows
    #         board_path = np.vstack(board_path)
    #
    #         # make the 2d array into an numpy array with integers
    #         board_path = np.array(board_path, dtype=int)
    #
    #         # add this board to the list of all the boards in the path
    #         self.all_boards_path.append(board_path)

def loadDataset(directory, filename, cars):
    """
    Reads an input file and converts this to usable game parameters
    :param filename: the input file that needs to be read
    :param cars: the list of cars that the cars need to be added to
    :return: the dimension as an int
    """

    path = "%s/%s" %(directory, filename)

    with open(path, 'rb') as csvfile:

        print "opened", path

        del cars[:]
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

# if the usage is incorrect the user is informed with a print statement
if (len(sys.argv) != 2):
    print('Error, USAGE: program.py foldername')

# if 2 commandline arguments are given the algorithm is run with creating an output file
else:
    try:
        cars = []

        directory = str(sys.argv[1])

        total_boards = 0
        solved = 0
        iterations = 0
        moves = 0
        horizontal = 0
        vertical = 0
        type1 = 0
        type2 = 0
        type3 = 0
        type4 = 0
        type5 = 0
        type6 = 0

        filename = "outputfiles/%s-output.csv" %(directory)

        with open(filename, 'wb') as csvfile:
            outputwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

            # write the board size as the first line of the csv
            outputwriter.writerow(["filename", "iterations", "moves", "solved", "H/V", "types", "dimension"])

            for filename in os.listdir(directory):
                print filename
                if filename.endswith(".csv"):
                    total_boards += 1
                    dimension = loadDataset(directory, filename, cars)
                    game = Game(dimension, cars)
                    result = game.deque()
                    if result[2] == "yes":
                        solved += 1.0
                        iterations += result[0]
                        moves += result[1]
                        horizontal += result[3]
                        vertical += result[4]
                        type1 += result[6]
                        type2 += result[7]
                        type3 += result[8]
                        type4 += result[9]
                        type5 += result[10]
                        type6 += result[11]
                    hor_ver = "%d:%d" %(result[3], result[4])
                    outputwriter.writerow([filename, result[0], result[1], result[2], hor_ver, result[5], dimension])

                else:
                    break

            percentage_solved = float(solved)/total_boards
            percentage_solved = percentage_solved
            mean_its = iterations/float(solved)
            mean_moves = moves/float(solved)
            mean_hv_ratio = "%d:%d" %(horizontal,vertical)
            mean_type_ratio = "%d:%d:%d:%d:%d:d" %(type1, type2, type3, type4, type5, type6)
            outputwriter.writerow(["mean", mean_its, mean_moves, percentage_solved, mean_hv_ratio, mean_type_ratio, "dim"])
            print "Percentage solvable: %2f. Mean number of iterations: %f. Mean number of moves: %f" %(percentage_solved, mean_its, mean_moves)

    except ValueError:
        print "no proper input was given, try again"
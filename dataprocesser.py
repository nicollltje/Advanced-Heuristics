import csv
import sys
import traceback
import math

def iterationsForUnsolved(filename):
    with open(filename, 'r') as csvfile:
        outputreader = csv.reader(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        iterations_total = 0
        iterations_total_solved = 0
        amount_of_USboards = 0
        amount_of_Sboards = 0

        lines = csv.reader(csvfile)
        dataset = list(lines)

        for row in dataset[1:]:
            # print row[3]

            if row[3] == "no":
                # print "hoi"
                iterations_total += int(row[1])
                amount_of_USboards += 1
            elif row[3] == 'yes':
                iterations_total_solved += int(row[1])
                amount_of_Sboards += 1


        print "Unsolved", iterations_total, amount_of_USboards
        print (float(iterations_total)/amount_of_USboards)
        print "Solved", iterations_total_solved, amount_of_Sboards
        print (float(iterations_total_solved)/amount_of_Sboards)

def std(filename):
    with open(filename, 'r') as csvfile:
        outputreader = csv.reader(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        moves = []
        board = 0

        close_std = 0

        mean_moves = 0

        for row in outputreader:
            if row[0] == "mean":
                mean_moves = float(row[2])
            elif row[3] == "yes":
                board += 1
                move = float(row[2])
                difference = move - mean_moves
                almost_std = difference * difference
                moves.append(almost_std)


        for item in moves:
            close_std += item

        stddev = math.sqrt(close_std/board)

        print "STD", stddev

if (len(sys.argv) != 2):
    print "improper usage. USAGE: dataprocesser.py filename"
else:
    try:
        filename = str(sys.argv[1])
        iterationsForUnsolved(filename)
        # std(filename)
    except ValueError:

        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        print ''.join('!! ' + line for line in lines)  # Log it or whatever here
        # if the input is invalid inform the user with a print statement
        print("boards and dimension should be of type integer")


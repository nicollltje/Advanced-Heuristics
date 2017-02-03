import csv
import sys
import traceback

def iterationsForUnsolved(filename):
    with open(filename, 'r') as csvfile:
        outputreader = csv.reader(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        iterations_total = 0
        amount_of_USboards = 0

        for row in outputreader:
            if row[3] == "no":
                iterations_total += int(row[1])
                amount_of_USboards += 1

        print iterations_total, amount_of_USboards
        print (float(iterations_total)/amount_of_USboards)

if (len(sys.argv) != 2):
    print "improper usage. USAGE: dataprocesser.py filename"
else:
    try:
        filename = str(sys.argv[1])
        iterationsForUnsolved(filename)

    except ValueError:

        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        print ''.join('!! ' + line for line in lines)  # Log it or whatever here
        # if the input is invalid inform the user with a print statement
        print("boards and dimension should be of type integer")


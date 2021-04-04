import csv
import sys

#print('Number of arguments:', len(sys.argv), 'arguments.')
#print('Argument List:', str(sys.argv))

with open('/Users/todlarson/workspace/networking/simplelookups/data.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

if len(sys.argv) == 1:
    for row in data:
        print("{} - My command {} second command {}".format(row[0],row[1],row[2]))
        print("{} - My command {} second command {}".format(row[0],row[4],row[5]))
elif len(sys.argv) == 2:
    found = False
    for row in data:
        if row[0] == sys.argv[1]:
            found = True
            print(row[0])
            print("My command {} second command {}".format(row[1],row[2]))
            print("My command {} second command {}".format(row[4],row[5]))
    if found == False:
        print("Input argument {} not found".format(sys.argv[1]))
else:
    print("Error - bad input arguments")

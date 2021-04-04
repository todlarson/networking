import csv

with open('/Users/todlarson/workspace/networking/simplelookups/data.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

print(data)
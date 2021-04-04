import csv

with open('data.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

print(data)
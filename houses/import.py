# TODO
import cs50
import csv
from sys import argv

if len(argv) != 2:
    print('Usage: python import.py [NAME OF CSV FILE]')
    exit(1)

db = cs50.SQL("sqlite:///students.db")

with open(argv[-1], 'r') as chars:

    reader = csv.DictReader(chars)

    for row in reader:

        current = row['name'].split()

        first, middle, last = current[0], current[1] if len(current) == 3 else None, current[-1]
        house = row['house']
        birth = row['birth']

        db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)", first, middle, last, house, birth)

print("Done INserting")
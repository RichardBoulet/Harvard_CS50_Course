# Program

from cs50 import get_string
from sys import argv

if len(argv) != 3:
    print('Error')
    exit(1)

csv = open(argv[1], 'r')


dna = []
ppl = {}

for index, row in enumerate(csv):
    if index == 0:
        dna = [dna for dna in row.strip().split(',')][1:]
    else:
        current_row = row.strip().split(',')
        ppl[current_row[0]] = [int(x) for x in current_row[1:]]




dna_strand = open(argv[2], 'r').read()

final_strands = []

for strand in dna:

    i = 0
    max_strand = -1
    current_max = 0

    while i < len(dna_strand):
        window = dna_strand[i : i + len(strand)]

        if window == strand:
            current_max += 1
            max_strand = max(max_strand, current_max)
            i += len(strand)
        else:
            current_max = 0
            i += 1

    final_strands.append(max_strand)

for name, data in ppl.items():
    if data == final_strands:
        print(name)
        exit(0)


print('No match')
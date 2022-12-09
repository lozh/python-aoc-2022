#!/usr/bin/env /usr/bin/python3

import sys

lookup = {
    ('A', 'X'): 4,
    ('A', 'Y'): 8,
    ('A', 'Z'): 3,
    ('B', 'X'): 1,
    ('B', 'Y'): 5,
    ('B', 'Z'): 9,
    ('C', 'X'): 7,
    ('C', 'Y'): 2,
    ('C', 'Z'): 6
}

def tuples_to_scores(tuples, lookup):
    return map(lookup.get, tuples)

def input_to_tuples(lines):
    return map(line_to_tuple, lines)

def line_to_tuple(line):
    return (line[0], line[2])


stdin = sys.stdin.read().splitlines()

tuples = input_to_tuples(stdin)
scores = tuples_to_scores(tuples, lookup)

print(sum(scores))



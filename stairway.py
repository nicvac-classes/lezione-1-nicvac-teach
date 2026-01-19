#!/usr/bin/env python3
# NOTE: it is recommended to use this even if you don't understand the following code.

import sys

# uncomment the two following lines if you want to read/write from files
# sys.stdin = open('stairway_input1.txt')
sys.stdin = open('input.txt')
sys.stdout = open('output.txt', 'w')

N = int(input().strip())

B = 0

# INSERT YOUR CODE HERE
i = 1
while i <= N:
    B += i
    i += 1


print(B)

sys.stdout.close()


import os
import pickle
import sys
import string
import re

data_path = sys.argv[1]


A = dict()
B = dict()
Pi = dict ()

file1 = open(data_path, 'r')
Lines = file1.readlines()

# Strips the newline character
for line in Lines:
    print(line.strip())
    print("Line{}: {}".format(count, line.strip()))
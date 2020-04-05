
import os
import pickle
import sys
import string
import re

data_path = sys.argv[1]
# data_path = "data/hmm-training-data/it_isdt_train_tagged.txt"

A = dict()
B = dict()
Pi = dict ()

file1 = open(data_path, 'r')
Lines = file1.readlines()

# Strips the newline character
for line in Lines:
    print("-------------------")
    line = line.strip()
    tokens = line.split(" ")
    print(line)
    print(tokens)
    print("-------------------")

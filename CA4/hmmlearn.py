
import os
import pickle
import sys
import string
import re

data_path = sys.argv[1]
# data_path = "data/hmm-training-data/it_isdt_train_tagged.txt"

tag_count_dict = dict()
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
    prev_tag = False
    for token in tokens:
        splitted_token = token.rsplit("/", 1)
        tag = splitted_token[1]
        word = splitted_token[0]

        if tag not in tag_count_dict:
            tag_count_dict[tag] = 1
        else:
            tag_count_dict[tag] += 1

        if not prev_tag:
            if tag not in Pi:
                Pi[tag] = 1
            else:
                Pi[tag] += 1
        else:
            if tag not in A:
                A[tag] = {prev_tag : 1}
            else:
                if prev_tag not in A[tag]:
                    A[tag][prev_tag] = 1
                else:
                    A[tag][prev_tag] += 1

        if tag not in B:
            B[tag] = {word:1}
        else:
            if word not in B[tag]:
                B[tag][word] = 1
            else:
                B[tag][word] += 1



        prev_tag = tag
    print("-------------------")

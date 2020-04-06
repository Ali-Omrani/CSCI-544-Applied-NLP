import os
import pickle
import sys
import string
import re
import numpy as np

data_path = sys.argv[1]
path_to_pickle = "dict.pickle"


with open(path_to_pickle, 'rb') as f:
    probs = pickle.load(f)


    A = probs["A"]
    B = probs["B"]
    Pi = probs["Pi"]
    tag_count_dict = probs["tag_count_dict"]
    word_list = probs["word_list"]
    print(A)
    print(B)
    print(Pi)

    file1 = open(data_path, 'r')
    Lines = file1.readlines()

    # Strips the newline character
    for line in Lines:
        print("-------------------")
        line = line.strip()
        tokens = line.split(" ")
        print(line)
        print(tokens)

        diff_tag_count = len(tag_count_dict)
        c = 0
        index_tag_mapping_dict = dict()
        for tag in tag_count_dict:
            index_tag_mapping_dict[c] = tag
            c += 1

        sequence_length = len(tokens)
        diff_word_count = len(word_list)
        viterbi = np.zeros((diff_tag_count, sequence_length))
        print(viterbi.shape)

        for i in range(diff_tag_count):
            corresponding_tag = index_tag_mapping_dict[i]
            if corresponding_tag not in Pi:
                viterbi[i][0] = 0
                continue
            else:
                viterbi[i][0] = Pi[corresponding_tag]
                if corresponding_tag in B:
                    if tokens[0] in B[corresponding_tag]:
                        viterbi[i][0] *= B[corresponding_tag][tokens[0]]
                    else:
                        viterbi[i][0] *= 1/(tag_count_dict[corresponding_tag]+diff_word_count)
                else:
                    #TODO
                    viterbi[i][0] = 0







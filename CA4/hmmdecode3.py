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

    file1 = open(data_path, 'r')
    Lines = file1.readlines()

    # Strips the newline character
    for line in Lines:
        print("-------------------")
        line = line.strip()
        tokens = line.split(" ")
        print(line)
        diff_tag_count = len(tag_count_dict)
        c = 0
        index_tag_mapping_dict = dict()
        for tag in tag_count_dict:
            index_tag_mapping_dict[c] = tag
            c += 1

        sequence_length = len(tokens)
        diff_word_count = len(word_list)
        num_of_tags = len(tag_count_dict)
        viterbi = np.zeros((diff_tag_count, sequence_length))
        backpointers = np.zeros((diff_tag_count, sequence_length))

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


        for i in range(1, sequence_length):
            for j in range(diff_tag_count):
                corresponding_tag = index_tag_mapping_dict[j]
                max_prob = 0
                for k in range(diff_tag_count):
                    prev_tag = index_tag_mapping_dict[k]
                    #TODO check if each exists!
                    if tokens[i] not in B[corresponding_tag]:
                        B[corresponding_tag][tokens[i]] = 1/(tag_count_dict[tag]+diff_word_count)
                    if corresponding_tag not in A[prev_tag]:
                        A[prev_tag][corresponding_tag] = 1/(tag_count_dict[prev_tag]+num_of_tags)

                    temp_prob = viterbi[k][i-1] * A[prev_tag][corresponding_tag] * B[corresponding_tag][tokens[i]]

                    if temp_prob > max_prob:
                        max_prob = temp_prob
                        backpointers[j][i] = k

                viterbi[j][i] = max_prob


#       find the final top viterbi value
        final_max = 0
        best_final_state = 0
        for i in range(diff_tag_count):
            if viterbi[i][sequence_length-1] > final_max:
                final_max = viterbi[i][sequence_length-1]
                best_final_state = i


#       backtrack
        final_tag_list = []
        final_tag_list.append(index_tag_mapping_dict[best_final_state])
        prev_best_tag = best_final_state
        for i in range (sequence_length-2, -1, -1):
            new_tag = backpointers[prev_best_tag][i]
            final_tag_list.append(index_tag_mapping_dict[int(new_tag)])
            prev_best_tag = int(new_tag)

        result_str = ""
        for i in range(sequence_length):
            result_str += tokens[i]+"/"+final_tag_list[sequence_length-1-i]
            if i!=sequence_length-1:
                result_str += " "

        print(result_str)


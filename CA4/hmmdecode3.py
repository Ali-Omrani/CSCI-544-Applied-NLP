import os
import pickle
import sys
import string
import re

path_to_pickle = "dict.pickle"


with open(path_to_pickle, 'rb') as f:
    probs = pickle.load(f)


    A = probs["A"]
    B = probs["B"]
    Pi = probs["Pi"]

    print(A)
    print(B)
    print(Pi)

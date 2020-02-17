import os
import pickle
import math
import csv

def read_probs(path_to_pickle):
    with open(path_to_pickle, 'rb') as f:
        return pickle.load(f)

def get_text_file_paths(dir_paths):
    text_files = []
    for dir_path in dir_paths:
        # r=root, d=directories, f = files
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if file.endswith(".txt"):
                    if os.path.join(root, file) not in text_files:
                        text_files.append(os.path.join(root, file))
    return text_files


def get_class_prob(file_path, class_probs):
    file = open(file_path, mode='r')
    text = file.read()
    text = text.replace("\n", "").replace("(", "").replace(")", "").replace(".", "").replace(";", "").replace(",", "")
    tokens = text.split(" ")
    UK = 0
    prob = 0

    for token in tokens:
        if token in class_probs:
            prob += math.log(class_probs[token])
        else:
            UK += 1

    return prob

# probs = {"ali": 0.2, "mamad": 0.3}

pred_dir_path = ["data/positive_polarity"]


text_file_paths = get_text_file_paths(pred_dir_path)

probs_path = "test_dump.pkl"

probs = read_probs(probs_path)

pred_file_path = text_file_paths[2]
print(pred_file_path)
predict_pos_neg(pred_file_path, probs, probs)
# for text_file_path in text_file_paths:

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

probs_paths = {"positive":"positive.pkl", "negative":"negative.pkl", "truthful": "truthful.pkl", "deceptive": "deceptive.pkl"}
probs = {}
for key in probs_paths:
    probs[key] = read_probs(probs_paths[key])




pred_dir_path = ["data/positive_polarity"]
text_file_paths = get_text_file_paths(pred_dir_path)
for pred_file_path in text_file_paths:
    pos_prob = get_class_prob(pred_file_path, probs["positive"])
    neg_prob = get_class_prob(pred_file_path, probs["negative"])
    truthful_prob = get_class_prob(pred_file_path, probs["truthful"])
    deceptive_prob = get_class_prob(pred_file_path, probs["deceptive"])

    label1 = ""
    label2 = ""

    print("p", pos_prob, "n", neg_prob, "t", truthful_prob, "d", deceptive_prob)


    if pos_prob > neg_prob:
        label1 = "positive"
    else:
        label1 = "negative"

    if truthful_prob > deceptive_prob:
        label2 = "truthful"
    else:
        label2 = "deceptive"

    print(label1, label2, pred_file_path)


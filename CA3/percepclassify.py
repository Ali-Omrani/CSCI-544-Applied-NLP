import os
import pickle
import math
import csv
import sys
import string
import re

STOP_WORDS = ["i","me","my","myself","we","our","ours","ourselves","you","your","yours","yourself","yourselves","he","him","his","himself","she","her","hers","herself","it","its","itself","they","them","their","theirs","themselves","what","which","who","whom","this","that","these","those","am","is","are","was","were","be","been","being","have","has","had","having","do","does","did","doing","a","an","the","and","but","if","or","because","as","until","while","of","at","by","for","with","about","against","between","into","through","during","before","after","above","below","to","from","up","down","in","out","on","off","over","under","again","further","then","once","here","there","when","where","why","how","all","any","both","each","few","more","most","other","some","such","no","nor","not","only","own","same","so","than","too","very","s","t","can","will","just","don","should","now"]

def read_weights(path_to_pickle):
   #print("loading ", path_to_pickle)
    with open(path_to_pickle, 'rb') as f:
        return pickle.load(f)

def get_bag_of_words(tokens):
    bag_of_words = {}
    for token in tokens:
        if token in bag_of_words:
            bag_of_words[token] += 1
        else:
            bag_of_words[token] = 1

    return bag_of_words

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


def classify(pred_file_path, model_weights, model_bias, vocab):
    file = open(pred_file_path, mode='r')
    text = file.read()
   #print(text)
    translator = str.maketrans("", "", string.punctuation)
    text = text.translate(translator).lower()
    tokens = []
    for item in re.split("\W+", text):
        if item not in STOP_WORDS:
            tokens.append(item)
    x = get_bag_of_words(tokens)
    activation = 0
    for word in x:
        activation += x[word] * model_weights[word]
    activation += model_bias

    # TODO : check for sign
    if activation >= 0:
        return 1
    else:
        return -1


vocab = []
with open("vocab.pkl", 'rb') as f:
    vocab = pickle.load(f)
# print("vocab is:")
# print(vocab)

# TODO: add other weights
counts_paths = {"pos_neg":"pos_neg.pkl"}
counts = {}
for key in counts_paths:
    counts[key] = read_weights(counts_paths[key])
   #print(key)
   #print(counts[key])

model_path = sys.argv[1]
pred_dir_path = [sys.argv[2]]
text_file_paths = get_text_file_paths(pred_dir_path)
outF = open("nboutput.txt", "w")
for pred_file_path in text_file_paths:

    if "README" in pred_file_path:
        continue
    # print("classifing ", pred_file_path)

    pos_prob = get_class_prob(pred_file_path, counts["positive"], vocab)
    neg_prob = get_class_prob(pred_file_path, counts["negative"], vocab)
    truthful_prob = get_class_prob(pred_file_path, counts["truthful"], vocab)
    deceptive_prob = get_class_prob(pred_file_path, counts["deceptive"], vocab)

    label1 = ""
    label2 = ""

    ##print("p", positive_prob, "n", neg_prob, "t", truthful_prob, "d", deceptive_prob)


    if pos_prob > neg_prob:
        label1 = "positive"
    else:
        label1 = "negative"

    if truthful_prob > deceptive_prob:
        label2 = "truthful"
    else:
        label2 = "deceptive"

    ##print(label1, label2, pred_file_path)

    outF.write(label2+" "+label1+" "+pred_file_path+"\n")


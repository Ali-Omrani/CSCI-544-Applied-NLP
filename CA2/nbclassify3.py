import os
import pickle
import math
import csv
import sys
import string
import re
STOP_WORDS = ["i","me","my","myself","we","our","ours","ourselves","you","your","yours","yourself","yourselves","he","him","his","himself","she","her","hers","herself","it","its","itself","they","them","their","theirs","themselves","what","which","who","whom","this","that","these","those","am","is","are","was","were","be","been","being","have","has","had","having","do","does","did","doing","a","an","the","and","but","if","or","because","as","until","while","of","at","by","for","with","about","against","between","into","through","during","before","after","above","below","to","from","up","down","in","out","on","off","over","under","again","further","then","once","here","there","when","where","why","how","all","any","both","each","few","more","most","other","some","such","no","nor","not","only","own","same","so","than","too","very","s","t","can","will","just","don","should","now"]


def read_counts(path_to_pickle):
    print("loading ", path_to_pickle)
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


def get_class_prob(file_path, class_counts, vocab):
    file = open(file_path, mode='r')
    text = file.read()
    print(text)
    translator = str.maketrans("", "", string.punctuation)
    text = text.translate(translator).lower()
    tokens = []
    for item in re.split("\W+", text):
        if item not in STOP_WORDS:
            tokens.append(item)
    UK = 0
    prob = 0
    total = sum(class_counts.values())
    print("inside get_class_probs")
    print(class_counts)
    print(tokens)
    for token in tokens:
        if token not in vocab:
            print("not in vocab")
            continue
        if token in class_counts:
            print("found in vocab", class_counts[token])
            prob += math.log((class_counts[token] + 1)/(total + len(vocab)))
            print("prob till now", prob)
        else:
            print("not found in class => prob is :", math.log(1/(total+len(vocab))))
            prob += math.log(1/(total+len(vocab)))

    return prob



vocab = []
with open("vocab.pkl", 'rb') as f:
    vocab = pickle.load(f)
print("vocab is:")
print(vocab)

counts_paths = {"positive":"positive.pkl", "negative":"negative.pkl", "truthful": "truthful.pkl", "deceptive": "deceptive.pkl"}
counts = {}
for key in counts_paths:
    counts[key] = read_counts(counts_paths[key])
    print(key)
    print(counts[key])

pred_dir_path = [sys.argv[1]]
# pred_dir_path = ["data/positive_polarity"]
text_file_paths = get_text_file_paths(pred_dir_path)
outF = open("nboutput.txt", "w")
for pred_file_path in text_file_paths:

    pos_prob = get_class_prob(pred_file_path, counts["positive"], vocab)
    neg_prob = get_class_prob(pred_file_path, counts["negative"], vocab)
    truthful_prob = get_class_prob(pred_file_path, counts["truthful"], vocab)
    deceptive_prob = get_class_prob(pred_file_path, counts["deceptive"], vocab)

    label1 = ""
    label2 = ""

    # print("p", positive_prob, "n", neg_prob, "t", truthful_prob, "d", deceptive_prob)


    if pos_prob > neg_prob:
        label1 = "positive"
    else:
        label1 = "negative"

    if truthful_prob > deceptive_prob:
        label2 = "truthful"
    else:
        label2 = "deceptive"

    # print(label1, label2, pred_file_path)

    outF.write(label1+" "+label2+" "+pred_file_path+"\n")


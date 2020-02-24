# this is token based classification
import os
import pickle
import sys
import string
import re

STOP_WORDS = ["i","me","my","myself","we","our","ours","ourselves","you","your","yours","yourself","yourselves","he","him","his","himself","she","her","hers","herself","it","its","itself","they","them","their","theirs","themselves","what","which","who","whom","this","that","these","those","am","is","are","was","were","be","been","being","have","has","had","having","do","does","did","doing","a","an","the","and","but","if","or","because","as","until","while","of","at","by","for","with","about","against","between","into","through","during","before","after","above","below","to","from","up","down","in","out","on","off","over","under","again","further","then","once","here","there","when","where","why","how","all","any","both","each","few","more","most","other","some","such","no","nor","not","only","own","same","so","than","too","very","s","t","can","will","just","don","should","now"]
MAX_ITER = 100

data_path = sys.argv[1]

# test_fold_name = "fold1"



positive_dir = [os.path.join(data_path, "positive_polarity")]
negative_dir = [os.path.join(data_path, "negative_polarity")]

truthful_dirs = [os.path.join(positive_dir[0], "truthful_from_TripAdvisor"), os.path.join(negative_dir[0], "truthful_from_Web")]
deceptive_dirs = [os.path.join(positive_dir[0], "deceptive_from_MTurk"), os.path.join(negative_dir[0], "deceptive_from_MTurk")]


def get_text_file_paths(dir_paths):
    text_files = []
    for dir_path in dir_paths:
        # print("exploring ", dir_path)
        # r=root, d=directories, f = files
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if "README" in file:
                    continue
                if file.endswith(".txt"):
                    text_files.append(os.path.join(root, file))
    return text_files

file_paths_dict = {}

file_paths_dict["positive"] = get_text_file_paths(positive_dir)

file_paths_dict["negative"] = get_text_file_paths(negative_dir)
file_paths_dict["truthful"] = get_text_file_paths(truthful_dirs)
file_paths_dict["deceptive"] = get_text_file_paths(deceptive_dirs)


def get_texts(file_paths):
    texts = []
    for file_path in file_paths:
        # print("reading ", file_path)
        file = open(file_path, mode='r')
        all_of_it = file.read()
        # print(all_of_it)
        texts.append(all_of_it)
    return texts



def get_tokens(text):
    tokens = []
    translator = str.maketrans("", "", string.punctuation)
    text = text.translate(translator).lower()
    for item in re.split("\W+", text):
        if item not in STOP_WORDS:
            tokens.append(item)

        # text = text.replace("\n", "").replace("(", "").replace(")", "").replace(".", "").replace(";", "").replace(",",                                                                                          "")
        # tokens.extend(text.split(" "))
    return tokens

def get_bag_of_words(tokens):
    bag_of_words = {}
    for token in tokens:
        if token in bag_of_words:
            bag_of_words[token] += 1
        else:
            bag_of_words[token] = 1

    return bag_of_words

def get_probs(bag_of_words, vocab_size):
    probs = {}
    total = sum(bag_of_words.values())
    for key in bag_of_words:
        probs[key] = (bag_of_words[key] + 1)/(total + vocab_size)
    return probs


def save_to_pickle(obj, filename):
    with open(filename+'.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


categories = ["positive", "negative", "truthful", "deceptive"]
vocab = []
bag_of_words = {}
x_pos_neg = []
y_pos_neg = []
x_truth_deceptive = []
y_truth_deceptive = []

for category in categories:
    print(category)
    texts = get_texts(file_paths_dict[category])
    for text in texts:
        tokens = get_tokens(text)
        bag_of_words = get_bag_of_words(tokens)
        if category == "positive":
            y_pos_neg.append(1)
            x_pos_neg.append(bag_of_words)
        elif category == "negative":
            y_pos_neg.append(-1)
            x_pos_neg.append(bag_of_words)
        elif category == "truthful":
            y_truth_deceptive.append(1)
            x_truth_deceptive.append(bag_of_words)
        else:
            y_truth_deceptive.append(-1)
            x_truth_deceptive.append(bag_of_words)

        for word in bag_of_words:
            if word not in vocab:
                vocab.append(word)

# print(x_pos_neg[:2])
# print(y_pos_neg[:2])
# print(x_truth_deceptive[:2])
# print(y_truth_deceptive[:2])

# -------------------------- perceptron learning -----------------------



def train(max_iter, input_x, input_y):
    weights = {}
    for word in vocab:
        weights[word] = 0
    bias = 0
    for iteration in range(max_iter):
        # TODO: permute
        indices = range(len(input_x))
        for index in indices:
            x = input_x[index]
            y = input_y[index]
            activation = 0
            for word in x:
                activation += x[word]*weights[word]
            activation += bias

            if y*activation <= 0:
                print("updating for y = ", y)
                for word in x:
                    weights[word] += y*x[word]
                bias += y
    weights["MODEL_BIAS"] = bias
    return weights


# TODO: save to text
pos_neg_weights = train(MAX_ITER, x_pos_neg, y_pos_neg)
save_to_pickle(pos_neg_weights, "pos_neg")
truth_deceptive_weights = train(MAX_ITER, x_truth_deceptive, y_truth_deceptive)
save_to_pickle(truth_deceptive_weights, "truth_deceptive")

def train_avg(max_iter, input_x, input_y):
    weights = {}
    u = {}
    for word in vocab:
        weights[word] = 0
        u[word] = 0
    bias = 0
    betha = 0
    c = 1
    for iteration in range(max_iter):
        # TODO: permute
        indices = range(len(input_x))
        for index in indices:
            x = input_x[index]
            y = input_y[index]
            activation = 0
            for word in x:
                activation += x[word] * weights[word]
            activation += bias

            if y * activation <= 0:
                for word in x:
                    weights[word] += y * x[word]
                    u[word] += y * x[word] * c
                bias += y
                betha += y * c
            c += 1
    for word in weights:
        weights[word] = weights[word]-(u[word]/c)
    weights["MODEL_BIAS"] = bias - (betha/c)
    return weights

# TODO : save to text
pos_neg_weights = train_avg(MAX_ITER, x_pos_neg, y_pos_neg)
save_to_pickle(pos_neg_weights, "pos_neg_avg")
truth_deceptive_weights = train_avg(MAX_ITER, x_truth_deceptive, y_truth_deceptive)
save_to_pickle(truth_deceptive_weights, "truth_deceptive_avg")


save_to_pickle(vocab, "vocab")
#
#
#
# for category in categories:
#     # probs = get_probs(bag_of_words[category], len(vocab))
#     save_to_pickle(bag_of_words[category], category)
# this is token based classification
import os
import pickle
import sys
import string
import re



data_path = sys.argv[1]

# test_fold_name = "fold1"

positive_dir = [os.path.join(data_path, "positive_polarity")]
negative_dir = [os.path.join(data_path, "negative_polarity")]

truthful_dirs = [os.path.join(positive_dir[0], "truthful_from_TripAdvisor"), os.path.join(negative_dir[0], "truthful_from_Web")]
deceptive_dirs = [os.path.join(positive_dir[0], "deceptive_from_MTurk"), os.path.join(negative_dir[0], "deceptive_from_MTurk")]


def get_text_file_paths(dir_paths):
    text_files = []
    for dir_path in dir_paths:
        print("exploring ", dir_path)
        # r=root, d=directories, f = files
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if file.endswith(".txt"):
                    text_files.append(os.path.join(root, file))
    return text_files

file_paths_dict = {}

file_paths_dict["positive"] = get_text_file_paths(positive_dir)

file_paths_dict["negative"] = get_text_file_paths(negative_dir)
file_paths_dict["truthful"] = get_text_file_paths(truthful_dirs)
file_paths_dict["deceptive"] = get_text_file_paths(deceptive_dirs)
for path in file_paths_dict["deceptive"]:
    print(path)


def get_texts(file_paths):
    texts = []
    for file_path in file_paths:
        # print("reading ", file_path)
        file = open(file_path, mode='r')
        all_of_it = file.read()
        # print(all_of_it)
        texts.append(all_of_it)
    return texts



def get_tokens(texts):
    tokens = []
    for text in texts:
        translator = str.maketrans("", "", string.punctuation)
        text = text.translate(translator).lower()
        tokens.extend(re.split("\W+", text))

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

def get_probs(bag_of_words):
    probs = {}
    total = sum(bag_of_words.values())
    for key in bag_of_words:
        probs[key] = bag_of_words[key]/total
    return probs


def save_to_pickle(obj, filename):
    with open(filename+'.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


categories = ["positive", "negative", "truthful", "deceptive"]
for category in categories:
    texts = get_texts(file_paths_dict[category])
    tokens = get_tokens(texts)
    bag_of_words = get_bag_of_words(tokens)
    pos_probs = get_probs(bag_of_words)
    save_to_pickle(pos_probs, category)
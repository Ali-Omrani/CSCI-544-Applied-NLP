import os
from os import walk
import csv
import pickle

data_path = "data"
test_fold_name = "fold1"
result_path = "test_dump"
# print(os.listdir(data_path))
# h1 = []
# for path in os.listdir(data_path):
#     temp_path = os.path.join(data_path,path)
#     if os.path.isdir(temp_path):
#         print(temp_path)
#         h1.append(temp_path)
#         print(h1)

positive_dir = [os.path.join(data_path, "positive_polarity")]
negative_dir = [os.path.join(data_path, "negative_polarity")]

truthful_dirs = [os.path.join(positive_dir[0], "truthful_from_TripAdvisor"), os.path.join(negative_dir[0], "truthful_from_TripAdvisor")]
deceptive_dirs = [os.path.join(positive_dir[0], "deceptive_from_MTurk"), os.path.join(negative_dir[0], "deceptive_from_MTurk")]

print(positive_dir)


def get_text_file_paths(dir_paths):
    text_files = []
    for dir_path in dir_paths:
        print("exploring", dir_path)
        # r=root, d=directories, f = files
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if file.endswith(".txt"):
                    if os.path.join(root, file) not in text_files:
                        text_files.append(os.path.join(root, file))
    return text_files

category = "positive"
file_paths_dict = {}

file_paths_dict["positive"] = get_text_file_paths(positive_dir)
file_paths_dict["negative"] = get_text_file_paths(negative_dir)
file_paths_dict["truthful"] = get_text_file_paths(truthful_dirs)
file_paths_dict["deceptive"] = get_text_file_paths(deceptive_dirs)

print(len(file_paths_dict[category]))
# print(file_paths_dict["deceptive"])


def get_texts(file_paths):
    texts = []
    for file_path in file_paths:
        # print("reading ", file_path)
        file = open(file_path, mode='r')
        all_of_it = file.read()
        # print(all_of_it)
        texts.append(all_of_it)
    return texts

texts = get_texts(file_paths_dict[category])



tokens = []
for text in texts:
    text = text.replace("\n", "").replace("(", "").replace(")", "").replace(".", "").replace(";", "").replace(",", "")
    tokens.extend(text.split(" "))

def get_bag_of_words(tokens):
    bag_of_words = {}
    for token in tokens:
        if token in bag_of_words:
            bag_of_words[token] += 1
        else:
            bag_of_words[token] = 1

    return bag_of_words


bag_of_words = get_bag_of_words(tokens)

print(bag_of_words)

def get_probs(bag_of_words):
    probs = {}
    total = sum(bag_of_words.values())
    for key in bag_of_words:
        probs[key] = bag_of_words[key]/total
    return probs

pos_probs = get_probs(bag_of_words)
print(pos_probs)

def save_to_csv(probs):
    with open(result_path+".csv", 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=probs.keys())
        writer.writeheader()
        for data in [probs]:
            writer.writerow(data)

def save_to_pickle(obj, filename):
    with open(filename+'.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

save_to_pickle(pos_probs, result_path)
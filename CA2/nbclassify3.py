import os
from os import walk

data_path = "data"

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
def get_file_paths(dir_paths):
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

file_paths_dict["positive"] = get_file_paths(positive_dir)
file_paths_dict["negative"] = get_file_paths(negative_dir)
file_paths_dict["truthful"] = get_file_paths(truthful_dirs)
file_paths_dict["deceptive"] = get_file_paths(deceptive_dirs)

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


print(len(texts))


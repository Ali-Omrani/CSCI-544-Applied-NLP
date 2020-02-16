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


def get_file_paths(dir_paths):
    files = []
    for dir_path in dir_paths:
        # r=root, d=directories, f = files
        for r, d, f in os.walk(dir_path):
            for file in f:
                if '.txt' in file:
                    files.append(os.path.join(r, file))
    return files

file_paths_dict = {}

file_paths_dict["positive"] = get_file_paths(positive_dir)
file_paths_dict["negative"] = get_file_paths(negative_dir)
file_paths_dict["truthful"] = get_file_paths(truthful_dirs)
file_paths_dict["deceptive"] = get_file_paths(deceptive_dirs)

print(file_paths_dict["deceptive"])

# print(type(h1))
# h1 = [item for item in h1 if os.path.isdir(item)]
# for item in h1:
#     print(h1)
#
# h1 = []
# for (dirpath_1, dirnames_1, filenames_1) in walk(data_path):
#     h1.extend(dirnames_1)
#     for (dirpath_2, dirname_2, filenames_2) in walk(h1):
#         print(dirname_2)
#     break
# print(h1)
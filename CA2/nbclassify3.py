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

positive_dir = os.path.join(data_path, "positive_polarity")
negative_dir = os.path.join(data_path, "negative_polarity")

truthful_dirs = [os.path.join(positive_dir, "truthful_from_TripAdvisor"), os.path.join(negative_dir, "truthful_from_TripAdvisor")]
deceptive_dirs = [os.path.join(positive_dir, "deceptive_from_MTurk"), os.path.join(negative_dir, "deceptive_from_MTurk")]
print(positive_dir)
print(negative_dir)
print(truthful_dirs)
print(deceptive_dirs)




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
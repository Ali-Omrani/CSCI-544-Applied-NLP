import os


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


def predict_pos_neg(file_path, pos_probs, neg_probs):
    file = open(file_path, mode='r')
    text = file.read()
    text = text.replace("\n", "").replace("(", "").replace(")", "").replace(".", "").replace(";", "").replace(",", "")
    tokens = text.split(" ")

    for token in tokens:
        print(token)




probs = {"ali": 0.2, "mamad": 0.3}

predict_path = "test_data"


text_file_paths = get_text_file_paths(predict_path)

for text_file_path in text_file_paths:




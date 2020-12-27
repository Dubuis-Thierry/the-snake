"""
Data management
"""
import pickle, os


class DataToSave:
    pass


def save_data(data):
    with open("data/scores.pickle", "wb") as file:
        pickle.dump(data, file)


def get_data(path="data/scores.pickle"):
    with open(path, "rb") as file:
        return pickle.load(file)


scores = DataToSave()
if os.path.exists("data/scores.pickle"):
    scores = get_data()
else:
    scores.highest = 0
    save_data(scores)

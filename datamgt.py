import pickle

class DataToSave:
    pass

def save_data(data):
    with open("data/scores.pickle", "wb") as file:
        pickle.dump(data, file)

def get_data(path="data/scores.pickle"):
    with open(path, "rb") as file:
        return pickle.load(file)
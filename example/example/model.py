import pickle

from xgboost import XGBClassifier


class Model:
    def __init__(self, target_names):
        self.clf = XGBClassifier()
        self.target_names = target_names

    def fit(self, X_train, y_train):
        self.clf.fit(X_train, y_train)

    def predict(self, data: dict) -> dict:
        y = self.predict_raw(data["features"])
        return self.target_names[y]

    def predict_raw(self, value):
        return self.clf.predict(value)

    def save(self):
        with open("model.pkl", "wb") as fp:
            pickle.dump(self, fp)

    @classmethod
    def load(cls, path: str):
        with open(path, "rb") as fp:
            model = pickle.load(fp)
        assert isinstance(model, cls)
        return model

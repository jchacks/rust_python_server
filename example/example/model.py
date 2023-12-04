import pickle
import treelite
import numpy as np
from xgboost import XGBClassifier


class Model:
    def __init__(self, target_names):
        self.clf = XGBClassifier()
        self.target_names = target_names

    def fit(self, X_train, y_train):
        self.clf.fit(X_train, y_train)
        self.clf._Booster.set_param("nthread", 1)

    def predict(self, data: dict) -> dict:
        # Make the prediction larger to increase the latency.
        y = self.predict_raw([data["features"]])
        return self.target_names[y][0]

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


class InferenceModel:
    def __init__(self, target_names, model):
        self.model = model
        self.target_names = target_names

    def predict(self, data: dict) -> dict:
        features = np.array([data["features"]])
        y = treelite.gtil.predict(self.model, features)
        return self.target_names[np.argmax(y)]

    @classmethod
    def from_model(cls, model: Model):
        tlite = treelite.frontend.from_xgboost(model.clf._Booster)
        return cls(model.target_names, tlite)

# Importing dataset from sklearn
import pickle

from sklearn import datasets
from sklearn.model_selection import train_test_split
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


if __name__ == "__main__":
    iris = datasets.load_iris()  # dataset loading
    X = iris.data  # Features stored in X
    y = iris.target  # Class variable
    target_names = iris.target_names
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("Example input", X_test[0])

    model = Model(target_names)
    model.fit(X_train, y_train)

    y_pred = model.predict({"features": X_test})
    print(y_pred)
    model.save()

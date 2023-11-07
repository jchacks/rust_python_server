# Importing dataset from sklearn

from sklearn import datasets
from sklearn.model_selection import train_test_split
from example.model import Model


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

    y_pred = model.predict({"features": X_test[0]})
    print(y_pred)
    model.save()

from typing import Optional
from example.model import Model

MODEL: Optional[Model] = None


def load_model(path: str):
    print("PYTHON: calling load_model")
    global MODEL
    MODEL = Model.load(path)
    print(MODEL)
    assert hasattr(MODEL, "predict")
    print("PYTHON: loaded model")


def run_model(data: dict):
    return MODEL.predict(data)


if __name__ == "__main__":
    import timeit
    number = 10
    res = timeit.timeit(
        'run_model({"features": [6.1, 2.8, 4.7, 1.2]})',
        setup='load_model("model.pkl")',
        globals=globals(),
        number=number,
    )
    print(res / number)

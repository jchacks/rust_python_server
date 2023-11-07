import time
from typing import Optional
from train import Model
import traceback

MODEL: Optional[Model] = None


def load_model(path: str):
    print("PYTHON: calling load_model")
    try:
        global MODEL
        MODEL = Model.load(path)
        print(MODEL)
        assert hasattr(MODEL, "predict")
    except Exception as e:
        print(e)
        traceback.print_exc()
    print("PYTHON: loaded model")


def run_model(data: dict):
    # Modify sharedmem to illustrate thread safety
    s = time.time()
    i = 0
    while time.time() - s < 0.1:
        prediction = MODEL.predict(data)
        i += 1
    print(i)
    return {"status": "Success", "prediction": prediction}


if __name__ == "__main__":
    load_model("./example/model.pkl")

import time, sys, threading
import numpy as np

LARGE_DATA = bytearray(1 * 1024 * 1024 * 1024)
print(len(LARGE_DATA), sys.getsizeof(LARGE_DATA))
SHARED_MEM = [1]

lock = threading.Lock()


def run_model(i: int, j: int):
    # locking does work in order
    # with lock:
    SHARED_MEM[0] = j
    # sys.stdout.write(f"pthread:{i} Making prediction {SHARED_MEM}: {j}\n")
    # sys.stdout.flush()

    s = time.time()
    A = np.random.rand(10, 10)
    B = np.random.rand(30, 10)
    while time.time() - s < 0.1:
        np.dot(B, A.T)

    # Try to modify, seems to work
    return {"Some": f"Prediction{i}", "shared_memory": SHARED_MEM, "j": j}


# def setup_flask():
#     from flask import Flask, request

#     app = Flask(__name__)

#     @app.post("/invoke")
#     def invoke():
#         data = request.get_json()
#         return run_model(**data)

#     return app


# if __name__ == "__main__":
#     app = setup_flask()

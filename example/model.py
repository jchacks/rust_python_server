import time, sys, threading
import numpy as np

# Allocate some large memory
LARGE_DATA = bytearray(1 * 1024 * 1024 * 1024)
print(len(LARGE_DATA), sys.getsizeof(LARGE_DATA))

# Add a global variable
SHARED_MEM = [1]

lock = threading.Lock()


def run_model(i: int, j: int):
    # Modify sharedmem to illustrate thread safety
    SHARED_MEM[0] = j
    sys.stdout.write(f"pthread:{i} Making prediction {SHARED_MEM}: {j}\n")
    sys.stdout.flush()

    s = time.time()
    A = np.random.rand(10, 10)
    B = np.random.rand(30, 10)
    while time.time() - s < 0.1:
        np.dot(B, A.T)

    return {"Some": f"Prediction{i}", "shared_memory": SHARED_MEM, "j": j}

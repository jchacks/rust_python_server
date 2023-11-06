import time, sys, threading

LARGE_DATA = bytearray(1 * 1024 * 1024 * 1024)
print(len(LARGE_DATA), sys.getsizeof(LARGE_DATA))
SHARED_MEM = [1]

lock = threading.Lock()


def run_model(i: int, j: int):
    # locking does work in order
    # with lock:
    SHARED_MEM[0] = j
    sys.stdout.write(f"pthread:{i} Making prediction {SHARED_MEM}: {j}\n")
    sys.stdout.flush()

    # time.sleep(0.1) # releases the gil so not a good example
    s = time.time()
    while time.time() - s < 0.1:
        pass
    
    # Try to modify, seems to work
    return {"Some": f"Prediction{i}", "shared_memory": SHARED_MEM, "j": j}

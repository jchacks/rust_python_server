# Rust Server Hosting Python Model

Experiments wrapping a python callable in a rust axum webserver.

## Introduction

A toy model located in `example/model.py` mulitplies numpy matrices for 0.1 sec.

Rust Axum Web Server loads the python module and exposes the function at `/invoke`.  

The python function needs to be thread safe, depending on how intensive the python function is and how the GIL is handled can affect the benchmarks, for example using `time.sleep` as a proxy for "cpu work" is not great as the GIL is released for the whole time sleeping.  A bare loop `while time.time() - start < 0.1: pass` is also not representative of invoking python libraries which might release the GIL during their operation.

Running locust with with 500 "users" 2700 requests per second was reached with mean response of 170ms and 95th percentile of 350ms. [BENCHMARK.md](/docs/BENCHMARK.md)


## Rust

To test the server using locust:

```bash
python3.10 -m venv .venv
source .venv/bin/activate
pip install -e ./example

# Create model.pkl
python -m example.train

# Boot server
cargo run -r

# Test using locust
cd example && locust
```

## Python Baseline

WIP: Add a flask application to compare.
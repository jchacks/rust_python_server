# Rust Server Hosting Python Model

Experiments wrapping a python callable in a rust axum webserver.

## Introduction

An toy model located in `example/model.py` mulitplies numpy matrices for 0.1 sec.

Rust Axum Web Server loads the python module and exposes the function at `/invoke`.

Running locust with with 500 "users" 2700 requests per second was reached with mean response of 170ms and 95th percentile of 350ms. [BENCHMARK.md](/docs/BENCHMARK.md)


## Rust

To test the server using locust:

```bash
python3.10 -m venv .venv
source .venv/bin/activate
pip install flask locust numpy

# Boot cargo server
cargo run -r

# Test using locust
cd example && locust
```

## Python Baseline

WIP: Add a flask application to compare.
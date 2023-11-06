# Rust Server Hosting Python Model

Experiments wrapping a python callable in a rust axum webserver.

## Introduction

An toy model located in `example/model.py` mulitplies numpy matrices for 0.1 sec.
Rust Axum Web Server loads the python module and exposes the function at `/invoke`.

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
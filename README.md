# Rust Server Python Model Experiment

Experiments wrapping a python callable in a rust axum webserver.

Note: Fun experiments but it doesnt really help due to GIL constraints.


## Introduction

A toy model located in `example/example/model.py` runs XGBoost.

Rust Axum Web Server loads the python module and exposes the function at `/invoke`.  

The python function needs to be thread safe, depending on how intensive the python function is and how the GIL is handled can affect the benchmarks, for example using `time.sleep` as a proxy for "cpu work" is not great as the GIL is released for the whole time sleeping.  A bare loop `while time.time() - start < 0.1: pass` is also not representative of invoking python libraries which might release the GIL during their operation.  Repeated XGBoost invocatons also scale very badly, not sure of the cause of this.

## Testing 

Useful to check the endpoint with curl:

```bash
$ curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"features": [6.1, 2.8, 4.7, 1.2]}' \
  http://localhost:3000/invoke

{"Success":{"prediction":"versicolor"}}
```

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
# Rust Server Hosting Python Model

Experiments wrapping a python callable in a rust axum webserver.

## Rust

To test the server using locust:

```bash
python3.10 -m venv .venv
source .venv/bin/activate
pip install flask locust numpy
cargo run -r
cd example && locust
```
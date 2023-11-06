from flask import Flask, request
from model import run_model


app = Flask(__name__)

@app.post("/invoke")
def invoke():
    data = request.get_json()
    return run_model(**data)


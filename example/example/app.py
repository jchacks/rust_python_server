from flask import Flask, request
from example.predict import run_model, load_model

load_model("model.pkl")

app = Flask(__name__)

@app.post("/invoke")
def invoke():
    data = request.get_json()
    return run_model(data)


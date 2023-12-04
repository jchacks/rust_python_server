from flask import Flask, request
from example.predict import run_model, load_model


def create_app():
    app = Flask(__name__)
    load_model("model.pkl")

    @app.post("/invoke")
    def invoke():
        data = request.get_json()
        return run_model(data)

    return app

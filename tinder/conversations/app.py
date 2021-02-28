from flask import Flask, request

app = Flask(__name__)


@app.route("/get_response", methods=["POST"])
def get_msg_response():
    pass

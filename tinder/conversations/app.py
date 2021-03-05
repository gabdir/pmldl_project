from flask import Flask, request, Response

app = Flask(__name__)


@app.route("/get_response", methods=["POST"])
def get_msg_response():

    return Response(status=501)

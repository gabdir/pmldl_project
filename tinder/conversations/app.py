from flask import Flask, request, Response
from transformers import AutoModelWithLMHead, AutoTokenizer
import torch


app = Flask(__name__)
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelWithLMHead.from_pretrained("microsoft/DialoGPT-medium")


@app.route("/get_response", methods=["POST"])
def get_msg_response():
    messages = request.values.get("messages")

    labeled_sentences = ""
    for sentence in messages:
        labeled_sentences = labeled_sentences + sentence + tokenizer.eos_token

    tokenized_all_sentences_string = tokenizer.encode(labeled_sentences, return_tensors='pt')
    reply_predicted = model.generate(tokenized_all_sentences_string, max_length=1000)
    prefix_length = tokenized_all_sentences_string.shape[-1]

    decoded_reply_predicted_with_input = tokenizer.decode(reply_predicted[0], skip_special_tokens=True)
    decoded_reply_predicted = tokenizer.decode(reply_predicted[:, prefix_length:][0], skip_special_tokens=True)

    return Response(status=200, response=decoded_reply_predicted)

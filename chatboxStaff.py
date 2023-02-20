from flask import jsonify, request
import json
from app import app


@app.route("/new_message", methods=["POST"])
def new_message():
    data = json.loads(request.data)
    message = data["message"]
    # Save the message to the database or do any other logic here
    return jsonify(success=True, message=message)


@app.route("/messages", methods=["GET"])
def get_messages():
    # Retrieve messages from the database or do any other logic here
    messages = []
    return jsonify(messages)





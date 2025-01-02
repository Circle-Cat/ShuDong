from api import event_handler
from typing import Any, Mapping
from flask import Flask, request, json

app = Flask(__name__)

@app.route("/", methods=["POST"])
def post() -> Mapping[str, Any]:
    """Handle requests from Google Chat

    - Create new Shudong post for ADDED_TO_SPACE and MESSAGE events
    - Update existing card for 'Appropriate','Inappropriate','NSFW' clicks

    Returns:
        Mapping[str, Any]: the response card
    """
    event = request.get_json()

    return event_handler.event_handler(event)


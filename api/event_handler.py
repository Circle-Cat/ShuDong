import uuid

from api.messages import (
    create_card,
    create_dialog_text,
    create_message_main_private,
    deleted_message,
)
from flask import json
from typing import Any, Mapping


def event_handler(event) -> Mapping[str, Any]:

    match event["type"]:
        case "ADDED_TO_SPACE":
            # Create new Shudong session for when added to a space
            message = {}

        case "MESSAGE":
            match event["message"]["annotations"][0]["type"]:
                case "SLASH_COMMAND":
                    match event["message"]["annotations"][0]["slashCommand"][
                        "commandId"
                    ]:
                        case "1":
                            # Create new Shudong session via slash command
                            message = create_card(
                                uuid.uuid4(), event["message"]["argumentText"]
                            )
                        case _:
                            message = {}

                case _:
                    user_id = event["message"]["sender"]["name"]
                    message = create_message_main_private(
                        "Please use slash command `/sendShudong` followed by your content to anonymously send/reply a new Shudong.",
                        user_id,
                    )

        case "CARD_CLICKED":
            action = event["action"]["actionMethodName"]

            if action == "send_new":
                message = create_dialog_text(
                    "Send/Reply a new Shudong anonymously",
                    "Please use slash command `/sendShudong` followed by your content to anonymously send/reply a new Shudong.",
                )
            else:
                count = int(event["action"]["parameters"][2]["value"])
                shudong_id = event["action"]["parameters"][0]["value"]

                # Rebuild voter dictionary
                voter = eval(event["action"]["parameters"][3]["value"])
                user_id = event["user"]["name"]

                # Remove inappropriate post by vote
                if count <= -30:
                    message = deleted_message(shudong_id)
                else:
                    content = event["action"]["parameters"][1]["value"]

                    if user_id in voter:
                        vote_recovery = - int(voter[user_id])
                    else:
                        vote_recovery = 0

                    match action:
                        case "appropriate":
                            # Appropriate butten pressed
                            voter[user_id] = 1
                            message = create_card(
                                shudong_id,
                                content,
                                voter=voter,
                                count=count + 1 + vote_recovery,
                                update=True,
                            )
                        case "inappropriate":
                            # Inappropriate button pressed
                            voter[user_id] = -1
                            message = create_card(
                                shudong_id,
                                content,
                                voter=voter,
                                count=count - 1 + vote_recovery,
                                update=True,
                            )
                        case "nsfw":
                            # NSFW button pressed
                            voter[user_id] = -5
                            message = create_card(
                                shudong_id,
                                content,
                                voter=voter,
                                count=count - 5 + vote_recovery,
                                update=True,
                            )

        case _:
            # no response for REMOVED_FROM_SPACE
            message = {}

    return json.jsonify(message)

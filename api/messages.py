from typing import Any, Mapping


def create_card(
    shudong_id: str,
    content: str,
    voter: str = "{}",
    count: int = 0,
    update: bool = False,
) -> Mapping[str, Any]:
    """Creates the card message

    Args:
        shudong_id (str): required, unique ID of the vote
        content (str): required, the content users can vote for
        voter (str): the user who voted (where appropriate)
        count (int): the current vote count
        update (bool): whether it's an update or a new vote session

    Returns:
        Mapping[str, Any]: the vote card
    """
    return {
        "actionResponse": {"type": ("UPDATE_MESSAGE" if update else "NEW_MESSAGE")},
        "cardsV2": [
            {
                "cardId": shudong_id,
                "card": {
                    "sections": [
                        {
                            "widgets": [
                                {"textParagraph": {"text": f"{content}"}},
                                {"textParagraph": {"text": f"🉑 <b>Score:{count}<b>"}},
                                {"divider": {}},
                                {
                                    "buttonList": {
                                        "buttons": [
                                            {
                                                "text": "Appropriate",
                                                "onClick": {
                                                    "action": {
                                                        "function": "appropriate",
                                                        "parameters": [
                                                            {
                                                                "key": "shudong_id",
                                                                "value": f"{shudong_id}",
                                                            },
                                                            {
                                                                "key": "content",
                                                                "value": f"{content}",
                                                            },
                                                            {
                                                                "key": "count",
                                                                "value": f"{count}",
                                                            },
                                                            {
                                                                "key": "voter",
                                                                "value": f"{voter}",
                                                            },
                                                        ],
                                                    }
                                                },
                                            },
                                            {
                                                "text": "Inappropriate",
                                                "onClick": {
                                                    "action": {
                                                        "function": "inappropriate",
                                                        "parameters": [
                                                            {
                                                                "key": "shudong_id",
                                                                "value": f"{shudong_id}",
                                                            },
                                                            {
                                                                "key": "content",
                                                                "value": f"{content}",
                                                            },
                                                            {
                                                                "key": "count",
                                                                "value": f"{count}",
                                                            },
                                                            {
                                                                "key": "voter",
                                                                "value": f"{voter}",
                                                            },
                                                        ],
                                                    }
                                                },
                                            },
                                            {
                                                "text": "NSFW",
                                                "onClick": {
                                                    "action": {
                                                        "function": "nsfw",
                                                        "parameters": [
                                                            {
                                                                "key": "shudong_id",
                                                                "value": f"{shudong_id}",
                                                            },
                                                            {
                                                                "key": "content",
                                                                "value": f"{content}",
                                                            },
                                                            {
                                                                "key": "count",
                                                                "value": f"{count}",
                                                            },
                                                            {
                                                                "key": "voter",
                                                                "value": f"{voter}",
                                                            },
                                                        ],
                                                    }
                                                },
                                            },
                                            {
                                                "text": "Send/Reply Shudong",
                                                "type": "BORDERLESS",
                                                "onClick": {
                                                    "action": {
                                                        "function": "send_new",
                                                        "interaction": "OPEN_DIALOG",
                                                    }
                                                },
                                            },
                                        ]
                                    }
                                },
                            ]
                        },
                    ]
                },
            }
        ],
    }


def create_message_main_private(content: str, user_id: str) -> Mapping[str, Any]:
    return {"text": content, "private_message_viewer": {"name": user_id}}


def create_dialog_text(header: str, content: str) -> Mapping[str, Any]:
    return {
        "actionResponse": {
            "type": "DIALOG",
            "dialogAction": {
                "dialog": {
                    "body": {
                        "sections": [
                            {
                                "header": header,
                                "widgets": [
                                    {"textParagraph": {"text": content}},
                                ],
                            }
                        ]
                    }
                }
            },
        }
    }


def deleted_message(shudong_id: str) -> Mapping[str, Any]:
    return {
        "actionResponse": {"type": ("UPDATE_MESSAGE")},
        "cardsV2": [
            {
                "cardId": shudong_id,
                "card": {
                    "sections": [
                        {
                            "widgets": [
                                {
                                    "textParagraph": {
                                        "text": "This post was removed by votes because it was not safe for work."
                                    }
                                }
                            ]
                        }
                    ]
                },
            }
        ],
    }

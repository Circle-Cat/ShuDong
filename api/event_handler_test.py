"""Test for event_handler.py"""

import unittest
import uuid
from flask import Flask, json
from api.event_handler import event_handler


class TestEventHandler(unittest.TestCase):
    """Unit tests for event_handler function"""

    def setUp(self):
        """Set up a Flask test app and app context"""
        self.app = Flask(__name__)  # Create a Flask app
        self.ctx = self.app.app_context()  # Create an app context
        self.ctx.push()  # Activate app context
        self.client = self.app.test_client()  # Test client

    def tearDown(self):
        """Clean up after each test"""
        self.ctx.pop()  # Remove app context after test

    def test_added_to_space_event(self):
        """Test case 1: Handling ADDED_TO_SPACE Event"""
        event = {"type": "ADDED_TO_SPACE"}
        response = event_handler(event)
        self.assertEqual(response.json, {})  # Should return an empty dictionary

    def test_message_event_slash_command(self):
        """Test case 2: Handling MESSAGE Event (Slash Command)"""
        event = {
            "type": "MESSAGE",
            "message": {
                "annotations": [
                    {"type": "SLASH_COMMAND", "slashCommand": {"commandId": "1"}}
                ],
                "argumentText": "Test Message",
            },
        }

        response = event_handler(event)

        # The response should contain a valid card with a UUID
        self.assertIn("cardsV2", response.json)
        self.assertIn("cardId", response.json["cardsV2"][0])

    def test_message_event_regular_message(self):
        """Test case 3: Handling MESSAGE Event (Regular Message)"""
        event = {
            "type": "MESSAGE",
            "message": {
                "annotations": [{"type": "PLAIN_TEXT"}],  # Not a slash command
                "sender": {"name": "user123"},
            },
        }

        response = event_handler(event)

        # Should return a private message instructing to use the slash command
        expected_message = "Please use slash command `/sendShudong` followed by your content to anonymously send/reply a new Shudong."
        self.assertEqual(response.json["text"], expected_message)
        self.assertEqual(response.json["private_message_viewer"]["name"], "user123")

    def test_card_clicked_voting(self):
        """Test case 4: Handling CARD_CLICKED Event (Voting)"""
        event = {
            "type": "CARD_CLICKED",
            "user": {"name": "user123"},
            "action": {
                "actionMethodName": "appropriate",
                "parameters": [
                    {"value": "shudong_1"},  # shudong_id
                    {"value": "Some content"},  # content
                    {"value": "5"},  # count
                    {"value": "{}"},  # voter (empty initially)
                ],
            },
        }

        # Call the event handler function with the test event
        response = event_handler(event)
        # Check if the vote count increased
        self.assertIn("cardsV2", response.json)

        # Assert that the score has increased as expected
        self.assertEqual(
            response.json["cardsV2"][0]["card"]["sections"][0]["widgets"][1][
                "textParagraph"
            ]["text"],
            "🉑 <b>Score:6<b>",
        )

    def test_card_clicked_inappropriate(self):
        """Test case 5: Handling CARD_CLICKED Event (Inappropriate Vote)"""
        event = {
            "type": "CARD_CLICKED",
            "user": {"name": "user123"},
            "action": {
                "actionMethodName": "inappropriate",
                "parameters": [
                    {"value": "shudong_1"},  # shudong_id
                    {"value": "Some content"},  # content
                    {"value": "5"},  # count
                    {"value": "{}"},  # voter (empty initially)
                ],
            },
        }

        response = event_handler(event)

        # Check if the vote count decreased
        self.assertIn("cardsV2", response.json)
        self.assertEqual(
            response.json["cardsV2"][0]["card"]["sections"][0]["widgets"][1][
                "textParagraph"
            ]["text"],
            "🉑 <b>Score:4<b>",
        )

    def test_card_clicked_nsfw(self):
        """Test case 6: Handling CARD_CLICKED Event (NSFW Vote)"""
        event = {
            "type": "CARD_CLICKED",
            "user": {"name": "user123"},
            "action": {
                "actionMethodName": "nsfw",
                "parameters": [
                    {"value": "shudong_1"},  # shudong_id
                    {"value": "Some content"},  # content
                    {"value": "10"},  # count
                    {"value": "{}"},  # voter (empty initially)
                ],
            },
        }

        response = event_handler(event)

        # Check if the vote count dropped by 5
        self.assertIn("cardsV2", response.json)
        self.assertEqual(
            response.json["cardsV2"][0]["card"]["sections"][0]["widgets"][1][
                "textParagraph"
            ]["text"],
            "🉑 <b>Score:5<b>",
        )

    def test_message_event_message_removal(self):
        """Test case 7: Handling MESSAGE Event (Message Removal)"""
        event = {
            "type": "CARD_CLICKED",
            "user": {"name": "user123"},
            "action": {
                "actionMethodName": "inappropriate",
                "parameters": [
                    {"value": "shudong_1"},  # shudong_id
                    {"value": "Some content"},  # content
                    {"value": "-30"},  # count is already -30
                    {"value": "{}"},  # voter
                ],
            },
        }

        response = event_handler(event)

        # Should return a message indicating the post was deleted
        self.assertEqual(
            response.json["cardsV2"][0]["card"]["sections"][0]["widgets"][0][
                "textParagraph"
            ]["text"],
            "This post was removed by votes because it was not safe for work.",
        )

    def test_unknown_event(self):
        """Test case 8: Handling Unknown Events"""
        event = {"type": "UNKNOWN_EVENT"}

        response = event_handler(event)

        # Should return an empty response
        self.assertEqual(response.json, {})


if __name__ == "__main__":
    unittest.main()

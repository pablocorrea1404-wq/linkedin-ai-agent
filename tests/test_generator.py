# -*- coding: utf-8 -*-
"""Unit tests for the LinkedIn AI Content Agent."""
import os
import unittest
from unittest.mock import patch
from src.config import TOPICS, load_state, save_state
from src.generator import SYSTEM_PROMPT, generate_post

class TestLinkedInAgent(unittest.TestCase):
    """Test suite for post generation and agent state."""

    def test_topics_configured(self):
        """Verify topics pool contains real-world technical architecture themes."""
        self.assertIsInstance(TOPICS, list)
        self.assertGreaterEqual(len(TOPICS), 5)
        for topic in TOPICS:
            self.assertIsInstance(topic, str)
            self.assertGreater(len(topic), 10)

    def test_system_prompt_rules(self):
        """Ensure prompt guidelines enforce technical authority and structure."""
        self.assertIn("Ingeniero Full Stack", SYSTEM_PROMPT)
        self.assertIn("hashtags", SYSTEM_PROMPT)
        self.assertIn("Pablo Correa Ribeiro", SYSTEM_PROMPT)

    @patch("src.generator.OPENAI_API_KEY", "")
    def test_missing_api_key_graceful_handling(self):
        """Ensure generate_post fails gracefully with missing credentials without raising unhandled exceptions."""
        result = generate_post()
        self.assertIn("Error: OPENAI_API_KEY no configurada", result)

    def test_state_load_save(self):
        """Test persistent state read and write operations."""
        sample_state = {
            "chat_ids": [12345678],
            "daily_active": True,
            "last_post": "Test post content"
        }
        save_state(sample_state)
        loaded = load_state()
        self.assertIn(12345678, loaded.get("chat_ids", []))
        self.assertEqual(loaded.get("last_post"), "Test post content")

if __name__ == "__main__":
    unittest.main()

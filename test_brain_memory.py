import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from brain import ValentineBrain


class BrainMemoryTests(unittest.TestCase):
    def test_history_is_saved_and_loaded(self):
        with tempfile.TemporaryDirectory() as directory:
            memory_path = Path(directory) / "memory.json"
            brain = ValentineBrain(memory_path=memory_path)

            with patch("brain.random.choice", return_value="Je suis là pour toi."):
                brain.process_input("Je me sens seul")

            reloaded = ValentineBrain(memory_path=memory_path)

            self.assertEqual(reloaded.conversation_history[0]["role"], "user")
            self.assertEqual(reloaded.conversation_history[0]["content"], "Je me sens seul")
            self.assertEqual(reloaded.conversation_history[1]["role"], "assistant")
            self.assertTrue(memory_path.exists())
            self.assertIsInstance(json.loads(memory_path.read_text(encoding="utf-8")), list)

    def test_api_messages_include_previous_context(self):
        with tempfile.TemporaryDirectory() as directory:
            brain = ValentineBrain(memory_path=Path(directory) / "memory.json")
            brain.memory.add_exchange("Je m'appelle Alex", "Enchantée Alex.")

            messages = brain._build_messages("Tu te souviens de mon prénom ?")

            self.assertEqual([message["role"] for message in messages], [
                "system", "user", "assistant", "user"
            ])
            self.assertEqual(messages[-2]["content"], "Enchantée Alex.")


if __name__ == "__main__":
    unittest.main()
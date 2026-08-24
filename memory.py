import json
import threading
from pathlib import Path


class ConversationMemory:
    """Persists a bounded chat history in a small local JSON file."""

    def __init__(self, path, max_messages=40):
        self.path = Path(path)
        self.max_messages = max(2, max_messages)
        self._lock = threading.Lock()
        self.messages = self._load()

    def _load(self):
        try:
            with self.path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except (OSError, json.JSONDecodeError):
            return []

        if not isinstance(data, list):
            return []

        return [
            message for message in data
            if isinstance(message, dict)
            and message.get("role") in {"user", "assistant"}
            and isinstance(message.get("content"), str)
            and message["content"].strip()
        ][-self.max_messages:]

    def snapshot(self):
        with self._lock:
            return list(self.messages)

    def add_exchange(self, user_input, assistant_response):
        with self._lock:
            self.messages.extend([
                {"role": "user", "content": user_input.strip()},
                {"role": "assistant", "content": assistant_response.strip()},
            ])
            self.messages = self.messages[-self.max_messages:]
            self._save()

    def add_assistant_message(self, content):
        with self._lock:
            self.messages.append({"role": "assistant", "content": content.strip()})
            self.messages = self.messages[-self.max_messages:]
            self._save()

    def clear(self):
        with self._lock:
            self.messages = []
            try:
                self.path.unlink()
            except FileNotFoundError:
                pass

    def _save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = self.path.with_suffix(self.path.suffix + ".tmp")
        with temporary_path.open("w", encoding="utf-8") as file:
            json.dump(self.messages, file, ensure_ascii=False, indent=2)
        temporary_path.replace(self.path)
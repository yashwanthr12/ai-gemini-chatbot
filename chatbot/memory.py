import os
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class ChatMemory:
    """
    Simple in-memory chat history.
    Stores messages as: {"role": "user"/"assistant", "content": "..."}
    """
    max_turns: int = field(default_factory=lambda: int(os.getenv("MEMORY_MAX_TURNS", "20")))
    messages: List[Dict[str, str]] = field(default_factory=list)

    def add_user(self, text: str) -> None:
        self.messages.append({"role": "user", "content": text})
        self._trim()

    def add_assistant(self, text: str) -> None:
        self.messages.append({"role": "assistant", "content": text})
        self._trim()

    def _trim(self) -> None:
        # max_turns means user+assistant pairs => 2 * max_turns messages
        limit = 2 * self.max_turns
        if len(self.messages) > limit:
            self.messages = self.messages[-limit:]

    def as_text_block(self) -> str:
        """
        Gemini library can accept content in many forms; simplest is to pass a text block.
        """
        if not self.messages:
            return "No prior conversation."
        lines = []
        for m in self.messages:
            role = "User" if m["role"] == "user" else "Assistant"
            lines.append(f"{role}: {m['content']}")
        return "\n".join(lines)
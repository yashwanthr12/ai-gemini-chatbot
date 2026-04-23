import os
import google.generativeai as genai
from chatbot.prompts import SYSTEM_PROMPT
from utils.logger import setup_logger

logger = setup_logger("gemini_api")

class GeminiChat:
    def __init__(self) -> None:
        api_key = os.getenv("GEMINI_API_KEY", "").strip()
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set in .env")

        genai.configure(api_key=api_key)

        # Preferred model from env (may fail if unavailable)
        preferred = os.getenv("MODEL_NAME", "").strip()

        # Build a list of candidate models to try (preferred first)
        candidates = []
        if preferred:
            candidates.append(preferred)

        # Safe fallbacks commonly supported
        candidates.extend([
            "gemini-1.0-pro",
            "gemini-pro",
        ])

        self.model_name = self._pick_working_model(candidates)
        self.model = genai.GenerativeModel(self.model_name)
        logger.info("Using Gemini model=%s", self.model_name)

    def _pick_working_model(self, candidates: list[str]) -> str:
        """
        Try candidates first; if they fail, list available models and pick one
        that supports generateContent.
        """
        # 1) Try candidates quickly
        for name in candidates:
            try:
                m = genai.GenerativeModel(name)
                _ = m.generate_content("ping")  # lightweight test call
                logger.info("Model works: %s", name)
                return name
            except Exception as e:
                logger.warning("Model failed: %s (%s)", name, type(e).__name__)

        # 2) If none work, list models and choose one that supports generateContent
        try:
            models = list(genai.list_models())
        except Exception as e:
            raise RuntimeError(
                "Failed to list Gemini models. Check your GEMINI_API_KEY and network access."
            ) from e

        # Filter models that support generateContent
        supported = []
        for m in models:
            # m.supported_generation_methods is usually present in this library
            methods = getattr(m, "supported_generation_methods", []) or []
            if "generateContent" in methods:
                supported.append(m.name)  # usually like 'models/gemini-pro'

        if not supported:
            raise RuntimeError(
                "No available models support generateContent for this API key. "
                "Open AI Studio -> check key permissions / enabled APIs."
            )

        # Pick the first supported model. It comes as "models/xxx" sometimes.
        chosen = supported[0]
        # Normalize "models/xyz" -> "xyz" for GenerativeModel constructor in many cases
        if chosen.startswith("models/"):
            chosen = chosen.replace("models/", "", 1)

        logger.info("Auto-selected supported model: %s", chosen)
        return chosen

    def generate(self, user_input: str, memory_text: str, tool_text: str = "") -> str:
        prompt = f"""{SYSTEM_PROMPT}

Conversation History:
{memory_text}

Tool Data (if any):
{tool_text}

User Question:
{user_input}

Answer:
"""
        logger.info("Calling Gemini model=%s", self.model_name)
        resp = self.model.generate_content(prompt)
        return (resp.text or "").strip()
    
from typing import List, Dict
from openai import OpenAI

class AIAssistant:
    def __init__(self, api_key: str, model: str = "gpt-4o-mini",
                 system_prompt: str = "You are a helpful assistant."):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self._system_prompt = system_prompt
        self._history: List[Dict[str, str]] = [
            {"role": "system", "content": system_prompt}
        ]

    def set_system_prompt(self, prompt: str) -> None:
        self._system_prompt = prompt
        self._history = [{"role": "system", "content": prompt}]

    def send_message(self, user_message: str) -> str:
        self._history.append({"role": "user", "content": user_message})
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self._history
        )
        reply_text = response.choices[0].message.content
        self._history.append({"role": "assistant", "content": reply_text})
        return reply_text

    def clear_history(self) -> None:
        self._history = [
            {"role": "system", "content": self._system_prompt}
        ]
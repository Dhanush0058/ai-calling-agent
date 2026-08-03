from app.agents.memory import ConversationMemory
from app.agents.prompt_manager import SYSTEM_PROMPT
from app.integrations.gemini_client import GeminiClient


class AIAgent:

    def __init__(self):
        self.memory = ConversationMemory()
        self.llm = GeminiClient()

    def ask(self, text):

        self.memory.add_user(text)

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

        messages.extend(
            self.memory.history()
        )

        answer = self.llm.chat(messages)

        self.memory.add_ai(answer)

        return answer

    def reset(self):
        self.memory.clear()
from app.agents.memory import ConversationMemory
from app.agents.prompt_manager import SYSTEM_PROMPT
from app.integrations.gemini_client import GeminiClient
from app.tools.customer_tools import CustomerTools


class AIAgent:

    def __init__(self):
        self.memory = ConversationMemory()
        self.llm = GeminiClient()

    def ask(
        self,
        text,
        db=None,
    ):

        self.memory.add_user(text)

        text_lower = text.lower()

        if db:
            if "how many customer" in text_lower:
                count = CustomerTools.customer_count(db)
                return f"There are {count} customers in the database."

        context = ""

        # ---------- Tool Calling ----------
        if db:

            customers = CustomerTools.get_all_customers(db)

            if customers:

                context = "\nCustomer Database:\n"

                for customer in customers:

                    context += (
                        f"Name: {customer.name}, "
                        f"Email: {customer.email}, "
                        f"Phone: {customer.phone}\n"
                    )

        # ---------- Prompt ----------

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT + context
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
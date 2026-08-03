class ConversationMemory:

    def __init__(self):
        self.messages = []

    def add_user(self, text):
        self.messages.append({
            "role": "user",
            "content": text
        })

    def add_ai(self, text):
        self.messages.append({
            "role": "assistant",
            "content": text
        })

    def history(self):
        return self.messages

    def clear(self):
        self.messages = []
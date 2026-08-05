class PromptBuilder:

    @staticmethod
    def build(
        message,
        context,
        tool_result,
    ):

        return f"""
You are an AI Customer Support Executive.

Customer Profile:

{context['profile']}

Customer Memory:

{context['memory']}

Tool Result:

{tool_result}

Current Question:

{message}

Answer naturally and professionally.
"""


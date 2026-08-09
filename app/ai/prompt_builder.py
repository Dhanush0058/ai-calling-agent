class PromptBuilder:

    @staticmethod
    def build(
        message,
        context,
        tool_result,
    ):

        relevant_calls = context.get("relevant_calls", "No relevant calls found.")

        return f"""
You are an AI Customer Support Executive.

Customer Profile:

{context['profile']}

Customer Memory:

{context['memory']}

Relevant Calls:

{relevant_calls}

Tool Result:

{tool_result}

Current Question:

{message}

Answer naturally and professionally.
"""


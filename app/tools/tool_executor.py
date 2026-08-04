from sqlalchemy.orm import Session

from app.memory.memory_service import MemoryService
from app.tools.customer_tools import CustomerTools
from app.tools.semantic_intent_router import router as SemanticIntentRouter


class ToolExecutor:

    def __init__(self, db: Session):
        self.db = db
        self.router = SemanticIntentRouter
        self.memory_service = MemoryService()

    def execute(self, message: str, customer_id: int | None = None):

        intent = self.router.predict(message)

        if intent == "CUSTOMER_COUNT":
            count = CustomerTools.customer_count(self.db)
            return f"There are {count} customers in the database."

        if intent == "CUSTOMER_LIST":
            customers = CustomerTools.get_all_customers(self.db)

            if not customers:
                return "No customers found."

            text = ""
            for customer in customers:
                text += (
                    f"Name: {customer['name']}\n"
                    f"Email: {customer['email']}\n"
                    f"Phone: {customer['phone']}\n\n"
                )

            return text

        if intent == "GET_CUSTOMER":
            name = self.router.extract_customer_name(message)
            if name is None:
                return "Customer not found."

            customer = CustomerTools.get_customer_by_name(self.db, name)

            if customer is None:
                return "Customer not found."

            return (
                f"Name: {customer['name']}\n"
                f"Email: {customer['email']}\n"
                f"Phone: {customer['phone']}"
            )

        if intent == "CALL_MEMORY":
            if customer_id is None:
                return "Customer ID is required to retrieve call memory."
            return self.memory_service.get_customer_memory(self.db, customer_id)

        return None
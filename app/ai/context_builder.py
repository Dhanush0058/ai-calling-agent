from app.memory.memory_service import MemoryService
from app.profile.profile_service import ProfileService


class ContextBuilder:

    def __init__(
        self,
        db,
        customer_id,
    ):
        self.db = db
        self.customer_id = customer_id

    def build(self, relevant_calls: str | None = None):

        profile = ProfileService(
            self.db
        ).get_profile(
            self.customer_id
        )

        memory = MemoryService().get_customer_memory(
            self.db,
            self.customer_id,
        )

        context = {
            "profile": profile,
            "memory": memory,
        }

        if relevant_calls is not None:
            context["relevant_calls"] = relevant_calls

        return context


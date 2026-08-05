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

    def build(self):

        profile = ProfileService(
            self.db
        ).get_profile(
            self.customer_id
        )

        memory = MemoryService(
            self.db
        ).get_customer_memory(
            self.customer_id
        )

        return {
            "profile": profile,
            "memory": memory,
        }


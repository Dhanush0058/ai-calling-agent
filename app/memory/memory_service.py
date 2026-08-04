from app.memory.memory_manager import MemoryManager
from app.memory.memory_retriever import MemoryRetriever


class MemoryService:

    def __init__(self, window_days: int = 30, max_calls: int = 5):
        self.retriever = MemoryRetriever(window_days=window_days, max_calls=max_calls)
        self.manager = MemoryManager()

    def get_customer_memory(self, db, customer_id: int) -> str:
        calls = self.retriever.fetch_recent_calls(db, customer_id)
        return self.manager.build_memory_context(calls)

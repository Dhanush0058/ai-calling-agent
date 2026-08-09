from __future__ import annotations

from typing import Literal

try:
    from sentence_transformers import SentenceTransformer
except Exception:  # pragma: no cover - optional dependency in lightweight environments
    SentenceTransformer = None

try:
    from sklearn.metrics.pairwise import cosine_similarity
except Exception:  # pragma: no cover - optional dependency in lightweight environments
    cosine_similarity = None

IntentName = Literal[
    "CUSTOMER_COUNT",
    "CUSTOMER_LIST",
    "GET_CUSTOMER",
    "CALL_MEMORY",
    "GENERAL_CHAT",
]

INTENT_EXAMPLES = {
    "CUSTOMER_COUNT": [
        "How many customers do we have?",
        "Total customers",
        "Count of customers",
        "Customer count",
        "Number of customers",
        "How many people signed up?",
        "How many registered users do we have?",
        "How many customers are there?",
        "Customer total",
        "Total number of customers",
    ],
    "CUSTOMER_LIST": [
        "Show all customers",
        "List customers",
        "Customer details",
        "Get customer list",
        "Display all customer records",
        "Show all customer information",
    ],
    "GET_CUSTOMER": [
        "Find customer by name",
        "Get customer details for John",
        "Show customer Alice",
        "Find user Sita",
        "Get customer record",
        "Show user info",
        "Get details for customer David",
    ],
    "CALL_MEMORY": [
        "What happened last time?",
        "What did I call about yesterday?",
        "Remind me about my previous complaint.",
        "Show my last conversation.",
        "Tell me about my previous calls.",
        "What did we discuss in my last call?",
    ],
    "GENERAL_CHAT": [
        "Tell me a joke",
        "Summarize the last conversation",
        "How are you?",
        "What should I do next?",
        "Give me a recommendation",
    ],
}

MODEL_NAME = "BAAI/bge-m3"


class SemanticIntentRouter:

    def __init__(self):
        self.model = None
        self.intent_embeddings = {}
        # Load lazily at runtime instead of during app import so the test suite and
        # startup path do not trigger the heavy SentenceTransformer model download.

    def _ensure_model_ready(self):
        if self.model is not None or SentenceTransformer is None:
            return

        try:
            self.model = SentenceTransformer(MODEL_NAME)
            self.intent_embeddings = {
                intent: self.model.encode(examples, convert_to_numpy=True)
                for intent, examples in INTENT_EXAMPLES.items()
            }
        except Exception:
            self.model = None
            self.intent_embeddings = {}

    def _fallback_predict(self, message: str) -> IntentName:
        normalized = message.lower()

        if any(token in normalized for token in ["how many", "total", "count", "number of", "customers", "users"]):
            return "CUSTOMER_COUNT"
        if any(token in normalized for token in ["list", "show all", "display", "all customers", "customer list"]):
            return "CUSTOMER_LIST"
        if any(token in normalized for token in ["find", "show", "customer", "user", "details"]):
            return "GET_CUSTOMER"
        if any(token in normalized for token in ["last time", "previous", "remember", "history", "conversation", "call"]):
            return "CALL_MEMORY"
        return "GENERAL_CHAT"

    def predict(self, message: str) -> IntentName:
        self._ensure_model_ready()

        if self.model is None or cosine_similarity is None:
            return self._fallback_predict(message)

        message_embedding = self.model.encode([message], convert_to_numpy=True)

        best_intent = "GENERAL_CHAT"
        best_score = -1.0

        for intent, embeddings in self.intent_embeddings.items():
            score = cosine_similarity(message_embedding, embeddings).max()
            if score > best_score:
                best_score = float(score)
                best_intent = intent

        return best_intent

    @staticmethod
    def extract_customer_name(message: str) -> str | None:
        normalized = message.strip()
        lower = normalized.lower()

        for marker in ["customer", "user"]:
            if marker in lower:
                parts = lower.split(marker, 1)[1].strip()
                if parts:
                    words = parts.split()
                    if words:
                        return words[-1].strip().title()

        if lower.startswith("find") or lower.startswith("show"):
            tokens = normalized.split()
            if tokens:
                return tokens[-1].strip().title()

        return None


router = SemanticIntentRouter()

class MemoryStore:
    def __init__(self):
        self.history = []

    def get_context(self):
        return self.history[-1] if self.history else ""

    def update_context(self, user_input, result):
        self.history.append({"query": user_input, "result": result})

memory_store = MemoryStore()

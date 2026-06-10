from lark import Lark, Transformer

class RAGTransformer(Transformer):
    def STRING(self, s):
        return str(s)[1:-1]
        
    def INT(self, n):
        return int(n)

    def load_cmd(self, items):
        return {"action": "load_documents", "path": items[0]}

    def chunk_cmd(self, items):
        return {"action": "configure_chunking", "chunk_size": items[0], "overlap": items[1]}

    def agent_cmd(self, items):
        return {"action": "initialize_agent", "agent_name": items[0], "model_type": items[1]}

    # NEW: Tell Python how to handle the QUERY command
    def query_cmd(self, items):
        return {"action": "run_query", "question": items[0]}

    def start(self, items):
        return items
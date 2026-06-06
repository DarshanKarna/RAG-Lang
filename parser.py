from lark import Lark, Transformer

# 1. The Transformer Class
# This tells Python what to do when it recognizes a rule from grammar.lark
class RAGTransformer(Transformer):
    
    # Remove the quotation marks from strings (e.g., '"gpt-4o"' -> 'gpt-4o')
    def STRING(self, s):
        return str(s)[1:-1]
        
    # Convert text numbers into real Python integers
    def INT(self, n):
        return int(n)

    # When it sees a LOAD command, create a Python dictionary
    def load_cmd(self, items):
        return {"action": "load_documents", "path": items[0]}

    # When it sees a CHUNK command, map the size and overlap
    def chunk_cmd(self, items):
        return {"action": "configure_chunking", "chunk_size": items[0], "overlap": items[1]}

    # When it sees an AGENT command, map the name and model
    def agent_cmd(self, items):
        return {"action": "initialize_agent", "agent_name": items[0], "model_type": items[1]}

    # The starting point: just return the list of all processed instructions
    def start(self, items):
        return items

# 2. Main Execution Block
if __name__ == "__main__":
    
    # Read our grammar rules
    with open("grammar.lark", "r") as f:
        grammar = f.read()

    # Read the user's custom script
    with open("test.rag", "r") as f:
        script_content = f.read()

    # Initialize Lark with our grammar and our Transformer
    parser = Lark(grammar, parser='lalr', transformer=RAGTransformer())

    try:
        # Do the actual parsing!
        parsed_ast = parser.parse(script_content)
        
        print("\n✅ --- Compilation Successful! ---")
        print("Generated Abstract Syntax Tree (AST):\n")
        
        # Print out the resulting Python dictionaries
        for instruction in parsed_ast:
            print(instruction)
            
    except Exception as e:
        print("\n❌ --- Syntax Error! ---")
        print(e)
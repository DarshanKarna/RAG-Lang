import time
from lark import Lark
from parser import RAGTransformer

# ==========================================
# 1. The Backend Logic (Simulated AI Tasks)
# ==========================================
# In the future, these functions will import your actual 4th-sem project code!

def load_documents(path):
    print(f"📄 [Ingestion Engine] Loading documents from: {path}...")
    time.sleep(1) # Simulating processing time
    print("   -> Success: Found and loaded 15 PDFs.\n")

def configure_chunking(size, overlap):
    print(f"✂️  [Text Splitter] Splitting text (Size: {size}, Overlap: {overlap})...")
    time.sleep(1)
    print("   -> Success: Generated 42 vector chunks.\n")

def initialize_agent(name, model):
    print(f"🤖 [Agent Framework] Initializing '{name}' with LLM: '{model}'...")
    time.sleep(1)
    print(f"   -> Success: Agent {name} is online and ready for queries.\n")

# ==========================================
# 2. The Interpreter (The AST Router)
# ==========================================
def execute_pipeline(ast):
    print("\n🚀 Starting RAG-Lang Execution Pipeline...\n")
    print("-" * 50)
    
    # Loop through the instructions our parser gave us
    for step in ast:
        action = step.get("action")

        # Map the text command to the actual Python function
        if action == "load_documents":
            load_documents(step["path"])
            
        elif action == "configure_chunking":
            configure_chunking(step["chunk_size"], step["overlap"])
            
        elif action == "initialize_agent":
            initialize_agent(step["agent_name"], step["model_type"])
            
        else:
            print(f"⚠️ Error: Unknown action mapped -> {action}")
            
    print("-" * 50)
    print("✅ Pipeline Execution Complete!\n")

# ==========================================
# 3. Main Execution Block
# ==========================================
if __name__ == "__main__":
    try:
        # Load the grammar and the user script
        with open("grammar.lark", "r") as f:
            grammar = f.read()
        with open("test.rag", "r") as f:
            script_content = f.read()

        # Step A: Compile the script into an AST
        dsl_parser = Lark(grammar, parser='lalr', transformer=RAGTransformer())
        parsed_ast = dsl_parser.parse(script_content)

        # Step B: Execute the AST
        execute_pipeline(parsed_ast)

    except Exception as e:
        print("\n❌ Execution Failed. Check your syntax in test.rag.")
        print(e)
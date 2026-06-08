import fitz  # PyMuPDF
from lark import Lark
from parser import RAGTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. NEW: Import LangChain core components for our Agent
from langchain_core.prompts import ChatPromptTemplate

# Global memory
PIPELINE_STATE = {
    "raw_text": "",
    "text_chunks": [],
    "agent_config": None  # NEW: A place to store our Agent's brain
}

def load_documents(filepath):
    print(f"📄 [Ingestion] Opening PDF: '{filepath}'...")
    doc = fitz.open(filepath)
    extracted_text = ""
    for page in doc:
        extracted_text += page.get_text()
    PIPELINE_STATE["raw_text"] = extracted_text
    print(f"   -> Success: Extracted {len(extracted_text)} characters.\n")

def configure_chunking(size, overlap):
    print(f"✂️  [Chunking] Slicing text (Size: {size}, Overlap: {overlap})...")
    raw_text = PIPELINE_STATE["raw_text"]
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=size, chunk_overlap=overlap)
    chunks = text_splitter.split_text(raw_text)
    PIPELINE_STATE["text_chunks"] = chunks
    print(f"   -> Success: Sliced text into {len(chunks)} distinct blocks.\n")

# 2. NEW: The Agent Configuration Function
def initialize_agent(name, model):
    print(f"🤖 [Agent Framework] Configuring '{name}' with LLM: '{model}'...")
    
    # Dynamically build the system instructions using the name from the DSL
    system_instructions = f"You are {name}, an expert AI assistant. Answer the user's questions based ONLY on the provided document chunks."
    
    # Create a real LangChain Prompt Template
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_instructions),
        ("human", "Context: {context}\n\nQuestion: {user_query}")
    ])
    
    # Save it to our state memory so it is ready to use
    PIPELINE_STATE["agent_config"] = {
        "prompt": prompt_template,
        "model_type": model
    }
    
    print(f"   -> Success: LangChain Prompt built for {name}.\n")
    print(f"Preview of System Prompt:\n\"{system_instructions}\"\n")

def execute_pipeline(ast):
    for step in ast:
        if step.get("action") == "load_documents":
            load_documents(step["path"])
        elif step.get("action") == "configure_chunking":
            configure_chunking(step["chunk_size"], step["overlap"])
        # 3. NEW: Route the agent command to our new function
        elif step.get("action") == "initialize_agent":
            initialize_agent(step["agent_name"], step["model_type"])

if __name__ == "__main__":
    with open("grammar.lark", "r") as f:
        grammar = f.read()
        
    with open("test.rag", "r") as f:
        script_content = f.read()

    dsl_parser = Lark(grammar, parser='lalr', transformer=RAGTransformer())
    parsed_ast = dsl_parser.parse(script_content)
    
    print("\n🚀 Starting RAG-Lang Execution...\n" + "-"*50)
    execute_pipeline(parsed_ast)
    print("-" * 50 + "\n✅ Pipeline Complete!\n")
import sys
import fitz  # PyMuPDF
from lark import Lark
from parser import RAGTransformer

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate

PIPELINE_STATE = {
    "raw_text": "",
    "text_chunks": [],
    "agent_config": None
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

def initialize_agent(name, model):
    print(f"🤖 [Agent Framework] Configuring '{name}' with LLM: '{model}'...")
    system_instructions = f"You are {name}, an expert AI assistant. Answer the user's questions based ONLY on the provided document chunks."
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_instructions),
        ("human", "Context: {context}\n\nQuestion: {user_query}")
    ])
    PIPELINE_STATE["agent_config"] = {"prompt": prompt_template, "model_type": model}
    print(f"   -> Success: LangChain Prompt built.\n")

# ==========================================
# NEW: The Query Execution Function
# ==========================================
def run_query(question):
    print(f"🔎 [Execution] Running Query: '{question}'...")
    
    # 1. Grab the Agent's brain
    agent_prompt = PIPELINE_STATE["agent_config"]["prompt"]
    
    # 2. Simulate Retrieval: Grab the first 2 chunks of our PDF to act as context
    retrieved_context = "\n\n".join(PIPELINE_STATE["text_chunks"][:2])
    
    # 3. Format the final payload for the LLM
    final_payload = agent_prompt.format_messages(
        context=retrieved_context,
        user_query=question
    )
    
    print("   -> Success: RAG Context Successfully Merged!\n")
    print("================ FINAL LLM PAYLOAD ================")
    print(final_payload[0].content) # Prints the System prompt
    print("-" * 50)
    print(final_payload[1].content) # Prints the Context + User Question
    print("===================================================\n")

def execute_pipeline(ast):
    for step in ast:
        if step.get("action") == "load_documents":
            load_documents(step["path"])
        elif step.get("action") == "configure_chunking":
            configure_chunking(step["chunk_size"], step["overlap"])
        elif step.get("action") == "initialize_agent":
            initialize_agent(step["agent_name"], step["model_type"])
        # NEW: Route the query command
        elif step.get("action") == "run_query":
            run_query(step["question"])

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
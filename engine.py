import fitz  # This is PyMuPDF
from lark import Lark
from parser import RAGTransformer

# Global memory to hold our extracted text
PIPELINE_STATE = {
    "raw_text": ""
}

def load_documents(filepath):
    print(f"Opening PDF: '{filepath}'...")
    
    # 1. Open the PDF using PyMuPDF
    doc = fitz.open(filepath)
    extracted_text = ""
    
    # 2. Loop through every page and grab the text
    for page in doc:
        extracted_text += page.get_text()
        
    # 3. Save it to our memory
    PIPELINE_STATE["raw_text"] = extracted_text
    
    print(f"   -> Success: Extracted {len(extracted_text)} characters of text.\n")
    
    # Let's print the first 100 characters just to prove it worked!
    print("Preview: ", extracted_text[:100], "...\n")

def execute_pipeline(ast):
    for step in ast:
        if step.get("action") == "load_documents":
            load_documents(step["path"])

if __name__ == "__main__":
    with open("grammar.lark", "r") as f:
        grammar = f.read()
        
    with open("test.rag", "r") as f:
        script_content = f.read()

    dsl_parser = Lark(grammar, parser='lalr', transformer=RAGTransformer())
    parsed_ast = dsl_parser.parse(script_content)
    
    execute_pipeline(parsed_ast)
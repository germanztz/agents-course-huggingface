import llama_index
from llama_index.llms.ollama import Ollama 
from llama_index.core.agent.workflow import ReActAgent, AgentWorkflow
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import SimpleDirectoryReader
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import SentenceSplitter

import chromadb

import asyncio
import os
from dotenv import load_dotenv
import glob
import PyPDF2
    

DATA_PATH = "chat-neus-catala/data/"
embedding_model = OllamaEmbedding(model_name="qllama/bge-small-en-v1.5:f16")
llm = Ollama(model="qwen2.5:7b-instruct")


def digest_pdf(pdf_file: str) -> str:
    """
    Returns the text content of a PDF file.

    Parameters:
    pdf_file (str): The path to the PDF file.

    Returns:
    str: The text content of the PDF file.
    """
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text()
    print('Text extracted',text[:100])
    # white text in a file named after the pdf in the digest folder
    with open(DATA_PATH + 'digest/' + os.path.basename(pdf_file) + '.txt', 'w') as f:
        f.write(text)    
    
    return text

async def process_new_files():
    pdf_files = glob.glob(DATA_PATH + 'documents/*.pdf')
    print('New files',pdf_files)
    digested_files = glob.glob(DATA_PATH + 'digest/*.txt')
    print('Digested files',digested_files)
    #remove .txt extension from digested files
    digested_files = [file[:-4] for file in digested_files]
    new_files = [file for file in pdf_files if file not in digested_files]
    print('New files',new_files)

    for file in new_files:
        digest_pdf(file)
    # TODO: add only new files to vector_store

    reader = SimpleDirectoryReader(input_dir=DATA_PATH + 'digest/', recursive=False)
    documents = reader.load_data()


    db = chromadb.PersistentClient(path=DATA_PATH + 'chroma_db/neus_catala.db')
    chroma_collection = db.get_or_create_collection(name="neus_catala")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

    pipeline = IngestionPipeline(
        transformations=[
            SentenceSplitter(),
            embedding_model
        ],
        vector_store=vector_store,
    )
    nodes = await pipeline.arun(documents=documents)
    len(nodes)

asyncio.run(process_new_files())

# Load environment variables from .env file
# load_dotenv()


# llama_index.core.set_global_handler(
#     "arize_phoenix", 
#     endpoint="https://llamatrace.com/v1/traces"
# )




# # we can pass functions directly without FunctionTool -- the fn/docstring are parsed for the name/description
# multiply_agent = ReActAgent(
#     name="multiply_agent",
#     description="Is able to multiply two integers",
#     system_prompt="A helpful assistant that can use a tool to multiply numbers.",
#     tools=[multiply], 
#     llm=llm,
# )

# addition_agent = ReActAgent(
#     name="addition_agent",
#     description="Is able to add two integers",
#     system_prompt="A helpful assistant that can use a tool to add numbers.",
#     tools=[add], 
#     llm=llm,
# )

# menu_agent = ReActAgent(
#     name="menu_agent",
#     description="Is able to suggest a menu based when the occasion is mentioned.",
#     system_prompt="A helpful assistant that can use a tool to suggest a menu based on the occasion.",
#     tools=[suggest_menu], 
#     llm=llm,
# )

# # Create the workflow
# workflow = AgentWorkflow(
#     agents=[multiply_agent, addition_agent, menu_agent],
#     root_agent="multiply_agent"
# )

# async def run_workflow(user_msg: str):
#     response = await workflow.run(user_msg=user_msg)
#     print(response.response.blocks[0].text)

# Run the system

# asyncio.run(run_workflow(user_msg="print a list of items for a menu for the party in formal ocasion."))
text = """El domingo 16 de diciembre de 1962 Ardiaca fue detenido al salir de una reunión de partido celebrada en un piso de la Plaza de Santa Eulàlia de - 74 -Barcelona, junto al campesino sabadellense Joan Tena Folch y al carpintero José Ramírez Moreno"""
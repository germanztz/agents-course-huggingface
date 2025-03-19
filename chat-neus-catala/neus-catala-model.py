import llama_index
from llama_index.llms.ollama import Ollama 
from llama_index.core.agent.workflow import ReActAgent, AgentWorkflow, ToolCallResult, AgentStream
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import SimpleDirectoryReader
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import SentenceSplitter
# from llama_index.core.node_parser import TokenTextSplitter
from llama_index.core import VectorStoreIndex
from llama_index.core.tools import QueryEngineTool
from llama_index.core.prompts import PromptTemplate
from llama_index.core.evaluation import FaithfulnessEvaluator
import nest_asyncio
import pandas as pd

import chromadb

import asyncio
import os
from dotenv import load_dotenv
import glob
import PyPDF2

# Load environment variables from .env file
load_dotenv()
llama_index.core.set_global_handler(
    "arize_phoenix", 
    endpoint="https://llamatrace.com/v1/traces"
)

DATA_PATH = "chat-neus-catala/data/"
embedding_model = OllamaEmbedding(model_name="qllama/bge-small-en-v1.5:f16")
llm = Ollama(model="qwen2.5:7b-instruct") # Funciona de manera satisfactoria
# llm = Ollama(model="llama3.1:8b-instruct-q3_K_S")
# llm = Ollama(model="qwen2.5:32b-instruct")
# llm = Ollama(model="deepseek-r1:latest")


db = chromadb.PersistentClient(path=DATA_PATH + 'neus_catala.db')
chroma_collection = db.get_or_create_collection(name="neus_catala")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

#regex to clean double new lines
import re
rx_nl = re.compile(r'(\n\s*\n)')
rx_hyphen = re.compile(r'(-\n)')
rx_notdot = re.compile(r'(?<!\.)\n')
rx_num_leter = re.compile(r'(\d)([a-zA-Z])')

def clean_text(text: str) -> str:
    text = rx_nl.sub('\n', text)
    text = rx_hyphen.sub('', text)
    text = rx_notdot.sub(' ', text)
    text = rx_num_leter.sub(r'\1 \2', text)
    return text

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

    text = clean_text(text)
    file_path = DATA_PATH + 'digest/' + os.path.basename(pdf_file) + '.txt'
    # white text in a file named after the pdf in the digest folder
    with open(file_path, 'w') as f:
        f.write(text)    
    
    print(f'{file_path} length:',len(text))
    return file_path

def digest_pdf_list(pdf_files: list) -> list:
    return [digest_pdf(pdf_file) for pdf_file in pdf_files]

async def embed_files(new_files):
    if new_files is None or len(new_files) == 0:
        print('No new files')
        return

    try:
        new_files = digest_pdf_list(new_files)

        reader = SimpleDirectoryReader(input_files=new_files)
        documents = reader.load_data()
        # print('Documents',documents)

        pipeline = IngestionPipeline(
            transformations=[
                SentenceSplitter(chunk_size=200),
                # TokenTextSplitter(chunk_size=512),
                embedding_model
            ],
            vector_store=vector_store,
        )
        nodes = await pipeline.arun(documents=documents)
    except Exception as e:
        print(f"Error: {e})")

async def process_new_files():
    pdf_files = glob.glob(DATA_PATH + 'documents/*.pdf')
    # print('New files',pdf_files)
    digested_files = glob.glob(DATA_PATH + 'digest/*.txt')
    # get the filename of the digested files no extension, no path
    digested_files = [os.path.basename(file).split('.')[0] for file in digested_files]
    # print('Digested files',digested_files)
    new_files = [file for file in pdf_files if os.path.basename(file).split('.')[0] not in digested_files]
    # print('New files',new_files)
    print('digested files',new_files)
    await embed_files(new_files)


index = VectorStoreIndex.from_vector_store(
    vector_store=vector_store, embed_model=embedding_model
)


query_engine = index.as_query_engine(llm=llm)
query_engine_tool = QueryEngineTool.from_defaults(
    query_engine=query_engine,
    name="neus catala engine",
    description="Respon a les preguntes de l'usuari en catala",
)

# Create a RAG agent
query_engine_agent = AgentWorkflow.from_tools_or_functions(
    tools_or_functions=[query_engine_tool],
    llm=llm,
    system_prompt="You are a helpful assistant that has access to a database containing informatin about books. ",
)

evaluator = FaithfulnessEvaluator(llm=llm)


async def answer_question():
    tests = [
        {"question": "Que havien de passar Les presoneres de Ravensbrück abans d incorporar-se als treballs forçats?", "Correct response": "Quarentena."},
        {"question": "La Neus Catala considera que va tenir una infància com?", "Correct response": "feliç"},
        {"question": "La mateixa Neus, que presideix l Amical, va fer el discurs de presentació al paranimf de la Universitat de Barcelona, el juny de quin any?", "Correct response": "2006"},
        {"question": "La Neus va néixer als Guiamets, un poblet de la comarca tarragonina del Priorat, a quin any?", "Correct response": "1915"},
        {"question": "A principis del segle passat, a Els Guiamets hi arribava gent de quin pais?", "Correct response": "França"},
        {"question": "En Baltasar Català era un pagès que combinava el treball al camp amb que mes?", "Correct response": "barber i pintor"},
        {"question": "Quina fundació va fer el treball biogràfic sobre la Neus Catala?", "Correct response": "Fundació Pere Ardiaca"},
        {"question": "Els diumenges a la tarda es reunia amb els camarades i les seves famílies en quin lloc?", "Correct response": "un petit teatret"},
        {"question": "En aquell temps, el que més desitjava la Neus era treballar on?", "Correct response": "un bon hospital"},
        {"question": "Qui era el Francisco Serrano?", "Correct response": "el jove que els repartia la sopa a la presó"},
        {"question": "Les cendres d algunes d aquestes dones es troben en quin lloc?", "Correct response": "al fons del llac Schwedt"},     
    ]

    for test in tests:
        question_str = f'respond in calatan, in less than 5 words: {test["question"]}'
        print('\n\n**********Question:************\n',question_str, 'Response:',test['Correct response'])

        # test['default_response'] = await llm.apredict(PromptTemplate(question_str))
        test['default_response'] = llm.complete(question_str)
        
        print('*Default response:',test['default_response'])

        nest_asyncio.apply()  # This is needed to run the query engine
        test['informed_response'] = query_engine.query(question_str)
        print('*Informed response:',test['informed_response'])

        # handler = query_engine_agent.run(question)

        # # async for ev in handler.stream_events():
        # #     if isinstance(ev, ToolCallResult):
        # #         print("")
        # #         print("Called tool: ", ev.tool_name, ev.tool_kwargs, "=>", ev.tool_output)
        # #     elif isinstance(ev, AgentStream):  # showing the thought process
        # #         print(ev.delta, end="", flush=True)

        # informed_response = await handler    
        # print('*Informed agent response:',informed_response)
    
        test['informed_response_passing'] = evaluator.evaluate_response(query=test['question'], response=test['informed_response']).score

    df = pd.DataFrame(tests)
    print(df)

        # print dict questions table formated

asyncio.run(process_new_files())

asyncio.run(answer_question())



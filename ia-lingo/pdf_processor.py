"""
Módulo para procesar archivos PDF usando Ollama embeddings y el modelo qwen3
para extraer preguntas de opción múltiple.
"""

import PyPDF2
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import VectorStoreIndex
from langchain_core.documents import Document

# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_openai import ChatOpenAI
# from langfuse.langchain import CallbackHandler
import json
import os
from typing import List, Optional, Literal, TypedDict, Dict, Tuple, Any, Annotated

system_prompt = """You are a teacher who is preparing a quiz. 
You are preparing a quiz for students. 
Extract every keyword and concept and its definition from the text. 
Generate a question about the keyword or concept and its answer.
Only generate a question if you can point the answer
Use Catalan language.

Example Source:
4.1 Què és OAUTH2?
  És un estàndard obert d’autorització que permet que aplicacions de tercers puguin obtenir accés limitat a serveis web.
4.2 Característiques de OAUTH2
- Seguretat i delegació: No comparteix les credencials de l’usuari; utilitza tokens.
- Arquitectura basada en rols: Per a cada element del flux.
- Múltiples fluxos d’autorització: Tipus de concessió (grant types) adaptats a diferents tipus d’aplicacions i casos d’ús (ex: codi d’autorització, autorització implícita, credencialsdel propietari del recurs, credencials del client).

Example question 1:
- question: Què és OAUTH2?
- answer: És un estàndard obert d’autorització que permet que aplicacions de tercers puguin obtenir accés limitat a serveis web.
- source: {Example Source}

Example question 2:
- question: És la Seguretat una caracteristica de OAUTH2?
- answer: Si, No comparteix les credencials de l’usuari; utilitza tokens.
- source: {Example Source}

Example question 3:
- question: Què es la "autorització implícita" en OAUTH2?
- answer: Es un "flux d’autorització"
- source: {Example Source}
/no_think"""


class Question(TypedDict):
    """A question to be asked in a quiz."""
    question: Annotated[str, "The question in afirmative form."]
    answer: Annotated[str, "The correct answer."]

class QuestionList(TypedDict):
    """A collection of questions."""
    questions: List[Question]

file_dir = lambda f: os.path.dirname(f)
file_name = lambda f: os.path.basename(f)
file_prefix = lambda f: os.path.splitext(file_name(f))[0]
file_ext = lambda f: os.path.splitext(file_name(f))[1]
vs_path = lambda f: f + ".vs"
json_path = lambda f: f + ".json"

async def split_pdf(file_path:str) -> list[Document]:
    # Load and split PDF
    loader = PyPDFLoader(file_path)
    return loader.load_and_split()

async def split_text(file_path:str, encoding="utf-8") -> list[Document]:
    with open(file_path, "r", encoding=encoding) as f:
        return [Document(page_content=f.read(), metadata={"source": file_path, 'page_label':'1'})]

async def to_vector_store(file_path:str, chunk_size=1000, chunk_overlap=200):
    """
    Converts a PDF file into a Chroma vector store.

    Args:
        file_path (str): The path to the PDF file.

    Returns:
        Chroma: A Chroma vector store containing the PDF's content.
    """
    embedding=OllamaEmbeddings(model="nomic-embed-text")
    if os.path.isdir(vs_path(file_path)):
        return Chroma(persist_directory=vs_path(file_path), collection_name=file_name(file_path).replace(' ','_'), embedding_function=embedding)
    documents = []
    match file_ext(file_path).lower():
        case '.pdf':
            documents = await split_pdf(file_path=file_path)
        case '.md' | '.txt':
            documents = await split_text(file_path=file_path)

    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    
    # Create vector store
    return Chroma.from_documents(
        documents=text_splitter.split_documents(documents),
        collection_name=file_name(file_path).replace(' ','_'),
        embedding=embedding,
        persist_directory=vs_path(file_path)
        )

async def get_nodes(vectorstore: Chroma) -> List[Document]:
    """Retrieves all documents and their metadata from the Chroma vectorstore.

    Args:
        vectorstore (Chroma): The Chroma vectorstore to retrieve from.

    Returns:
        List[Document]: A list of Document objects, each containing the page content and metadata.
    """

    results = vectorstore.get(include=["documents", "metadatas"])
    nodes = []
    for i in range(len(results["ids"])):
        node = Document(
            id=results["ids"][i],
            page_content=results["documents"][i],
            metadata=results["metadatas"][i],
        )
        nodes.append(node)
    return nodes

async def store_questions(sqlitedb:str, questions: List[Dict[str, Any]]) -> None:
    async with sqlite3.connect(sqlitedb) as conn:
        # create table questions if dont exists
        await conn.execute(f"CREATE TABLE IF NOT EXISTS questions (question TEXT, answer TEXT, source TEXT)")
        for question in questions:
            await conn.execute(f"INSERT INTO questions (question, answer, source) VALUES (?, ?)",
                (question["question"], question["answer"], question["source"])
                )


async def process_pdf_with_ollama(file_path: str) -> Tuple[List[Dict[str, Any]], str]:
    """
    Process PDF file using Ollama embeddings and qwen3 model to extract questions.
    
    Args:
        file_path (str): Ruta al archivo PDF
        
    Returns:
        Tuple[List[Dict[str, Any]], str]: Lista de preguntas extraídas y ruta al archivo JSON guardado
        
    Raises:
        Exception: Si ocurre un error durante el procesamiento del PDF
    """
    # try:
    vectorstore = await to_vector_store(file_path)
    nodes = await get_nodes(vectorstore)
            
    llm_model = ChatOllama(model="qwen3")
    # llm_model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.2)
    # llm_model = ChatOpenAI(model="qwen-plus", api_key=os.getenv('DASHSCOPE_API_KEY'), base_url=os.getenv('DASHSCOPE_BASE_URL'))

    # Extract questions using qwen3 model
    questions = []
    
    for i, node in enumerate(nodes):
        try:
            # response = ollama.chat(model='qwen3', messages=[{'role': 'user', 'content': prompt}])
            response = await llm_model.with_structured_output(QuestionList).ainvoke([
                {'role': 'system', 'content': system_prompt}, 
                {'role': 'user', 'content': node.page_content}])
            for question in response['questions']:
                question["source"] = f"Page {node.metadata["page_label"]}: {node.page_content}"
                questions.append(question)
                # Save questions to JSON file with PDF name
                with open(json_path(file_path), 'a', encoding='utf-8') as f:
                    f.write(",\n")
                    json.dump(question, f, ensure_ascii=False, indent=2)

        except Exception as e:
            print(f"Error processing node {i}: {str(e)}")
            continue
    
    # If no questions were extracted, return an empty list
    if len(questions) == 0:
        print("No questions extracted from PDF")
        return [], None
    
    return questions, json_path(file_path)
        
    # except Exception as e:
    #     print(f"Detailed error: {str(e)}")
    #     raise Exception(f"Error processing File: {str(e)}")

if __name__ == "__main__":

    import asyncio

    async def main():
        # print(await process_pdf_with_ollama(
        #     "/home/daimler/workspaces/agents-course-huggingface/ia-lingo/uploads/test.pdf" ))
        print(await process_pdf_with_ollama(
            "/home/daimler/workspaces/agents-course-huggingface/tmb resp tecnico.md" ))
            
        # vs = await to_vector_store("/home/daimler/workspaces/agents-course-huggingface/ia-lingo/uploads/test.pdf" )
        # print(await get_nodes(vs))

    asyncio.run(main())
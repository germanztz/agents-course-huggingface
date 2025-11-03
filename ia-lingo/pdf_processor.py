"""
Módulo para procesar archivos PDF usando Ollama embeddings y el modelo qwen3
para extraer preguntas de opción múltiple.
"""

import json
import os
from typing import List, Dict, Tuple, Any


def process_pdf_with_ollama(pdf_path: str, pdf_filename: str) -> Tuple[List[Dict[str, Any]], str]:
    """
    Process PDF file using Ollama embeddings and qwen3 model to extract questions.
    
    Args:
        pdf_path (str): Ruta al archivo PDF
        pdf_filename (str): Nombre del archivo PDF
        
    Returns:
        Tuple[List[Dict[str, Any]], str]: Lista de preguntas extraídas y ruta al archivo JSON guardado
        
    Raises:
        Exception: Si ocurre un error durante el procesamiento del PDF
    """
    try:
        import PyPDF2
        from langchain_community.document_loaders import PyPDFLoader
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        from langchain_community.embeddings import OllamaEmbeddings
        from langchain_community.vectorstores import Chroma
        import ollama

        # Load and split PDF
        loader = PyPDFLoader(pdf_path)
        pages = loader.load_and_split()
        
        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        chunks = text_splitter.split_documents(pages)
        
        # Create embeddings using Ollama
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        
        # Create vector store
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=os.path.join(os.path.dirname(pdf_path), "vectorstore")
        )
        
        # Extract questions using qwen3 model
        questions = []
        
        for i, chunk in enumerate(chunks):
            # Use qwen3 model to extract questions from each chunk
            prompt = f"""Del siguiente texto, extrae preguntas de opción múltiple con 4 respuestas cada una. 
            Para cada pregunta, proporciona: pregunta, opciones (array de 4), respuesta_correcta (índice 0-3), 
            una pista (hint) y una explicación. Formato JSON.
            
Texto: {chunk.page_content}"""
            
            try:
                response = ollama.chat(model='qwen3', messages=[
                    {'role': 'user', 'content': prompt}
                ])
                
                # Parse the response (assuming it returns JSON)
                if isinstance(response, dict) and 'message' in response and 'content' in response['message']:
                    content = response['message']['content']
                    # Try to parse as JSON, if it fails, try to extract JSON from the string
                    try:
                        extracted_data = json.loads(content)
                    except json.JSONDecodeError:
                        # Try to find JSON-like structure in the content
                        import re
                        json_match = re.search(r'\[.*\]', content, re.DOTALL)
                        if json_match:
                            extracted_data = json.loads(json_match.group(0))
                        else:
                            json_match = re.search(r'\{.*\}', content, re.DOTALL)
                            if json_match:
                                extracted_data = [json.loads(json_match.group(0))]
                            else:
                                print(f"Could not parse response as JSON: {content}")
                                continue
                
                # If it's a single question, wrap in list
                if isinstance(extracted_data, dict) and 'pregunta' in extracted_data:
                    extracted_data = [extracted_data]
                
                # Add questions to list with ID
                for q in extracted_data:
                    if isinstance(q, dict) and 'pregunta' in q:
                        q['id'] = len(questions) + 1
                        questions.append(q)
                        
            except Exception as e:
                print(f"Error processing chunk {i}: {str(e)}")
                continue
        
        # If no questions were extracted, return an empty list
        if len(questions) == 0:
            print("No questions extracted from PDF")
            return [], None
        
        # Save questions to JSON file with PDF name
        json_filename = os.path.splitext(pdf_filename)[0] + '.json'
        json_path = os.path.join(os.path.dirname(pdf_path), json_filename)
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(questions, f, ensure_ascii=False, indent=2)
        
        return questions, json_path
        
    except Exception as e:
        print(f"Detailed error: {str(e)}")
        raise Exception(f"Error processing PDF: {str(e)}")
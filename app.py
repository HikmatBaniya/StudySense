import streamlit as st
import os
import yaml
import logging
from models.mistral_runner import MistralRunner
from models.embedder import Embedder
from services.vector_db import VectorDB
from services.document_parser import DocumentParser
from services.database import Database
from utils.text_splitter import TextSplitter

# Setup logging
logging.basicConfig(filename='logs/app.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_config():
    try:
        with open('configs/config.yaml', 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        st.error("Configuration error. Please check logs.")
        return {}

def main():
    config = load_config()
    if not config:
        return

    # Initialize components
    try:
        mistral = MistralRunner(config['model'])
        embedder = Embedder(config['embedding_model'])
        vector_db = VectorDB(config['vector_db'])
        parser = DocumentParser()
        splitter = TextSplitter(config['chunking']['chunk_size'], config['chunking']['chunk_overlap'])
        db = Database(config['database']['connection_string'])
    except Exception as e:
        logger.error(f"Initialization failed: {e}")
        st.error("Initialization error. Please check logs.")
        return

    st.title("Document Q&A Application")

    # File upload
    uploaded_files = st.file_uploader("Upload Documents", 
                                     type=['pdf', 'docx', 'txt'], 
                                     accept_multiple_files=True)
    
    if uploaded_files:
        st.write("Processing files...")
        progress_bar = st.progress(0)
        for i, uploaded_file in enumerate(uploaded_files):
            try:
                # Save raw file
                os.makedirs('data/raw', exist_ok=True)
                file_path = os.path.join('data/raw', uploaded_file.name)
                with open(file_path, 'wb') as f:
                    f.write(uploaded_file.getbuffer())
                
                # Store metadata in SQLite
                db.add_document(uploaded_file.name, file_path)
                
                # Parse document
                text = parser.parse(file_path)
                
                # Split text
                chunks = splitter.split_text(text, uploaded_file.name)
                
                # Generate embeddings
                embeddings = embedder.generate_embeddings([chunk['text'] for chunk in chunks])
                
                # Store in vector DB
                vector_db.add(chunks, embeddings, uploaded_file.name)
                
                logger.info(f"Processed file: {uploaded_file.name}")
            except Exception as e:
                logger.error(f"Error processing {uploaded_file.name}: {e}")
                st.error(f"Failed to process {uploaded_file.name}")
            progress_bar.progress((i + 1) / len(uploaded_files))
        
        st.success("All files processed!")

    # Query input
    query = st.text_input("Ask a question about your documents:")
    if query:
        try:
            # Embed query
            query_embedding = embedder.generate_embeddings([query])[0]
            
            # Search vector DB
            results = vector_db.search(query_embedding, k=5)
            
            # Log retrieved chunks for debugging
            logger.debug(f"Query: {query}")
            for res in results:
                logger.debug(f"Chunk from {res['file_name']}: {res['text'][:100]}... (Distance: {res['distance']})")
            
            # Prepare prompt for Mistral
            context = "\n\n".join([f"Document: {res['file_name']}\n{res['text']}" for res in results])
            prompt = (
                f"You are an expert assistant. Based on the following document excerpts, provide a detailed, accurate, and well-explained answer to the question. "
                f"You must give the best possible answer from the provided context"
                f"Use only the information provided in the context, and if the context is insufficient, say so clearly. Structure your answer with clear explanations and examples where relevant.\n\n"
                f"Context:\n{context}\n\n"
                f"Question: {query}\n\n"
                f"Answer:"
            )
            
            # Query Mistral
            answer = mistral.query(prompt)
            
            # Display answer and sources
            st.write("**Answer:**")
            st.write(answer)
            st.write("**Sources:**")
            for res in results:
                st.write(f"- {res['file_name']} (Chunk {res['chunk_id']}, Distance: {res['distance']:.3f})")
            
            logger.info(f"Answered query: {query}")
        except Exception as e:
            logger.error(f"Error answering query: {e}")
            st.error("Failed to process query. Please check logs.")

    # Display uploaded files
    st.write("**Uploaded Files:**")
    documents = db.get_all_documents()
    if documents:
        for doc in documents:
            st.write(f"- {doc.file_name} (Uploaded: {doc.upload_date})")
    else:
        st.write("No files uploaded yet.")

if __name__ == "__main__":
    main()
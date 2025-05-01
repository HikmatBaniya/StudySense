Document Q&A Application
This is a Streamlit-based application that allows users to upload documents (PDF, DOCX, TXT), process them using a local Mistral model, and ask questions about the content. The app stores document metadata in SQLite and embeddings in ChromaDB for efficient retrieval.
Setup

Create a virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install dependencies:
pip install -r requirements.txt


Ensure Mistral is running:

Run Mistral on http://localhost:8000/v1/completions.
Test with:curl -X POST http://localhost:8000/v1/completions -H "Content-Type: application/json" -d '{"prompt": "Test"}'




Create directories:
mkdir -p data/raw data/processed logs


Run the app:
streamlit run app.py



Usage

Upload documents via the web interface.
Ask questions about the documents.
View answers and source documents.

Project Structure

app.py: Main Streamlit app.
configs/config.yaml: Configuration settings.
services/: Document parsing, database, and vector DB handling.
models/: Mistral and embedding models.
utils/: Text chunking utilities.
data/: Raw and processed files.
logs/: Application logs.

Notes

Ensure SQLite database (data/documents.db) is writable.
ChromaDB stores embeddings in data/processed/vector_store.
Logs are saved to logs/app.log.


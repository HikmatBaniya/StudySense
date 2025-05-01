import chromadb
import numpy as np
import logging

logger = logging.getLogger(__name__)

class VectorDB:
    def __init__(self, config):
        try:
            self.client = chromadb.PersistentClient(path=config['path'])
            self.collection = self.client.get_or_create_collection("documents")
            logger.info("VectorDB initialized")
        except Exception as e:
            logger.error(f"VectorDB initialization failed: {e}")
            raise

    def add(self, chunks, embeddings, file_name):
        try:
            ids = [f"{file_name}_{chunk['chunk_id']}" for chunk in chunks]
            metadatas = [{"file_name": file_name, "chunk_id": chunk['chunk_id']} for chunk in chunks]
            texts = [chunk['text'] for chunk in chunks]
            self.collection.add(
                ids=ids,
                embeddings=embeddings.tolist(),
                metadatas=metadatas,
                documents=texts
            )
            logger.info(f"Added {len(chunks)} chunks to VectorDB for {file_name}")
        except Exception as e:
            logger.error(f"Error adding to VectorDB: {e}")
            raise

    def search(self, query_embedding, k=5):
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=k
            )
            # Filter results with similarity score (distance) threshold
            filtered_results = [
                {
                    "text": doc,
                    "file_name": meta["file_name"],
                    "chunk_id": meta["chunk_id"],
                    "distance": dist
                }
                for doc, meta, dist in zip(
                    results["documents"][0],
                    results["metadatas"][0],
                    results["distances"][0]
                )
                if dist < 0.8  # Adjust threshold as needed
            ]
            logger.debug(f"Retrieved {len(filtered_results)} chunks: {[r['file_name'] for r in filtered_results]}")
            return filtered_results
        except Exception as e:
            logger.error(f"Error searching VectorDB: {e}")
            raise
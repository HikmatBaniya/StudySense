from sentence_transformers import SentenceTransformer
import logging

logger = logging.getLogger(__name__)

class Embedder:
    def __init__(self, config):
        try:
            self.model = SentenceTransformer(config['name'])
            logger.info("Embedder initialized")
        except Exception as e:
            logger.error(f"Embedder initialization failed: {e}")
            raise

    def generate_embeddings(self, texts):
        try:
            embeddings = self.model.encode(texts, convert_to_numpy=True)
            return embeddings
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise
import logging

logger = logging.getLogger(__name__)

class TextSplitter:
    def __init__(self, chunk_size, chunk_overlap):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_text(self, text, file_name):
        try:
            # Simple character-based splitting (improve with token-based if needed)
            chunks = []
            start = 0
            chunk_id = 0
            while start < len(text):
                end = min(start + self.chunk_size, len(text))
                chunk_text = text[start:end]
                chunks.append({
                    "text": chunk_text,
                    "file_name": file_name,
                    "chunk_id": chunk_id
                })
                chunk_id += 1
                start += self.chunk_size - self.chunk_overlap
            logger.info(f"Split text into {len(chunks)} chunks for {file_name}")
            return chunks
        except Exception as e:
            logger.error(f"Error splitting text: {e}")
            raise
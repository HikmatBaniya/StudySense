import PyPDF2
import docx
import os
import logging

logger = logging.getLogger(__name__)

class DocumentParser:
    def parse(self, file_path):
        """Parse PDF, DOCX, or TXT file and return text."""
        try:
            ext = os.path.splitext(file_path)[1].lower()
            if ext == '.pdf':
                return self._parse_pdf(file_path)
            elif ext == '.docx':
                return self._parse_docx(file_path)
            elif ext == '.txt':
                return self._parse_txt(file_path)
            else:
                raise ValueError(f"Unsupported file extension: {ext}")
        except Exception as e:
            logger.error(f"Error parsing {file_path}: {e}")
            raise

    def _parse_pdf(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() or ""
                return text
        except Exception as e:
            logger.error(f"Error parsing PDF {file_path}: {e}")
            raise

    def _parse_docx(self, file_path):
        try:
            doc = docx.Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs if para.text])
            return text
        except Exception as e:
            logger.error(f"Error parsing DOCX {file_path}: {e}")
            raise

    def _parse_txt(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            logger.error(f"Error parsing TXT {file_path}: {e}")
            raise
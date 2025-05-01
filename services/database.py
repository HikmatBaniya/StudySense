from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

Base = declarative_base()

class Document(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True)
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    upload_date = Column(DateTime, default=datetime.utcnow)

class Database:
    def __init__(self, connection_string):
        try:
            self.engine = create_engine(connection_string)
            Base.metadata.create_all(self.engine)
            self.Session = sessionmaker(bind=self.engine)
            logger.info("Database initialized")
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise

    def add_document(self, file_name, file_path):
        try:
            session = self.Session()
            doc = Document(file_name=file_name, file_path=file_path)
            session.add(doc)
            session.commit()
            logger.info(f"Added document to database: {file_name}")
            return doc.id
        except Exception as e:
            session.rollback()
            logger.error(f"Error adding document {file_name}: {e}")
            raise
        finally:
            session.close()

    def get_all_documents(self):
        try:
            session = self.Session()
            documents = session.query(Document).all()
            return documents
        except Exception as e:
            logger.error(f"Error retrieving documents: {e}")
            raise
        finally:
            session.close()
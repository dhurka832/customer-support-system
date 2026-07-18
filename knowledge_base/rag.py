from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import logging
import shutil
from django.conf import settings

logger = logging.getLogger(__name__)

load_dotenv()

llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0
    )

_embedding = None

def get_embedding():
    global _embedding
    if _embedding is None:
        _embedding = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001"
        )
    return _embedding

def get_vectorstore_path():
    try:
        base_dir = settings.BASE_DIR
    except Exception:
        from pathlib import Path
        base_dir = Path(__file__).resolve().parent.parent
    return os.path.join(base_dir, "knowledge_base", "vectorstore")

def load_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    return documents

def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    return splitter.split_documents(documents)

def create_vector_store(chunks):
    vectorstore_path = get_vectorstore_path()
    if os.path.exists(vectorstore_path) and os.path.exists(os.path.join(vectorstore_path, "index.faiss")):
        try:
            db = FAISS.load_local(
                vectorstore_path,
                get_embedding(),
                allow_dangerous_deserialization=True
            )
            db.add_documents(chunks)
        except Exception as e:
            logger.error(f"Error loading existing vectorstore: {e}. Rebuilding vectorstore instead.")
            # If load fails due to dimension mismatch, rebuild from scratch including new chunks
            db = FAISS.from_documents(chunks, get_embedding())
        db.save_local(vectorstore_path)
    else:
        db = FAISS.from_documents(
            chunks,
            get_embedding()
        )
        db.save_local(vectorstore_path)
    return db

def load_vector_store():
    vectorstore_path = get_vectorstore_path()
    if not os.path.exists(vectorstore_path) or not os.path.exists(os.path.join(vectorstore_path, "index.faiss")):
        logger.warning(f"Vectorstore not found at: {vectorstore_path}")
        return None
    try:
        db = FAISS.load_local(
            vectorstore_path,
            get_embedding(),
            allow_dangerous_deserialization=True
        )
        return db
    except Exception as e:
        logger.error(f"Failed to load FAISS vectorstore: {e}. Attempting auto-rebuild from documents.")
        try:
            return rebuild_vector_store_from_all_docs()
        except Exception as rebuild_err:
            logger.error(f"Auto-rebuild of vectorstore failed: {rebuild_err}")
            return None

def rebuild_vector_store_from_all_docs():
    from .models import Document
    vectorstore_path = get_vectorstore_path()
    if os.path.exists(vectorstore_path):
        try:
            shutil.rmtree(vectorstore_path)
        except Exception as e:
            logger.warning(f"Could not remove old vectorstore directory: {e}")
            
    all_docs = Document.objects.all()
    all_chunks = []
    for doc in all_docs:
        if os.path.exists(doc.file.path):
            try:
                docs = load_pdf(doc.file.path)
                chunks = split_documents(docs)
                all_chunks.extend(chunks)
            except Exception as e:
                logger.error(f"Failed to load/split PDF {doc.file.path}: {e}")
        else:
            logger.warning(f"Document file does not exist on disk: {doc.file.path}")
                
    if all_chunks:
        try:
            db = FAISS.from_documents(all_chunks, get_embedding())
            db.save_local(vectorstore_path)
            logger.info("Successfully rebuilt vectorstore from all documents.")
            return db
        except Exception as e:
            logger.error(f"Failed to create FAISS from documents: {e}")
            raise e
    logger.warning("No document chunks to index.")
    return None


def search_documents(question):
    db = load_vector_store()   
    if db is None:
        return []
    try:
        docs = db.similarity_search(question, k=3)
        return docs
    except Exception as e:
        logger.error(f"Error during similarity search: {e}")
        return []

def generate_answer(question):

    docs = search_documents(question)
    if not docs:
        lower_q = question.lower().strip().rstrip('?!.')
        if lower_q in ['hi', 'hello', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening']:
            return "Hello! How can I help you today? (Note: The knowledge base is currently empty, so I can only answer general greetings.)"
        return "I'm sorry, I cannot answer this question because no documents have been uploaded to my knowledge base yet. Please upload documents via the admin panel."

    context = "\n\n".join(
        doc.page_content for doc in docs
    )

    prompt = f"""
    You are an AI Customer Support Assistant.

    Answer only from the provided context.
    Give a short answer in 1-2 sentences.

    Context:
    {context}

    Question:
    {question}
    """

    response = llm.invoke(prompt)

    return response.content


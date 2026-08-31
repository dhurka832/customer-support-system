import os
from dotenv import load_dotenv
from django.conf import settings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

def get_embedding():
    return GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

def get_vectorstore_path():
    base_dir = getattr(settings, 'BASE_DIR', os.path.dirname(os.path.dirname(__file__)))
    return os.path.join(base_dir, "knowledge_base", "vectorstore")

def load_and_split_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    return splitter.split_documents(documents)

def create_vector_store(chunks):
    vectorstore_path = get_vectorstore_path()
    index_file = os.path.join(vectorstore_path, "index.faiss")

    if os.path.exists(vectorstore_path) and os.path.exists(index_file):
        try:
            db = FAISS.load_local(vectorstore_path, get_embedding(), allow_dangerous_deserialization=True)
            db.add_documents(chunks)
        except Exception:
            db = FAISS.from_documents(chunks, get_embedding())
    else:
        db = FAISS.from_documents(chunks, get_embedding())

    db.save_local(vectorstore_path)
    return db

def load_vector_store():
    vectorstore_path = get_vectorstore_path()
    index_file = os.path.join(vectorstore_path, "index.faiss")

    if not os.path.exists(vectorstore_path) or not os.path.exists(index_file):
        return None

    try:
        return FAISS.load_local(vectorstore_path, get_embedding(), allow_dangerous_deserialization=True)
    except Exception:
        return rebuild_vector_store_from_all_docs()

def rebuild_vector_store_from_all_docs():
    from .models import Document

    vectorstore_path = get_vectorstore_path()
    if os.path.exists(vectorstore_path):
        for f in os.listdir(vectorstore_path):
            file_path = os.path.join(vectorstore_path, f)
            if os.path.isfile(file_path):
                try:
                    os.remove(file_path)
                except Exception:
                    pass

    all_docs = Document.objects.all()
    all_chunks = []
    for doc in all_docs:
        if doc.file and os.path.exists(doc.file.path):
            try:
                chunks = load_and_split_pdf(doc.file.path)
                all_chunks.extend(chunks)
            except Exception:
                pass

    if all_chunks:
        db = FAISS.from_documents(all_chunks, get_embedding())
        db.save_local(vectorstore_path)
        return db

    return None

def search_documents(question):
    db = load_vector_store()
    if db is None:
        return []
    try:
        return db.similarity_search(question, k=3)
    except Exception:
        return []

def generate_answer(question):
    docs = search_documents(question)

    if not docs:
        lower_q = question.lower().strip().rstrip('?!.')
        if lower_q in ['hi', 'hello', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening']:
            return "Hello! How can I help you today? (Note: Knowledge base is currently empty.)"
        return "I'm sorry, I cannot answer this question because no documents have been uploaded to the knowledge base yet."

    context = "\n\n".join(doc.page_content for doc in docs)

    prompt = f"""
You are an AI Customer Support Assistant.
Answer only using the provided context in 1-2 concise sentences.

Context:
{context}

Question:
{question}
"""

    response = llm.invoke(prompt)
    return response.content

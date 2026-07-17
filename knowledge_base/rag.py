from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0
    )

_embedding = None

def get_embedding():
    global _embedding
    if _embedding is None:
        from langchain_huggingface import HuggingFaceEmbeddings
        _embedding = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
    return _embedding


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
    import os
    vectorstore_path = "knowledge_base/vectorstore"
    if os.path.exists(vectorstore_path) and os.path.exists(os.path.join(vectorstore_path, "index.faiss")):
        db = FAISS.load_local(
            vectorstore_path,
            get_embedding(),
            allow_dangerous_deserialization=True
        )
        db.add_documents(chunks)
    else:
        db = FAISS.from_documents(
            chunks,
            get_embedding()
        )

    db.save_local(vectorstore_path)
    return db

def load_vector_store():
    import os
    vectorstore_path = "knowledge_base/vectorstore"
    if not os.path.exists(vectorstore_path) or not os.path.exists(os.path.join(vectorstore_path, "index.faiss")):
        return None
    db = FAISS.load_local(
        vectorstore_path,
        get_embedding(),
        allow_dangerous_deserialization=True
    )
    return db

def rebuild_vector_store_from_all_docs():
    from .models import Document
    import os
    import shutil
    
    vectorstore_path = "knowledge_base/vectorstore"
    if os.path.exists(vectorstore_path):
        try:
            shutil.rmtree(vectorstore_path)
        except Exception:
            pass
            
    all_docs = Document.objects.all()
    all_chunks = []
    for doc in all_docs:
        if os.path.exists(doc.file.path):
            try:
                docs = load_pdf(doc.file.path)
                chunks = split_documents(docs)
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
    docs = db.similarity_search(question, k=3)
    return docs

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


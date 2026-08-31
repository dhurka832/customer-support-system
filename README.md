# SupportSphere — AI-Powered Customer Support System

SupportSphere is a full-stack **Customer Support Platform** built with **Django 5.2**. It combines a Retrieval-Augmented Generation (RAG) AI chatbot (Llama 3 + FAISS), smart ticket management, a knowledge base document indexing system, and an administrative dashboard — backed by **PostgreSQL**.

---

## Key Features

### 1. AI Chatbot (`chatbot`)
- **Real-time AI Support**: Customers ask questions and receive instant answers grounded directly in internal knowledge base documents.
- **RAG Architecture**: Uses FAISS vector storage + Google AI Embeddings (`gemini-embedding-001`) + Llama 3 (via Groq API) to retrieve relevant context before generating answers.
- **Streamlined JavaScript**: Clean, lightweight client-side logic for real-time AJAX message processing and session loading.
- **Access Control**: Dedicated to customer accounts (admins focus exclusively on support operations and knowledge management).

### 2. Ticket Management (`support`)
- **Customer Ticket Portal**: Submit support tickets with priority levels (Low, Medium, High) and detailed descriptions.
- **Interactive Replies**: Staff and customers communicate via threaded replies.
- **Inline Status Updates**: Staff dynamically update ticket statuses (Open → In Progress → Closed) via AJAX.

### 3. Knowledge Base (`knowledge_base`)
- **Document Upload**: Staff upload policy handbooks or guides (PDF format).
- **Automatic Vector Indexing**: Documents are parsed (`pypdf`) and indexed into local FAISS vector storage.
- **Management Command**: `python manage.py rebuild_vectorstore` command to re-index documents on demand.

### 4. Admin Dashboard (`accounts`)
- **System Metrics**: Total registered users, total conversations, total messages, active users today, and per-user averages via Django ORM aggregations.
- **Customer Directory**: Search, browse, and inspect customer profiles with live conversation counts.
- **Chat Logs Audit**: Comprehensive log search and date filtering for customer chat sessions.
- **Global Search**: Unified search across users, conversations, chat messages, and support tickets.

### 5. Auth & Simple Login Interface
- **Split-Panel Login & Register**: Clean layout with branding panel and secure login form.
- **Clear Demo Credentials**: Simple plain text demo credentials display (`Dhurka` / `Dhurka@345`).

---

## Tech Stack & Architecture

| Layer | Technology |
|---|---|
| **Backend** | Django 5.2 (Python 3.10+) |
| **Database** | PostgreSQL |
| **AI / RAG** | LangChain + FAISS Vector Store + Llama 3 via Groq API |
| **Embeddings** | Google AI Embeddings (`models/gemini-embedding-001`) |
| **Frontend** | HTML5, Vanilla CSS3, Clean JavaScript |
| **CSS Framework** | Bootstrap 5 |
| **Static Serving** | WhiteNoise |

---

## Screenshots

<p align="center">
  <img src="screenshots/admin-dashboard.jpg" alt="Admin Dashboard View" width="400"/>
  <img src="screenshots/admin-tickets.jpg" alt="Admin Tickets View" width="400"/>
  <img src="screenshots/conversation-log.jpg" alt="Conversation Log View" width="400"/>
  <img src="screenshots/create_ticket.jpg" alt="Create Ticket View" width="400"/>
  <img src="screenshots/customer-directory.jpg" alt="Customer Directory View" width="400"/>
  <img src="screenshots/rag_chatbot.jpg" alt="RAG Chatbot View" width="400"/>
  <img src="screenshots/user_profile.jpg" alt="User Profile View" width="400"/>
  <img src="screenshots/user_tickets.jpg" alt="User Tickets View" width="400"/>
  <img src="screenshots/knowledge_base.jpg" alt="Knowledge Base View" width="400"/>
  <img src="screenshots/login.jpg" alt="Login View" width="400"/>
  <img src="screenshots/register.jpg" alt="Register View" width="400"/>
</p>

---

## Project Structure

```
customer_support_system/
│
├── accounts/                   
├── chatbot/                   
│   ├── models.py                
│   └── views.py                 
├── customer_support_system/   
├── knowledge_base/             
│   ├── rag.py                   
│   └── vectorstore/            
├── support/                    
│
├── static/
│   ├── css/                    
│   └── js/
│       ├── chatbot.js          
│       ├── tickets.js          
│       └── sidebar.js         
│
├── templates/                  
├── manage.py
└── requirements.txt
```

---

## Quick Setup

1. **Clone & Virtual Environment**:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   source venv/bin/activate # Linux/macOS
   pip install -r requirements.txt
   ```

2. **Database & Environment Setup**:
   Create a `.env` file in the root directory:
   ```env
   SECRET_KEY=your_secret_key
   GROQ_API_KEY=your_groq_api_key
   GOOGLE_API_KEY=your_google_api_key
   DATABASE_URL=postgres://USER:PASSWORD@localhost:5432/customer_support
   DEBUG=True
   ```

3. **Migrations & Vectorstore**:
   ```bash
   python manage.py migrate
   python manage.py rebuild_vectorstore
   python manage.py createsuperuser
   python manage.py runserver
   ```

---

## Key Dependencies

| Package | Purpose |
|---|---|
| `django==5.2` | Core Web Framework |
| `psycopg2-binary` | PostgreSQL Database Adapter |
| `dj-database-url` | Database URL parser |
| `langchain` + `langchain-groq` | RAG Pipeline & Llama 3 LLM |
| `faiss-cpu` | Vector Similarity Search |
| `langchain-google-genai` | Google AI Embeddings |
| `pypdf` | PDF Text Extraction |
| `whitenoise` | Production Static File Serving |

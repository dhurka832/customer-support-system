# SupportSphere — AI Customer Support & Operations Platform

An enterprise-grade, full-stack **Customer Support & Operations Platform** built with **Django 5.2**, **PostgreSQL**, and **Retrieval-Augmented Generation (RAG)**. Features intelligent automated knowledge retrieval via Llama 3 & FAISS, interactive support ticketing, and real-time operations analytics powered by a pure **HTML5/CSS3/Vanilla JS** design system.

---

## ⚡ Core Features

- **RAG-Powered AI Support**: Sub-second inquiry responses grounded in internal PDF documentation using **FAISS Vector Store**, Google AI Embeddings (`gemini-embedding-001`), and **Llama 3** (via Groq API).
- **Interactive Ticket Management**: Customer ticket submission with priority tagging (Low, Medium, High), status tracking (Open, In Progress, Closed), and real-time staff response threading.
- **Knowledge Base Vector Engine**: PDF upload pipeline that parses documents via `pypdf`, generates embeddings, and indexes them into vector storage with CLI rebuild commands (`manage.py rebuild_vectorstore`).
- **Analytics & Operations Dashboard**: Bento-grid system metrics (active users, resolution rates, dialogue density), customer directory management, and global search across records.
- **Pure Vanilla UI Architecture**: Bespoke card-based design system built without third-party CSS frameworks (zero Bootstrap dependency) for performance and responsiveness.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Django 5.2, Python 3.10+ |
| **Database** | PostgreSQL / SQLite3 |
| **AI / RAG Pipeline** | LangChain, FAISS Vector Store, Llama 3 (Groq API) |
| **Embeddings** | Google AI Embeddings (`models/gemini-embedding-001`) |
| **Frontend** | Semantic HTML5, Custom Modern CSS3 (Grid/Flexbox), Vanilla JS |
| **Static Serving** | WhiteNoise |

---

## Screenshots 

<img src="screenshots/admin-dashboard.jpg" width="300" height="200">
<img src="screenshots/admin-support-tickets.jpg" width="300" height="200">
<img src="screenshots/conversation-log.jpg" width="300" height="200">
<img src="screenshots/customer-directory.jpg" width="300" height="200">
<img src="screenshots/customer-support-tickets.jpg" width="300" height="200">
<img src="screenshots/create-ticket.jpg" width="300" height="200">
<img src="screenshots/rag-chatbot.jpg" width="300" height="200">
<img src="screenshots/user-profile.jpg" width="300" height="200">
<img src="screenshots/knowledge-base.jpg" width="300" height="200">
<img src="screenshots/knowledge_base_documents.jpg" width="300" height="200">
<img src="screenshots/register.jpg" width="300" height="200">
<img src="screenshots/login.jpg" width="300" height="200">

---

## 🚀 Quick Setup

```bash
# 1. Clone repository & create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements.txt

# 2. Configure Environment Variables (.env)
SECRET_KEY=your_django_secret_key
GROQ_API_KEY=your_groq_api_key
GOOGLE_API_KEY=your_google_api_key
DATABASE_URL=postgres://user:password@localhost:5432/support_db
DEBUG=True

# 3. Initialize Database & Vector Store
python manage.py migrate
python manage.py rebuild_vectorstore
python manage.py runserver
```

---

## 📂 Project Structure

```
├── accounts/               # User auth, admin analytics dashboard, profile management
├── chatbot/                # RAG AI assistant, conversation sessions, AJAX API
├── knowledge_base/         # PDF upload pipeline, LangChain RAG logic & FAISS store
├── support/                # Ticket lifecycle, staff threaded replies & status API
├── static/                 # Pure CSS design system & Vanilla JS interactive modules
├── templates/              # Semantic templates & modern card-based UI
└── manage.py
```

# SupportSphere — AI-Powered Customer Support System

SupportSphere is a premium, full-stack **Customer Support Platform** built on **Django 5.2**. It combines a RAG-powered AI chatbot (Llama 3 + FAISS), smart ticket management, a knowledge base document system, and a rich administrative dashboard — all backed by a **dual-database architecture**: SQLite for user accounts and MongoDB for chat logs.

---

## 🚀 Key Features

### 1. 🤖 AI Chatbot (`chatbot`)
- **Real-time AI Chat**: Customers ask questions and receive instant replies grounded in the company's internal knowledge base documents.
- **Smart Conversation Sidebar**: Full chat session history is stored in MongoDB and displayed in a collapsible sidebar. Users can switch between threads or start fresh sessions.
- **RAG-Powered Responses**: Integrates FAISS vector store + Llama 3 (via Groq API) to retrieve semantically relevant document chunks before generating answers.

### 2. 🎫 Ticket Management (`support`)
- **My Tickets Portal**: Customers can submit support tickets with priority levels (Low, Medium, High) and detailed descriptions.
- **Interactive Replies**: Staff post direct replies to ticket threads.
- **Inline AJAX Status Updates**: Admins update ticket statuses (Open → In Progress → Closed) without full page reloads.

### 3. 📚 Knowledge Base (`knowledge_base`)
- **Document Upload**: Staff upload company handbooks, policy PDFs, or guides.
- **Automatic Vector Indexing**: Uploaded documents are parsed and indexed into the FAISS vector database to enrich the AI chatbot's context.

### 4. 📊 Admin Dashboard (`accounts`)
- **Metrics Overview**: Total users, total conversations (MongoDB), total messages, active users today, and per-user averages.
- **30-Day Activity Charts**: Conversation and message timelines powered by Chart.js, aggregated via MongoDB pipelines.
- **Customer Directory**: Browse, search, and sort customers — annotated with live conversation & message counts from MongoDB.
- **Conversation Logs**: Browse, search, and filter all chat threads from MongoDB with date range filters.
- **CSV Export**: Download all message logs as a CSV file.
- **Global Search**: Search users (SQLite), conversations & messages (MongoDB), and tickets simultaneously.

### 5. 🔐 Premium Auth Pages
- **Split-panel Login & Register screens**: Dark animated branding panel on the left, clean white form on the right.
- **Demo Credentials Box**: Login page shows clickable demo pills (`Dhurka / Dhurka@345`) that auto-fill the form.
- Fully responsive — branding panel collapses on mobile.

---

## 🛠️ Architecture & Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Django 5.2 (Python 3.10+) |
| **Primary Database** | SQLite — User accounts, tickets, knowledge base |
| **Chat Log Database** | MongoDB — Conversations, messages, chat history |
| **AI / NLP** | FAISS Vector Store + Llama 3 via Groq API |
| **Embeddings** | HuggingFace `sentence-transformers` |
| **Frontend** | HTML5, Vanilla CSS3, Vanilla JavaScript |
| **CSS Framework** | Bootstrap 5 (grid, icons, base utilities) |
| **Visualization** | Chart.js (admin analytics graphs) |
| **Static Serving** | WhiteNoise (production-ready) |
| **MongoDB Driver** | PyMongo 4.x |

---

## 🗄️ Dual-Database Design

```
SQLite (db.sqlite3)                  MongoDB (customer_support)
─────────────────────────────────    ──────────────────────────────────
  auth_user (User accounts)            conversations  (chat sessions)
  support_ticket (Tickets)             messages       (Q&A exchanges)
  ticketreply                          chat_history   (legacy log)
  knowledge_base_document
  django_session / admin tables
```

The MongoDB integration layer lives in [`chatbot/mongodb.py`](chatbot/mongodb.py), exposing clean helper functions used by all views.

---

## 📁 Project Structure

```
customer_support_system/
│
├── accounts/                   # User auth, registration & admin dashboard views
├── chatbot/                    # AI chatbot views, MongoDB helpers, RAG integration
│   ├── mongodb.py              # ★ MongoDB connector & all CRUD helpers
│   └── views.py                # Chatbot views (uses mongodb.py exclusively)
├── customer_support_system/    # Django project settings, root URLs
├── knowledge_base/             # Document upload, text extraction, FAISS indexing
│   └── vectorstore/            # FAISS index files (index.faiss, index.pkl)
├── support/                    # Ticket management views & models
│
├── static/
│   ├── css/
│   │   ├── base.css            # Global portal styles & design tokens
│   │   ├── auth.css            # ★ Premium split-panel login/register design
│   │   ├── chatbot.css         # Chat sidebar & message bubble styling
│   │   └── dashboard.css       # Admin dashboard & sidebar styling
│   └── js/
│       ├── chatbot.js          # AJAX conversation loading & message sending
│       ├── dashboard-chart.js  # Chart.js analytics initializer
│       ├── tickets.js          # AJAX ticket status updates
│       ├── customers.js        # Customer directory modal
│       └── sidebar.js          # Admin sidebar toggle
│
├── templates/
│   ├── accounts/               # login.html, register.html, profile.html
│   ├── chatbot/                # chatbot.html, history.html
│   ├── dashboard/              # Admin panel templates
│   └── support/                # Ticket list, detail, create templates
│
├── media/                      # Uploaded documents
├── manage.py
├── db.sqlite3                  # SQLite database (users, tickets, etc.)
└── requirements.txt
```

---

## ⚙️ Setup & Installation

### 1. Prerequisites
- Python 3.10+
- **MongoDB** running locally on `mongodb://localhost:27017/` (or set `MONGODB_URI` in `.env`)
- Virtual Environment utility (`venv`)

### 2. Clone & Setup Environment
```bash
# Create virtual environment
python -m venv venv

# Activate — Windows:
.\venv\Scripts\activate
# Activate — Linux/macOS:
source venv/bin/activate

# Install all dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
MONGODB_URI=mongodb://localhost:27017/        # Optional: defaults to local
MONGODB_DB_NAME=customer_support             # Optional: defaults to this name
```

### 4. Run SQLite Migrations
Initialize the relational database schema (users, tickets, etc.):
```bash
python manage.py migrate
```

### 5. Create an Admin Superuser
Required to access the Admin Dashboard and Knowledge Base upload portal:
```bash
python manage.py createsuperuser
```

### 6. Start MongoDB
Make sure your local MongoDB instance is running:
```bash
# Windows (if installed as a service):
net start MongoDB

# Or start manually:
mongod --dbpath "C:\data\db"
```

### 7. Run the Development Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser.

> **Demo Login**: Username `Dhurka` / Password `Dhurka@345` *(shown as clickable pills on the login page)*

---

## 🧪 Verification & Static Files

After modifying any file in `static/`, recompile with:
```bash
python manage.py collectstatic --noinput
```

Run the Django system check:
```bash
python manage.py check
```
Expected: `System check identified no issues (0 silenced).`

---

## 📦 Key Dependencies

| Package | Purpose |
|---|---|
| `django==5.2` | Web framework |
| `pymongo` | MongoDB driver |
| `langchain` + `langchain-groq` | RAG chain & Groq LLM integration |
| `faiss-cpu` | Vector similarity search |
| `sentence-transformers` | Document embedding model |
| `pypdf` + `python-docx` | Document text extraction |
| `whitenoise` | Static file serving |
| `dj-database-url` | Database URL configuration helper |
| `gunicorn` | Production WSGI server |

# SupportSphere — AI-Powered Customer Support System

SupportSphere is a premium, full-stack **Customer Support Platform** built on **Django 5.2**. It combines a RAG-powered AI chatbot (Llama 3 + FAISS), smart ticket management, a knowledge base document system, and a rich administrative dashboard — all backed by a single **PostgreSQL** database.

---

## Key Features

### 1. AI Chatbot (`chatbot`)
- **Real-time AI Chat**: Customers ask questions and receive instant replies grounded in the company's internal knowledge base documents.
- **Smart Conversation Sidebar**: Full chat session history is stored in PostgreSQL and displayed in a collapsible sidebar. Users can switch between threads or start fresh sessions.
- **RAG-Powered Responses**: Integrates FAISS vector store + Llama 3 (via Groq API) to retrieve semantically relevant document chunks before generating answers.

### 2. Ticket Management (`support`)
- **My Tickets Portal**: Customers can submit support tickets with priority levels (Low, Medium, High) and detailed descriptions.
- **Interactive Replies**: Staff post direct replies to ticket threads.
- **Inline AJAX Status Updates**: Admins update ticket statuses (Open → In Progress → Closed) without full page reloads.

### 3. Knowledge Base (`knowledge_base`)
- **Document Upload**: Staff upload company handbooks, policy PDFs, or guides.
- **Automatic Vector Indexing**: Uploaded documents are parsed and indexed into the FAISS vector database to enrich the AI chatbot's context.

### 4. Admin Dashboard (`accounts`)
- **Metrics Overview**: Total users, total conversations, total messages, active users today, and per-user averages — all computed with Django ORM aggregations against PostgreSQL.
- **30-Day Activity Charts**: Conversation and message timelines powered by Chart.js, aggregated via Django's `TruncDate`/`Count` queryset annotations.
- **Customer Directory**: Browse, search, and sort customers — annotated with live conversation & message counts via ORM `Count` annotations.
- **Conversation Logs**: Browse, search, and filter all chat threads with date range filters.
- **CSV Export**: Download all message logs as a CSV file.
- **Global Search**: Search users, conversations & messages, and tickets simultaneously — all backed by PostgreSQL.

### 5. Premium Auth Pages
- **Split-panel Login & Register screens**: Dark animated branding panel on the left, clean white form on the right.
- **Demo Credentials Box**: Login page shows clickable demo pills (`Dhurka / Dhurka@345`) that auto-fill the form.
- Fully responsive — branding panel collapses on mobile.

---

##  Architecture & Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Django 5.2 (Python 3.10+) |
| **Database** | PostgreSQL — user accounts, tickets, knowledge base, conversations, messages, chat history |
| **AI / NLP** | FAISS Vector Store + Llama 3 via Groq API |
| **Embeddings** | Google AI Embeddings (`models/gemini-embedding-001`) |
| **Frontend** | HTML5, Vanilla CSS3, Vanilla JavaScript |
| **CSS Framework** | Bootstrap 5 (grid, icons, base utilities) |
| **Visualization** | Chart.js (admin analytics graphs) |
| **Static Serving** | WhiteNoise (production-ready) |
| **DB Driver** | psycopg2-binary |
| **DB URL Parsing** | dj-database-url |

---

#  Screenshots

<p align="center">
  <img src="screenshots/admin-dashboard.jpg" alt="Admin Dashboard View"  height="400" width="400"/>
  <img src="screenshots/ai_chat.jpg" alt="AI Chat View"  height="400" width="400"/> 
  <img src="screenshots/chat_logs.jpg" alt="Chat Logs View"  height="400" width="400"/>
  <img src="screenshots/customers.jpg" alt="Customers View"  height="400" width="400"/>
  <img src="screenshots/knowledge_base.jpg" alt="Knowledge Base View"  height="400" width="400"/>
  <img src="screenshots/tickets.jpg" alt="Tickets View"  height="400" width="400"/>
  <img src="screenshots/user_tickets.jpg" alt="User Tickets iew"  height="400" width="400"/>
  <img src="screenshots/user-profile.jpg" alt="User Profile View" width="400" height="400"/>
  <img src="screenshots/login.jpg" alt="Login View"  height="400" width="400" /> 

</p>

---

## Database Design


```
PostgreSQL (customer_support)
──────────────────────────────────────
  auth_user                  (User accounts)
  support_ticket              (Tickets)
  support_ticketreply         (Ticket replies)
  knowledge_base_document      (Uploaded docs)
  chatbot_conversation         (Chat sessions)
  chatbot_message              (Q&A exchanges within a conversation)
  chatbot_chathistory          (Flat legacy Q&A log)
  django_session / admin tables
```

---

## Project Structure

```
customer_support_system/
│
├── accounts/                   # User auth, registration & admin dashboard views
├── chatbot/                    # AI chatbot views, models, RAG integration
│   ├── models.py                # Conversation / Message / ChatHistory models
│   └── views.py                 # Chatbot views (uses the Django ORM exclusively)
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
└── requirements.txt
```

---

## Setup & Installation

### 1. Prerequisites
- Python 3.10+
- **PostgreSQL** running locally (or accessible via a connection string)
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

### 3. Create the PostgreSQL Database
```bash
createdb customer_support
# or, from the psql shell:
# CREATE DATABASE customer_support;
```

### 4. Configure Environment Variables
Create a `.env` file in the project root:
```env
SECRET_KEY=your_secret_key_here
GROQ_API_KEY=your_groq_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
DATABASE_URL=postgres://USER:PASSWORD@localhost:5432/customer_support
DEBUG=True
```
`DATABASE_URL` is parsed by `dj-database-url` in `settings.py`. If it's not set, the project falls back to a local `db.sqlite3` file — useful for a quick first run, but PostgreSQL is the intended database for this project. If using Google AI Embeddings, make sure to supply your `GOOGLE_API_KEY`.

### 5. Rebuild the Vector Store
Before running the chatbot for the first time or after updating documents, rebuild the FAISS vector database to generate embeddings using Google AI:
```bash
python manage.py rebuild_vectorstore
```

### 6. Run Migrations
Creates all tables — users, tickets, knowledge base documents, conversations, messages, chat history:
```bash
python manage.py migrate
```

### 7. Create an Admin Superuser
Required to access the Admin Dashboard and Knowledge Base upload portal:
```bash
python manage.py createsuperuser
```

### 8. Run the Development Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser.

> **Demo Login**: Username `Dhurka` / Password `Dhurka@345` *(shown as clickable pills on the login page)*

---

## Verification & Static Files

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

## Troubleshooting

### Server Error (500) with no details
By default `DEBUG=False` hides the real traceback. Set `DEBUG=True` in `.env`, restart the server, and reproduce the error to see the actual exception. Once fixed, set it back to `False` before deploying.

The most common causes right after switching to PostgreSQL:

1. **PostgreSQL isn't running or isn't reachable.**
   ```bash
   psql "postgres://USER:PASSWORD@localhost:5432/customer_support" -c "\dt"
   ```
   If this fails to connect, every page will 500.

2. **`psycopg2-binary` / `dj-database-url` aren't installed** (added when the project moved off MongoDB):
   ```bash
   pip install -r requirements.txt
   ```

3. **Migrations haven't been applied to the new database.**
   ```bash
   python manage.py migrate
   ```
   If `chatbot_conversation`, `chatbot_message`, or `chatbot_chathistory` don't exist yet, any chatbot or dashboard page will 500 with `relation "..." does not exist`.

4. **`DATABASE_URL` is missing or wrong** in `.env` — check the user, password, host, port, and database name.

If the traceback points somewhere else entirely, open an issue (or ask for help) with the full stack trace — the exact line tells you which of the above (if any) is the actual cause.

---

## Key Dependencies

| Package | Purpose |
|---|---|
| `django==5.2` | Web framework |
| `psycopg2-binary` | PostgreSQL driver |
| `dj-database-url` | Database URL configuration helper |
| `langchain` + `langchain-groq` | RAG chain & Groq LLM integration |
| `faiss-cpu` | Vector similarity search |
| `langchain-google-genai` | Google AI Embeddings integration |
| `pypdf` | Document text extraction |
| `whitenoise` | Static file serving |
| `gunicorn` | Production WSGI server |

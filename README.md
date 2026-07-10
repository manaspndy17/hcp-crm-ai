# AI-First CRM – HCP Log Interaction Module

An AI-first Customer Relationship Management module for pharmaceutical field representatives to log Healthcare Professional (HCP) interactions — either through a traditional structured form or a conversational AI chat interface powered by a LangGraph agent.

## Overview

Field reps can simply describe an interaction in natural language (e.g. *"Met Dr. Smith, discussed Product X efficacy, positive sentiment, shared brochure"*), and an AI agent extracts structured data, saves it to the database, and auto-fills the form — removing the need for manual data entry.

## Tech Stack

- **Frontend:** React + Redux Toolkit
- **Backend:** Python + FastAPI
- **AI Agent Framework:** LangGraph
- **LLM:** Groq — `llama-3.1-8b-instant`
  - Note: The task originally specified `gemma2-9b-it`, but this model was officially decommissioned by Groq. Migrated to `llama-3.1-8b-instant` per Groq's official deprecation recommendation (docs: console.groq.com/docs/deprecations).
- **Database:** MySQL
- **Font:** Google Inter

## LangGraph Agent & Tools

The LangGraph agent acts as the reasoning layer between the field rep's natural language input and the CRM's backend actions. It reads the user's message, decides which tool(s) are relevant, extracts the necessary parameters using the LLM, and executes real database operations — rather than just generating a text response.

### The 5 Tools

1. **`log_interaction`** — Extracts HCP name, interaction type, topics discussed, sentiment, and outcomes from a natural language message and saves a new interaction record to the database.

2. **`edit_interaction`** — Updates a specific field of an already-logged interaction (e.g. "change sentiment for interaction 3 to Neutral"), identified by interaction ID.

3. **`search_hcp_interactions`** — Retrieves the interaction history for a given HCP by name, useful for reps preparing for a follow-up visit.

4. **`schedule_followup`** — Attaches a follow-up action/next step to an existing logged interaction.

5. **`suggest_materials`** — Recommends relevant marketing materials or brochures to share based on the topic discussed during the interaction.

Each tool is a plain Python function with a descriptive docstring; the LLM reads these docstrings to decide which tool to call and with what arguments — this is the core mechanism of LangGraph's tool-calling pattern.

## Project Structure


hcp-crm-ai/
├── backend/
│   ├── main.py           # FastAPI app & routes (/chat, /interactions, /interactions/manual)
│   ├── agent.py           # LangGraph agent setup (LLM + tools binding)
│   ├── tools.py            # The 5 LangGraph tools
│   ├── models.py          # SQLAlchemy DB model (Interaction table)
│   ├── database.py       # DB connection/session setup
│   ├── create_tables.py    # One-time script to create DB tables
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx        # Main UI - structured form (left) + AI chat (right)
│   │   ├── store.js         # Redux slice for interaction form state
│   │   └── main.jsx        # Redux Provider setup
│   └── package.json
└── README.md


## How to Run

### Prerequisites
- Python 3.10+
- Node.js + npm
- MySQL running locally
- A free Groq API key (console.groq.com)

### Backend Setup

```bash
cd backend
python -m venv venv

# Activate venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

pip install -r requirements.txt
```

Create a `.env` file inside `backend/`:
```env
DATABASE_URL=mysql+pymysql://your_user:your_password@localhost:3306/hcp_crm
GROQ_API_KEY=your_groq_api_key_here
```

Create the database and tables:
```sql
CREATE DATABASE hcp_crm;
```
```bash
python create_tables.py
```

Run the backend server:
```bash
uvicorn main:app --reload
```
Backend runs at `http://localhost:8000` — interactive API docs available at `http://localhost:8000/docs`.

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```
Frontend runs at `http://localhost:5173`.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/interactions` | List all logged interactions |
| POST | `/interactions/manual` | Save a manually filled-out form |
| POST | `/chat` | Send a natural language message to the LangGraph AI agent |

## Known Limitations

- Groq's free tier has a rate limit (6000 tokens/minute), which may occasionally cause brief delays between rapid consecutive AI chat requests.
- Sentiment classification is inferred by the LLM based on tone; not a clinically validated sentiment model.
- Authentication/user management not implemented — out of scope for this assignment.

## What I Understood From This Task

This task demonstrates how an AI-first CRM shifts data entry from manual, structured forms to natural conversation — while still preserving the reliability of a structured backend. LangGraph's tool-calling pattern separates *reasoning* (deciding what to do, handled by the LLM) from *execution* (actually doing it, handled by deterministic Python functions and a real database) — which keeps the system reliable even though its interface feels conversational and flexible.
# PriorAuth

PriorAuth is a multi-agent AI prototype designed to assist
healthcare providers with insurance prior authorization workflows.

The system reads insurance guidelines, identifies authorization
requirements, retrieves supporting patient evidence, and generates
a structured prior authorization draft.

> Current implementation: Agent 1 — Guidelines Reader

---

## Current Status

| Component | Status |
|---|---|
| Guidelines Reader | ✅ Implemented |
| PDF extraction | ✅ Implemented |
| Groq LLM integration | ✅ Implemented |
| Structured output | ✅ Implemented |
| Streamlit UI | ⏳ Planned |
| Patient Chart Reviewer | ⏳ Planned |
| Vector Database | ⏳ Planned |
| Evidence Matcher | ⏳ Planned |
| Form Writer | ⏳ Planned |
| Validator | ⏳ Planned |
| Human Review | ⏳ Planned |

---

# Architecture

Current Agent 1 architecture:

```text
Insurance Guideline PDF
          |
          v
      Streamlit
          |
          v
   Guidelines Agent
          |
     +----+----+
     |         |
     v         v
PyMuPDF      Groq
     |         |
     +----+----+
          |
          v
       Pydantic
          |
          v
 Structured Guideline
          |
          v
      Streamlit

```

---

# File Structure

```text
priorauth/
│
├── app/
│   ├── agents/
│   │   └── guideline_agent.py
│   │
│   ├── models/
│   │   └── guideline.py
│   │
│   ├── services/
│   │   ├── groq_client.py
│   │   └── pdf_parser.py
│   │
│   └── ui/
│       └── streamlit_app.py
│
├── data/
│   └── guidelines/
│
├── tests/
│
├── docs/
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

# Installation & Setup

Follow these steps to set up and run the project locally on your machine.

### 1. Clone the Repository

Clone the project repository to your local system using Git:

```bash
git clone <repository-url>
cd <repository-folder-name>
```

### 2. Create and Activate a Virtual Environment
It is recommended to create a virtual environment to manage project dependencies independently.

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
Install all required packages listed in the requirements.txt file:

```bash
pip install -r requirements.txt
```

### 4. Running the Project

```bash
python main.py
```
Later we will use **Streamlit** to run the project.
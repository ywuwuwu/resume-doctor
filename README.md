# ResumeDoctor.ai

**ResumeDoctor.ai** is an AI-powered resume review and job matching web app that helps job seekers improve their resumes faster and discover better-fit roles. Users upload a resume (text or PDF), the system generates actionable improvement suggestions, and recommends relevant jobs using vector similarity search.

## Why it’s useful

* **End-to-end product**: Upload → parse → AI feedback → scoring → job recommendations
* **LLM integration**: Personalized rewrite suggestions and highlight extraction
* **Semantic matching**: Embedding + Elasticsearch kNN for job recommendation (beyond keyword search)
* **Production-minded deployment**: Reverse proxy + automated deployment via GitHub Actions

---

## Key Features

* **Resume upload**

  * Supports plain text resumes and PDF uploads
* **AI resume critique**

  * Calls a configurable LLM (“书生” model) to generate personalized suggestions
  * Outputs structured feedback (strengths, missing items, improvements)
* **Vector-based job recommendation**

  * Creates embeddings for resumes / job posts
  * Uses Elasticsearch vector similarity search to retrieve the most relevant roles
* **Automatic scoring & feedback**

  * Provides a resume quality score (completeness, highlights, potential)

---

## Tech Highlights (what I built)

* **Frontend + backend full-stack integration**

  * React SPA communicates with a Flask REST API
* **LLM-based analysis pipeline**

  * Prompted generation for resume critiques and optimization suggestions
* **Embedding + kNN retrieval**

  * Semantic job matching using vector representations + Elasticsearch indexing/search
* **Persistent storage**

  * Stores resume metadata and results in MySQL
* **CI/CD deployment**

  * Automated build/deploy pipeline with Nginx reverse proxy routing traffic to Flask + React build

---

## Repository Structure

```text
resume-doctor/
├── README.md                      # Project documentation
├── frontend/                      # React frontend
│   ├── public/
│   └── src/
│       └── App.js                 # Main UI
├── backend/                       # Flask backend service
│   └── app.py
├── init/                          # Initialization scripts
│   ├── init_mysql.sql             # MySQL schema
│   └── init_es.py                 # Elasticsearch initialization (index + mapping)
└── .github/workflows/             # CI/CD workflows
    └── deploy.yml
```

---

## Tech Stack

|              Layer | Technology                 | What it’s used for                    |
| -----------------: | -------------------------- | ------------------------------------- |
|           Frontend | React                      | Resume upload UI + results dashboard  |
|            Backend | Flask                      | REST API, business logic, model calls |
|           Database | MySQL                      | Resume records, analysis outputs      |
| Search / Retrieval | Elasticsearch              | Job index + vector similarity search  |
|                 AI | Embedding model + “书生” LLM | Embeddings + text critique generation |
|         Deployment | Nginx + GitHub Actions     | Reverse proxy + automated deployment  |

---

## Quick Start

### 1) Clone the repo

```bash
git clone https://github.com/ywuwuwu/resume-doctor.git
cd resume-doctor
```

### 2) Backend (Flask)

```bash
cd backend
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

### 3) Frontend (React)

```bash
cd frontend
npm install
npm start
```

---

## Configuration

This project depends on **an LLM endpoint**, **an embedding model**, **MySQL**, and **Elasticsearch**.

Create a `.env` (or set environment variables in your deployment platform) for:

* **LLM (书生)**


* **Embeddings**

* **MySQL**

* **Elasticsearch**

---

## Deployment Notes (Nginx + CI/CD)

* **Nginx** routes:

  * `/api/*` → Flask backend
  * `/` → React build output

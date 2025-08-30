📄 Final README.md

\# ⚡ Physics QnA System



A Question-Answering system for Class 10 Physics built with \*\*FastAPI\*\*, \*\*ChromaDB\*\*, and \*\*Sentence Transformers\*\*.  

This project allows students to ask questions about physics formulas and theories and get \*\*short, to-the-point answers\*\*.



---



\## 📌 Features

\- 🔹 Formula questions → returns concise equations (e.g., `v = s / t`)

\- 🔹 Theory questions → returns short explanations (1–2 sentences)

\- 🔹 Special cases handled directly:

&nbsp; - Newton’s Laws

&nbsp; - Ohm’s Law

&nbsp; - Archimedes’ Principle

&nbsp; - Law of Gravitation

&nbsp; - Boyle’s Law

&nbsp; - Charles’ Law

\- 🔹 Frontend built with simple \*\*HTML + CSS + JavaScript\*\*

\- 🔹 Backend built with \*\*Python (FastAPI)\*\*



---



\## 🛠️ Tech Stack

\- \*\*Backend:\*\* FastAPI

\- \*\*Vector DB:\*\* ChromaDB

\- \*\*Embeddings:\*\* Sentence Transformers (`all-MiniLM-L6-v2`)

\- \*\*Frontend:\*\* HTML, CSS, JavaScript



---



\## 🚀 How to Run



\### 1. Setup Environment

```bash

python -m venv venv

venv\\Scripts\\activate    # for Windows

pip install -r requirements.txt



2\. Prepare Data

\# Extract text from PDF

python scripts/extract\_text.py data/physics\_book.pdf data/physics\_book.txt



\# Create embeddings

python scripts/chunk\_and\_embed.py data/physics\_book.txt data/chunks.jsonl



\# Build vector database

python scripts/build\_db.py data/chunks.jsonl



3\. Run Backend

uvicorn app.main:app --reload --port 8000





API will be available at: 👉 http://127.0.0.1:8000/docs



4\. Run Frontend



Simply open frontend/index.html in your browser.



Green box = Formula answer



Blue box = Theory answer



📷 Demo (Example)





Question:

Explain Newton's Third Law



Answer:



Theory: Newton's Third Law: For every action, there is an equal and opposite reaction.



📂 Project Structure

physics-qa-project/

&nbsp;├─ app/            # FastAPI backend

&nbsp;├─ scripts/        # Data preparation scripts

&nbsp;├─ frontend/       # Simple HTML frontend

&nbsp;├─ data/           # PDF + text data

&nbsp;├─ requirements.txt

&nbsp;├─ README.md

&nbsp;└─ .gitignore



🙌 Credits



Built by Momina ✨



Uses FastAPI, ChromaDB, HuggingFace Sentence Transformers


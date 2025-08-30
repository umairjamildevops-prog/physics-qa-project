from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import chromadb
from sentence_transformers import SentenceTransformer
import re

app = FastAPI(title="Physics QnA")

# ✅ CORS Middleware (frontend ko backend se baat karne dega)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Allow all origins (frontend HTML)
    allow_credentials=True,
    allow_methods=["*"],   # Allow all methods (POST, GET, OPTIONS etc.)
    allow_headers=["*"],   # Allow all headers
)

# ✅ Chroma client
client = chromadb.PersistentClient(path=".chromadb")
collection = client.get_or_create_collection("physics10")

# ✅ Embedding model
embed_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

class Query(BaseModel):
    question: str
    top_k: int = 3

# ✅ Formula detection
def contains_formula_request(q: str) -> bool:
    ql = q.lower()
    for w in ["formula", "equation", "derive", "expression"]:
        if w in ql:
            return True
    if "=" in q:
        return True
    return False

# ✅ Extract formula
def extract_formula_from_text(text: str):
    for ln in text.split("\n"):
        ln = ln.strip()
        if "=" in ln and len(ln) < 100:
            return ln
    return None

@app.post("/ask")
def ask(q: Query):
    q_text = q.question.strip().lower()
    emb = embed_model.encode(q_text).tolist()

    # 🔹 Special Cases
    if "newton" in q_text and "first law" in q_text:
        return {"type": "theory", "answer": 
                "Newton's First Law: A body remains at rest, or in uniform motion in a straight line, unless acted upon by an external force."}
    if "newton" in q_text and "second law" in q_text:
        return {"type": "theory", "answer": 
                "Newton's Second Law: Force is equal to mass times acceleration (F = ma)."}
    if "newton" in q_text and "third law" in q_text:
        return {"type": "theory", "answer": 
                "Newton's Third Law: For every action, there is an equal and opposite reaction."}
    if "ohm" in q_text and "law" in q_text:
        return {"type": "theory", "answer": 
                "Ohm’s Law: The current through a conductor is directly proportional to the voltage across it, if temperature remains constant (V = IR)."}
    if "archimedes" in q_text and "principle" in q_text:
        return {"type": "theory", "answer": 
                "Archimedes’ Principle: A body immersed in a fluid experiences an upward force equal to the weight of the fluid displaced by it."}
    if "law of gravitation" in q_text or ("universal" in q_text and "gravitation" in q_text):
        return {"type": "theory", "answer": 
                "Law of Gravitation: Every two masses attract each other with a force directly proportional to the product of their masses and inversely proportional to the square of the distance between them (F = G m₁m₂ / r²)."}
    if "boyle" in q_text and "law" in q_text:
        return {"type": "theory", "answer": 
                "Boyle’s Law: The pressure of a gas is inversely proportional to its volume at constant temperature (P ∝ 1/V)."}
    if "charles" in q_text and "law" in q_text:
        return {"type": "theory", "answer": 
                "Charles’ Law: The volume of a gas is directly proportional to its absolute temperature at constant pressure (V ∝ T)."}

    # 🔹 General DB Search
    res = collection.query(
        query_embeddings=[emb], n_results=q.top_k, include=["metadatas", "distances"]
    )
    texts = [m["text"] for m in res["metadatas"][0]]

    if contains_formula_request(q.question):
        for t in texts:
            f = extract_formula_from_text(t)
            if f:
                return {"type": "formula", "answer": f}
        return {"type": "formula", "answer": texts[0].split("\n")[0]}

    best_text = texts[0]
    sentences = re.split(r'[.!?]', best_text)
    short_answer = sentences[0].strip()
    if len(sentences) > 1:
        short_answer += ". " + sentences[1].strip()
    return {"type": "theory", "answer": short_answer}
import os

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))  # Railway ka apna PORT use karega
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)


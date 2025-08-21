# localgpt.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from llama_cpp import Llama
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

# -------- Setup --------

# Load LLM
llm = Llama(
    model_path="models/mistral/mistral-7b-instruct-v0.1.Q4_K_M.gguf",
    n_ctx=512,
    n_threads=4,
    use_mlock=True
)

# Chroma with persistence
chroma_client = chromadb.PersistentClient(path="./chroma_db")

embedding_fn = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

collection = chroma_client.get_or_create_collection(
    name="delhi-assistant",
    embedding_function=embedding_fn
)

# Populate DB if empty
if collection.count() == 0:
    print("📥 Adding knowledge data...")
    with open("data/knowledge.txt", "r", encoding="utf-8") as f:
        content = f.read().strip().split("\n\n")
    for i, block in enumerate(content):
        lines = block.split("\n")
        if len(lines) >= 2:
            question = lines[0].replace("Q:", "").strip()
            answer = lines[1].replace("A:", "").strip()
            doc = f"Question: {question}\nAnswer: {answer}"
            collection.add(
                documents=[doc],
                metadatas=[{"source": "knowledge.txt"}],
                ids=[f"qa-{i}"]
            )
    print("✅ Knowledge base embedded into Chroma.")
else:
    print(f"✅ Knowledge base already loaded ({collection.count()} docs).")


# -------- API Setup --------
app = FastAPI()

# Allow frontend (React) to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: restrict to ["http://localhost:5173"] in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    message: str


@app.post("/chat")
async def chat(query: Query):
    try:
        # Search Chroma
        results = collection.query(query_texts=[query.message], n_results=3)
        docs = results["documents"][0] if results and results["documents"] else []
        context = "\n".join(docs) if docs else "No relevant info found."

        # If no knowledge found
        if context.strip() == "No relevant info found.":
            return {"reply": "Not found in database"}

        # Prompt for LLM
        prompt = f"""You are a Delhi Metro & City assistant. 
Use only the knowledge provided below to answer the query.
If the answer is not in the knowledge, reply strictly with: "Not found in database".

Knowledge:
{context}

User: {query.message}
Assistant:"""

        # Generate answer
        response = llm.create_completion(
            prompt=prompt,
            max_tokens=300,
            stop=["User:", "Assistant:"]
        )
        answer = response["choices"][0]["text"].strip()

        return {"reply": answer or "Not found in database"}

    except Exception as e:
        print("⚠️ Error in /chat:", e)
        return {"reply": "⚠️ Internal error, please try again."}


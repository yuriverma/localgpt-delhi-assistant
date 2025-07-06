# localgpt.py

import os
from llama_cpp import Llama
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

# Step 1: Load your local LLM (Mistral GGUF)
llm = Llama(
    model_path="models/mistral/mistral-7b-instruct-v0.1.Q4_K_M.gguf",
    n_ctx=512,        # keep this small for 8GB RAM
    n_threads=4,
    use_mlock=True
)

# Step 2: Setup Chroma + Embedder
print("🔄 Setting up vector store...")

embedding_fn = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(
    name="delhi-food",
    embedding_function=embedding_fn
)

# Step 3: Load & embed food data from food.txt
if collection.count() == 0:
    with open("data/food.txt", "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    for i, line in enumerate(lines):
        collection.add(
            documents=[line],
            metadatas=[{"source": "food.txt"}],
            ids=[f"food-{i}"]
        )
    print("✅ Food data embedded into Chroma.")
else:
    print("✅ Chroma already has food data.")

# Step 4: Ask user query
while True:
    query = input("\n🗣️  Ask something about food in Delhi (type 'exit' to quit): ")
    if query.lower() == "exit":
        break

    # Step 5: Search Chroma
    results = collection.query(query_texts=[query], n_results=3)
    docs = results["documents"][0] if results["documents"] else ["No data found."]

    # Step 6: Build Prompt
    context = "\n".join(docs)
    prompt = f"""You are a helpful Delhi city assistant. Use the food info below to answer the user question.

Food Data:
{context}

User: {query}
Assistant:"""

    # Step 7: Local LLM Response
    response = llm(prompt, max_tokens=200)
    print("🤖 Assistant:", response["choices"][0]["text"].strip())


# embedder.py

import os
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

# Load embedding model (offline, small)
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# Use in-memory Chroma client (safe for now)
chroma_client = chromadb.Client()

embedding_fn = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

def embed_food_data():
    collection = chroma_client.get_or_create_collection(
        name="delhi-food",
        embedding_function=embedding_fn
    )

    with open("data/food.txt", "r") as file:
        lines = [line.strip() for line in file if line.strip()]

    for i, chunk in enumerate(lines):
        collection.add(
            documents=[chunk],
            metadatas=[{"source": "food.txt"}],
            ids=[f"food-{i}"]
        )
    print("✅ Food data embedded into Chroma.")


def embed_metro_data():
    collection = chroma_client.get_or_create_collection(
        name="delhi-metro",
        embedding_function=embedding_fn
    )

    with open("data/metro_routes.txt", "r") as file:
        lines = [line.strip() for line in file if line.strip()]

    for i, chunk in enumerate(lines):
        collection.add(
            documents=[chunk],
            metadatas=[{"source": "metro.txt"}],
            ids=[f"metro-{i}"]
        )
    print("✅ Metro data embedded into Chroma.")


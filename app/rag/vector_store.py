import json
from pathlib import Path

import chromadb


DATA_PATH = Path("data/knowledge_base.json")
CHROMA_PATH = ".chroma"


client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = client.get_or_create_collection(
    name="support_knowledge_base"
)


def load_knowledge_base():
    with open(DATA_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def build_knowledge_base():
    documents = load_knowledge_base()

    if collection.count() > 0:
        return

    collection.add(
        ids=[str(i) for i in range(len(documents))],
        documents=[item["ticket"] for item in documents],
        metadatas=[
            {
                "category": item["category"],
                "resolution": item["resolution"],
            }
            for item in documents
        ],
    )


def search_similar_tickets(query: str, n_results: int = 3):
    results = collection.query(
        query_texts=[query],
        n_results=n_results,
    )

    return results

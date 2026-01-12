import json
from pathlib import Path
from .models import Document

DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "documents.json"

with open(DATA_PATH, "r", encoding="utf-8") as f:
    raw_docs = json.load(f)

DOCUMENTS = []

for idx, doc in enumerate(raw_docs):
    DOCUMENTS.append(
        Document(
            id=idx,
            title=doc.get("metadata", {}).get("title", "Untitled"),
            text=doc.get("page_content", "")
        )
    )

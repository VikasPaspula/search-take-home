from fastapi import APIRouter
from typing import List

from .models import SearchRequest, SearchResult
from .data import DOCUMENTS
from .integrations import (
    search_faiss,
    knowledge_graph_score,
    text_to_cypher,
)

router = APIRouter()


@router.post("/api/search", response_model=List[SearchResult])
def search(request: SearchRequest):

    cypher_query = text_to_cypher(request.query)

    vector_results = search_faiss(request.query, request.top_k * 3)

    best_results = {}

    for doc_index, vector_score in vector_results:
        document = DOCUMENTS[doc_index]

        cypher_bonus = 0.0
        if cypher_query.where:
            if request.query.lower() in document.text.lower():
                cypher_bonus = 0.1

        kg_score = knowledge_graph_score(request.query, document)

        final_score = (
            0.6 * vector_score +
            0.3 * kg_score +
            0.1 * cypher_bonus
        )

        final_score = min(max(final_score, 0.0), 1.0)

        existing = best_results.get(document.id)
        if existing is None or final_score > existing.score:
            best_results[document.id] = SearchResult(
                document=document,
                score=final_score
            )
            
    sorted_results = sorted(
        best_results.values(),
        key=lambda r: r.score,
        reverse=True
    )

    return sorted_results[: request.top_k]

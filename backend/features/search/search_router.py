from fastapi import APIRouter, HTTPException

from .data import DOCUMENTS  # noqa: F401
from .models import SearchEntry, SearchRequest, SearchResult
from .scoring import search_documents

router = APIRouter(prefix="/search", tags=["search"])
SEARCH_HISTORY: list[SearchEntry] = []


@router.post("", response_model=list[SearchResult])
async def search(request: SearchRequest) -> list[SearchResult]:
    """
    Search over the in-memory DOCUMENTS collection.
    - Implement simple ranking logic over DOCUMENTS based on `request.query`.
    - Return the top `request.top_k` results, sorted by score (highest first).

    Focus on clear, readable, and well-structured code.
    """
    query = request.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query must not be empty.")

    # TODO: implement ranking
    results: list[SearchResult] = []  # await search_documents(...)
    return results


@router.get("/history", response_model=list[SearchEntry])
async def get_history() -> list[SearchEntry]:
    """
    Return recent searches (most recent first).

    TODO (live exercise):
    - Read from the in-memory SEARCH_HISTORY list.
    - Consider ordering and size limits (e.g., last 10 items).
    """
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.post("/history", response_model=SearchEntry)
async def add_history(entry: SearchEntry) -> SearchEntry:
    """
    Store a new search query.

    TODO (live exercise):
    - Append to SEARCH_HISTORY.
    - Return the entry that was stored.
    - Decide how to handle duplicate queries (up to you).
    """
    raise HTTPException(status_code=501, detail="Not implemented yet")

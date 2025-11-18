from functools import lru_cache

from langchain_core.documents import Document

from .models import SearchResult


def rerank_result(query: str, document: Document) -> float:
    """Given a query, and a document, process both and return a score.

    The float should be representative of the quality of the document in relation to the query.

    You may use any technique you want, and you may use packages not specified, but if so you must
    add them to the requirements.txt.
    """
    # TODO
    return 0.0


@lru_cache()
def load_FAISS(documents: list[Document]):
    """Create and return a FAISS vector store from the DOCUMENTS list."""
    # TODO
    return


def search_documents(query: str, documents: list[Document]) -> list[SearchResult]:
    """Using the FAISS vector store, search for the query and return a list of SearchResults.

    After searching FAISS, you should rerank all the remaining results using your custom 'rerank_result'
    function, and removing bad results. You may add args/kwargs as needed.
    """
    # TODO - Search FAISS, rerank, filter.
    return []

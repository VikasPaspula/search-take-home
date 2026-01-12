import numpy as np
import faiss
from typing import List, Tuple

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.language_models.fake import FakeListLLM

from .models import Document, CypherQuery
from .data import DOCUMENTS

def embed_text(text: str) -> np.ndarray:
    """
    Deterministic mock embedding.
    Keeps behavior stable without external models.
    """
    np.random.seed(abs(hash(text)) % (2**32))
    return np.random.rand(384).astype("float32")


DIMENSION = 384
faiss_index = faiss.IndexFlatL2(DIMENSION)

doc_embeddings = np.array([embed_text(doc.text) for doc in DOCUMENTS])
faiss_index.add(doc_embeddings)


def search_faiss(query: str, top_k: int) -> List[Tuple[int, float]]:
    """
    Search FAISS using semantic similarity.
    Returns (document_index, similarity_score).
    """
    query_embedding = embed_text(query).reshape(1, -1)
    distances, indices = faiss_index.search(query_embedding, top_k)

    results = []
    for idx, dist in zip(indices[0], distances[0]):
        similarity = 1.0 / (1.0 + dist)
        results.append((idx, similarity))

    return results


def knowledge_graph_score(query: str, document: Document) -> float:

    query_terms = set(query.lower().split())
    doc_terms = set(document.text.lower().split())

    if not query_terms:
        return 0.0

    overlap = query_terms.intersection(doc_terms)
    return min(len(overlap) / len(query_terms), 1.0)


def text_to_cypher(query: str) -> CypherQuery:

    parser = PydanticOutputParser(pydantic_object=CypherQuery)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You convert natural language queries into Cypher queries "
                "over a graph of Document nodes.\n"
                "{format_instructions}"
            ),
            ("human", "{query}")
        ]
    ).partial(format_instructions=parser.get_format_instructions())

    fake_llm = FakeListLLM(
        responses=[
            """
            {
              "match": "(d:Document)",
              "where": "d.text CONTAINS 'machine'",
              "return_": "d"
            }
            """
        ]
    )

    chain = prompt | fake_llm | parser

    return chain.invoke({"query": query})

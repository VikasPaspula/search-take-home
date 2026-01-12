from pydantic import BaseModel
from typing import Optional


class Document(BaseModel):
    id: int
    title: str
    text: str


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5


class SearchResult(BaseModel):
    document: Document
    score: float


class CypherQuery(BaseModel):
    match: str
    where: Optional[str] = None
    return_: str = "d"

    def __str__(self) -> str:
        if self.where:
            return f"MATCH {self.match} WHERE {self.where} RETURN {self.return_}"
        return f"MATCH {self.match} RETURN {self.return_}"

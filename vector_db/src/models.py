from dataclasses import dataclass
from typing import List, Dict

@dataclass
class SearchResult:
    file_path: str
    similarity: float
    language: str
    repo: str
    code: str

@dataclass
class CodeEmbedding:
    vector: List[float]
    metadata: Dict
    content: str
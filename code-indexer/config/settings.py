import os
from typing import List

class Settings:
    # GitHub configuration
    GITHUB_API_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
    
    REPOSITORIES: List[str] = [
        "https://github.com/python/cpython",
        "https://github.com/django/django",
        "https://github.com/pallets/flask",
        "https://github.com/pwncollege/ctf-archive",
        "https://github.com/spring-projects/spring-boot",
        "https://github.com/protocolbuffers/protobuf",
    ]
    
    # File filtering
    CODE_EXTENSIONS: List[str] = [".py", ".java", ".c", ".cpp", ".js", ".go"]
    MAX_FILE_SIZE: int = 100000  # 100KB
    IGNORE_DIRS: List[str] = ["__pycache__", ".git", "node_modules", "venv"]
    

    # Storage
    REPOS_ROOT: str = "repositories"
    VECTOR_DB_PATH: str = "vector_db"
    CHROMA_COLLECTION_NAME: str = "code_embeddings"
    
    # Processing
    CHUNK_SIZE: int = 1000  # For large files
    MIN_CODE_LENGTH: int = 50  # Minimum chars to consider as valid code

settings = Settings()
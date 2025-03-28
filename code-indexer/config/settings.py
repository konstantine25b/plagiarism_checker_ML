import os
from typing import List

class Settings:
    # GitHub configuration
    GITHUB_API_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
    
    REPOSITORIES: List[str] = [
        "https://github.com/konstantine25b/Backend-Of-Plants-Ecommerce-Website",
        "https://github.com/konstantine25b/realtime-auth-signin-tracker-frontend",
        "https://github.com/langgenius/dify",
        "https://github.com/NirDiamant/GenAI_Agents",
        "https://github.com/shadps4-emu/shadPS4",
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
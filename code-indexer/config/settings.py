import os
from pathlib import Path
from typing import List

class Settings:
    # GitHub configuration
    GITHUB_API_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
    
    REPOSITORIES: List[str] = [
        "https://github.com/konstantine25b/Backend-Of-Plants-Ecommerce-Website",
        "https://github.com/konstantine25b/realtime-auth-signin-tracker-frontend",
        # "https://github.com/langgenius/dify",
        # "https://github.com/NirDiamant/GenAI_Agents",
        # "https://github.com/shadps4-emu/shadPS4",
    ]
    
    # File processing
    CODE_EXTENSIONS: List[str] = [".py", ".java", ".c", ".cpp", ".js", ".go"]
    MAX_FILE_SIZE: int = 100000  # 100KB
    IGNORE_DIRS: List[str] = ["__pycache__", ".git", "node_modules", "venv"]
    
    # Storage paths
    REPOS_ROOT: str = "repositories"
    VECTOR_DB_PATH: str = "data/vector_db"
    
    # Embedding configuration
    EMBEDDING_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_BATCH_SIZE: int = 32
    
    # Processing settings
    CHUNK_SIZE: int = 1000
    MIN_CODE_LENGTH: int = 50

    def __init__(self):
        """Initialize paths - called when settings is instantiated"""
        # Create required directories
        Path(self.REPOS_ROOT).mkdir(parents=True, exist_ok=True)
        Path(self.VECTOR_DB_PATH).mkdir(parents=True, exist_ok=True)

# Instantiate settings
settings = Settings()
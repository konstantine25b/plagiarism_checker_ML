import os
from pathlib import Path
from typing import List

class Settings:
    # GitHub configuration
    GITHUB_API_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
    
    REPOSITORIES: List[str] = [
        "https://github.com/konstantine25b/Backend-Of-Plants-Ecommerce-Website",
        "https://github.com/konstantine25b/realtime-auth-signin-tracker-frontend",
        "https://github.com/konstantine25b/realtime-auth-signin-tracker-backend",
        "https://github.com/konstantine25b/SnakeGame",
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


    def __init__(self):
        """Initialize required directories"""
        Path(self.REPOS_ROOT).mkdir(parents=True, exist_ok=True)

# Instantiate settings
settings = Settings()
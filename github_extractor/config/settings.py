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
    
    # Storage paths - now under data directory
    DATA_ROOT: str = "data"
    REPOS_DIR: str = "repositories"  # Now relative to DATA_ROOT

    def __init__(self):
        """Initialize required directories"""
        # Create full paths
        self._data_path = Path(self.DATA_ROOT)
        self._repos_path = self._data_path / self.REPOS_DIR
        
        # Create directories
        self._data_path.mkdir(parents=True, exist_ok=True)
        self._repos_path.mkdir(parents=True, exist_ok=True)

    @property
    def repos_root(self) -> str:
        """Get the full path to the repositories directory"""
        return str(self._repos_path)

# Instantiate settings
settings = Settings()
import os
from pathlib import Path

class Settings:
    # Embedding configuration
    EMBEDDING_MODEL = "microsoft/codebert-base"
    EMBEDDING_BATCH_SIZE = 16
    
    # Root data directory
    DATA_DIR = "data"
    
    # Path configuration (relative to DATA_DIR)
    CODE_DIR = "repositories"  # Where extracted code files are stored
    OUTPUT_DIR = "embeddings"  # Where to save the embeddings
    
    # File processing
    CODE_EXTENSIONS = [".py", ".java", ".js", ".go", ".c", ".cpp"]
    IGNORE_DIRS = ["__pycache__", ".git", "node_modules"]
    MAX_FILE_SIZE = 100000  # 100KB

    def __init__(self):
        """Ensure directories exist"""
        # Create full paths by joining with DATA_DIR
        self._data_path = Path(self.DATA_DIR)
        self._code_path = self._data_path / self.CODE_DIR
        self._output_path = self._data_path / self.OUTPUT_DIR
        
        # Create directories
        self._data_path.mkdir(parents=True, exist_ok=True)
        self._code_path.mkdir(parents=True, exist_ok=True)
        self._output_path.mkdir(parents=True, exist_ok=True)

    @property
    def code_dir(self):
        """Get full path to code directory"""
        return str(self._code_path)

    @property
    def output_dir(self):
        """Get full path to embeddings directory"""
        return str(self._output_path)

settings = Settings()
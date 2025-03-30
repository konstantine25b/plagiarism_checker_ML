from pathlib import Path

class Settings:
    # Directory setup
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR.parent / "data"  # Points to shared data directory
    
    # ChromaDB configuration
    CHROMA_DIR = DATA_DIR / "vector_db"
    COLLECTION_NAME = "code_embeddings"
    
    # Embedding source paths
    EMBEDDINGS_PATH = DATA_DIR / "embeddings" / "embeddings.npy"
    METADATA_PATH = DATA_DIR / "embeddings" / "metadata.json"
    
    # Indexing configuration (optimized for code search)
    INDEX_CONFIG = {
        "hnsw:space": "cosine",
        "hnsw:construction_ef": 128,
        "hnsw:search_ef": 64,
        "hnsw:M": 16
    }

    @classmethod
    def create_dirs(cls):
        """Ensure all required directories exist"""
        cls.CHROMA_DIR.mkdir(parents=True, exist_ok=True)

# Initialize directories
Settings.create_dirs()
# plagiarism_checker/config/settings.py
import os

class Settings:
    CHROMA_DIR = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "data",
        "vector_db"
    )
    EMBEDDINGS_PATH = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "data",
        "embeddings",
        "embeddings.npy"
    )
    METADATA_PATH = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "data",
        "embeddings",
        "metadata.json"
    )
    COLLECTION_NAME = "code_collection"
    INDEX_CONFIG = {"hnsw:space": "cosine"}
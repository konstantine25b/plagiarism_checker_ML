import os
import sys
import pytest
import numpy as np
import json
from pathlib import Path

# Add the parent directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.chroma_manager import ChromaCodeDB
from config.settings import Settings

@pytest.fixture
def test_db(tmp_path):
    """Test ChromaDB instance with controlled test data"""
    # Configure test paths
    Settings.CHROMA_DIR = tmp_path / "chroma_test"
    Settings.EMBEDDINGS_PATH = tmp_path / "embeddings.npy"
    Settings.METADATA_PATH = tmp_path / "metadata.json"
    
    # Create clear test embeddings (3D for simplicity)
    embeddings = np.array([
        [0.9, 0.1, 0.1],  # Will match query [1, 0, 0]
        [0.1, 0.8, 0.1],  # Will match query [0, 1, 0], slightly less than 0.9
        [0.1, 0.1, 0.7]   # Will match query [0, 0, 1], even less than 0.8
    ])
    np.save(Settings.EMBEDDINGS_PATH, embeddings)
    
    # Create matching metadata
    with open(Settings.METADATA_PATH, 'w') as f:
        json.dump({
            "files": [
                {"file_path": "match_x.py", "language": "python"},
                {"file_path": "match_y.py", "language": "python"},
                {"file_path": "match_z.py", "language": "python"}
            ]
        }, f)
    
    db = ChromaCodeDB()
    db.load_from_disk()
    return db

@pytest.fixture
def empty_db(tmp_path):
    """Test ChromaDB instance with empty collection"""
    # Use a different directory for empty tests
    Settings.CHROMA_DIR = tmp_path / "empty_test"
    db = ChromaCodeDB()
    # Ensure collection is empty by deleting if it exists, otherwise it will throw error.
    try:
        db.collection.delete()
    except ValueError:
        pass # collection does not exist, so it is empty
    return db

def test_similarity_ranking(test_db):
    """Test embeddings return in correct similarity order"""
    results = test_db.search([1.0, 0.0, 0.0])  # Should match first embedding
    
    assert len(results) == 3
    assert results[0]['file_path'] == "match_x.py"
    assert results[0]['similarity'] > results[1]['similarity']
    assert results[1]['similarity'] > results[2]['similarity']

def test_high_similarity_match(test_db):
    """Test very similar embeddings get high scores"""
    results = test_db.search([0.95, 0.05, 0.0])  # Very close to first embedding
    assert results[0]['similarity'] > 0.95

def test_metadata_integrity(test_db):
    """Test metadata persists through storage and retrieval"""
    results = test_db.search([0.0, 1.0, 0.0])  # Matches match_y.py
    assert results[0]['language'] == "python"
    assert results[0]['file_path'] == "match_y.py"

def test_empty_collection(empty_db):
    """Test search on empty collection"""
    results = empty_db.search([0.5, 0.5, 0.5])
    assert len(results) == 0

def test_exact_match_similarity(test_db):
    """Test exact match returns similarity ~1.0"""
    # Get the first stored embedding
    embeddings = np.load(Settings.EMBEDDINGS_PATH)
    results = test_db.search(embeddings[0].tolist())
    assert abs(results[0]['similarity'] - 1.0) < 0.01

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
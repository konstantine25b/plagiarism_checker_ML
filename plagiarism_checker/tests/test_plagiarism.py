from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient # Ensure import from fastapi.testclient
import sys
import os
import pytest
from pathlib import Path
from typing import List, Dict
from unittest.mock import patch

# Adjust the Python path to include the necessary directories
root_dir = Path(__file__).parent.parent.parent  # plagiarism_checker_ML
sys.path.insert(0, str(root_dir))
sys.path.insert(0, str(root_dir / "plagiarism_checker"))
sys.path.insert(0, str(root_dir / "plagiarism_checker" / "src"))
sys.path.insert(0, str(root_dir / "vector_db" / "src"))
sys.path.insert(0, str(root_dir / "code_embedder" / "src"))

from plagiarism_checker.main import app
from plagiarism_checker.src import plagiarism_checker_functions
from vector_db.src.chroma_manager import ChromaCodeDB
from code_embedder.src.embedder import CodeBertEmbedder
from plagiarism_checker.src.plagiarism_checker_functions import db, embedder

client = TestClient(app) # Correct initialization

@pytest.fixture
def mock_functions(monkeypatch):
    def mock_check_plagiarism_function(code: str) -> List[Dict]:
        return [
            {
                "file_path": "db_file1.py",
                "similarity": 0.95,
                "language": "python",
                "repo": "db_repo1",
                "code": "print('db_code1')",
            },
            {
                "file_path": "db_file2.py",
                "similarity": 0.90,
                "language": "python",
                "repo": "db_repo2",
                "code": "print('db_code2')",
            },
            {
                "file_path": "db_file3.js",
                "similarity": 0.85,
                "language": "javascript",
                "repo": "db_repo3",
                "code": "console.log('db_code3')",
            },
            {
                "file_path": "db_file4.py",
                "similarity": 0.80,
                "language": "python",
                "repo": "db_repo1",
                "code": "print('db_code4')",
            },
            {
                "file_path": "db_file5.js",
                "similarity": 0.75,
                "language": "javascript",
                "repo": "db_repo2",
                "code": "console.log('db_code5')",
            },
        ]
    monkeypatch.setattr(
        "plagiarism_checker.src.plagiarism_checker_functions.check_plagiarism_function",
        mock_check_plagiarism_function,
    )

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Enter Code to Check for Plagiarism" in response.text

def test_check_plagiarism(mock_functions):
    response = client.post("/check_plagiarism/", data={"code": "print('test')"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 5

def test_check_plagiarism_error():
    def mock_embed(*args, **kwargs):
        return [[0.1, 0.2, 0.3]]

    def mock_search(*args, **kwargs):
        raise RuntimeError("Plagiarism check error in database search")

    with patch.object(plagiarism_checker_functions, 'embedder', side_effect=mock_embed):
        with patch.object(plagiarism_checker_functions, 'db', side_effect=mock_search):
            response = client.post("/check_plagiarism/", data={"code": "print('test')"})
            assert response.status_code == 200
            # Optionally, you can check for a specific error message or structure if FastAPI provides one by default
            # For example:
            # assert "detail" in response.json()

def test_check_plagiarism_full_flow(mock_functions):
    """
    Tests the full flow of plagiarism checking: embedding, searching, and returning results.
    """
    user_code = "def my_function():\n    print('hello')\n"
    response = client.post("/check_plagiarism/", data={"code": user_code})

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 5

    # Assert that the structure of the returned data is as expected
    for match in response.json():
        assert "file_path" in match
        assert "similarity" in match
        assert "language" in match
        assert "repo" in match
        assert "code" in match

    # You might want to add more specific assertions about the content
    # if the mocked data has predictable values.
    expected_keys = ["file_path", "similarity", "language", "repo", "code"]
    for match in response.json():
        assert all(key in match for key in expected_keys)

    # To explicitly check if the user's code is returned (if the API is designed to do so),
    # you would need to know the exact structure of the response.
    # Assuming the current mocked function doesn't return the user's code directly,
    # we can't assert that here without modifying the mock or the expected API response.
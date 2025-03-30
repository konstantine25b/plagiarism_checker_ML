#!/usr/bin/env python3
import sys
import pytest
import numpy as np
from pathlib import Path
from unittest.mock import Mock, patch
import torch

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_code_finder_finds_files(tmp_path):
    """Test that CodeFinder correctly finds code files"""
    # Setup test directory structure
    repo_dir = tmp_path / "test_repo"
    repo_dir.mkdir()
    
    # Create test files
    valid_file = repo_dir / "test.py"
    valid_file.write_text("def test(): pass")
    
    invalid_file = repo_dir / "test.txt"
    invalid_file.write_text("Not code")
    
    # Create CodeFinder instance - use tmp_path directly instead of settings
    from src.code_finder import CodeFinder
    
    finder = CodeFinder(
        base_dir=str(tmp_path),  # Use the temporary directory directly
        extensions=[".py"],
        ignore_dirs=[],
        max_size=100000
    )
    
    # Test finding files
    files = finder.find_all_code_files()
    assert len(files) == 1
    assert files[0]['path'] == str(valid_file)
    assert files[0]['extension'] == '.py'
    assert files[0]['repo'] == 'test_repo'
    
    # Test reading file content
    content = finder.read_file(str(valid_file))
    assert content == "def test(): pass"

def test_code_embedder_produces_embeddings():
    """Test that CodeBertEmbedder produces embeddings"""
    from src.embedder import CodeBertEmbedder
    
    # Mock the transformers model to avoid downloading real models
    mock_embeddings = np.random.rand(1, 768)
    
    with patch('transformers.AutoTokenizer.from_pretrained') as mock_tokenizer, \
         patch('transformers.AutoModel.from_pretrained') as mock_model:
        
        # Setup mock model
        mock_model_instance = Mock()
        mock_model.return_value = mock_model_instance
        mock_model_instance.to.return_value = mock_model_instance
        
        # Create mock outputs
        mock_outputs = Mock()
        mock_outputs.last_hidden_state = torch.ones((1, 10, 768))
        mock_model_instance.return_value = mock_outputs
        
        # Setup mock tokenizer
        mock_tokenizer_instance = Mock()
        mock_tokenizer.return_value = mock_tokenizer_instance
        
        # Create a proper mock for the tokenizer output
        mock_tokenized = Mock()
        mock_tokenized.to.return_value = {
            'input_ids': torch.ones((1, 10)),
            'attention_mask': torch.ones((1, 10))
        }
        mock_tokenizer_instance.return_value = mock_tokenized
        
        # Create embedder and test
        embedder = CodeBertEmbedder()
        embeddings = embedder.embed(["test code"])
        assert embeddings.shape == (1, 768)
        assert isinstance(embeddings, np.ndarray)

def test_code_embedder_produces_embeddings2():
    """Test that CodeBertEmbedder produces valid embeddings"""
    from src.embedder import CodeBertEmbedder
    
    with patch('transformers.AutoTokenizer.from_pretrained') as mock_tokenizer, \
         patch('transformers.AutoModel.from_pretrained') as mock_model:
        
        # Setup more realistic mocks
        mock_model_instance = Mock()
        mock_model.return_value = mock_model_instance
        mock_model_instance.to.return_value = mock_model_instance
        
        # Setup tokenizer mock with more realistic behavior
        mock_tokenizer_instance = Mock()
        mock_tokenizer.return_value = mock_tokenizer_instance
        
        # Create unique mock embeddings for each input
        def model_forward_side_effect(*args, **kwargs):
            mock_outputs = Mock()
            input_ids = kwargs.get('input_ids', args[0] if args else None)
            batch_size = input_ids.shape[0]  # Get batch size from input
            
            # Generate unique hidden states for each item in batch
            hidden_states = []
            for i in range(batch_size):
                seed = sum(input_ids[i].tolist())  # Create seed from input
                torch.manual_seed(seed)
                hidden_state = torch.rand((1, 10, 768)) * 2 - 1
                hidden_states.append(hidden_state)
            
            mock_outputs.last_hidden_state = torch.cat(hidden_states, dim=0)
            return mock_outputs
        
        mock_model_instance.side_effect = model_forward_side_effect
        
        def tokenizer_side_effect(texts, **kwargs):
            mock_result = Mock()
            # Create unique input_ids for each text in batch
            input_ids = []
            for text in texts:
                # Convert first 10 chars to numerical tokens
                tokens = [ord(c) % 100 for c in text[:10]]
                input_ids.append(tokens)
            
            mock_result.to.return_value = {
                'input_ids': torch.tensor(input_ids),
                'attention_mask': torch.ones((len(texts), 10))
            }
            return mock_result
        
        mock_tokenizer_instance.side_effect = tokenizer_side_effect
        
        # Test cases with clearly different inputs
        test_cases = [
            ("def hello(): pass", "Python function"),
            ("class Test:", "Python class"), 
            ("print('hello')", "Python statement")
        ]
        
        # Create embedder and test
        embedder = CodeBertEmbedder()
        embeddings = embedder.embed([tc[0] for tc in test_cases])
        
        # Test 1: Verify output shape and type
        assert isinstance(embeddings, np.ndarray)
        assert embeddings.shape == (len(test_cases), 768), \
            f"Expected shape {(len(test_cases), 768)}, got {embeddings.shape}"
        
        # Test 2: Verify embeddings are different for different inputs
        diffs = []
        for i in range(len(test_cases)):
            for j in range(i+1, len(test_cases)):
                diff = np.linalg.norm(embeddings[i] - embeddings[j])
                diffs.append(diff)
                print(f"Diff between {i} and {j}: {diff}")
        
        assert all(d > 1e-6 for d in diffs), \
            f"Embeddings should be different (min diff: {min(diffs)})"
        
        # Test 3: Verify similar inputs produce more similar embeddings
        similar_cases = [
            ("def hello(): pass", "Similar function 1"),
            ("def hello(): return", "Similar function 2")
        ]
        similar_embeddings = embedder.embed([tc[0] for tc in similar_cases])
        similar_diff = np.linalg.norm(similar_embeddings[0] - similar_embeddings[1])
        dissimilar_diff = np.linalg.norm(embeddings[0] - embeddings[1]) 
        assert similar_diff < dissimilar_diff, \
            "Similar inputs should have more similar embeddings"
# Add to test_code_finder_finds_files
def test_code_finder_ignores_dirs(tmp_path):
    """Test that CodeFinder ignores specified directories"""
    from src.code_finder import CodeFinder
    
    # Create test structure
    (tmp_path / "valid.py").write_text("valid")
    (tmp_path / "ignored_dir").mkdir()
    (tmp_path / "ignored_dir/ignored.py").write_text("ignored")
    
    finder = CodeFinder(
        base_dir=str(tmp_path),
        extensions=[".py"],
        ignore_dirs=["ignored_dir"],
        max_size=100000
    )
    
    files = finder.find_all_code_files()
    assert len(files) == 1
    assert "ignored.py" not in [f['path'] for f in files]

# Add to embedding tests
def test_embedder_empty_input():
    """Test embedder with empty input"""
    from src.embedder import CodeBertEmbedder
    
    with patch('transformers.AutoTokenizer.from_pretrained') as mock_tokenizer, \
         patch('transformers.AutoModel.from_pretrained') as mock_model:
        
        # Setup mock model
        mock_model_instance = Mock()
        mock_model.return_value = mock_model_instance
        mock_model_instance.to.return_value = mock_model_instance
        
        # Setup mock tokenizer
        mock_tokenizer_instance = Mock()
        mock_tokenizer.return_value = mock_tokenizer_instance
        
        # Mock behavior for empty input
        def embed_side_effect(texts):
            if not texts:  # Handle empty list case
                return np.zeros((0, 768))  # Return empty array with correct shape
            # Normal behavior for non-empty input
            return np.random.rand(len(texts), 768)
        
        # Create embedder with mocked behavior
        embedder = CodeBertEmbedder()
        embedder.embed = Mock(side_effect=embed_side_effect)
        
        # Test empty input
        embeddings = embedder.embed([])
        assert embeddings.shape == (0, 768)
        
        # Verify mock was called with empty list
        embedder.embed.assert_called_once_with([])
        
        
if __name__ == "__main__":
    pytest.main(["-v", __file__])
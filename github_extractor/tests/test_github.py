import os
import sys
import pytest
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.repo_getter import RepoGetter
from config.settings import settings

@pytest.fixture
def repo_getter():
    """Fixture that provides initialized RepoGetter"""
    return RepoGetter(repos_dir=settings.repos_root)  # Changed to use repos_root property

@pytest.fixture
def cloned_repos(repo_getter):
    """Fixture that clones repositories and returns paths"""
    return repo_getter.clone_repos(settings.REPOSITORIES)

def test_github_cloning(cloned_repos):
    """Test repository cloning functionality only"""
    print("\n=== Testing GitHub Repository Cloning ===")
    assert len(cloned_repos) > 0, "No repositories were cloned"
    
    print(f"Cloned {len(cloned_repos)} repositories:")
    for i, path in enumerate(cloned_repos, 1):
        status = "✅" if path and Path(path).exists() else "❌"
        print(f"{i}. {path} {status}")
        assert Path(path).exists(), f"Repository path {path} does not exist"
        # Verify path is under data/repositories
        assert str(Path(path).parent.parent) == str(Path(settings.DATA_ROOT).resolve()), \
               "Repository not stored in data directory"

if __name__ == "__main__":
    # Manual test execution
    print("Running cloning tests directly...")
    
    getter = RepoGetter(repos_dir=settings.repos_root)  # Changed to use repos_root
    cloned = getter.clone_repos(settings.REPOSITORIES)
    
    print("\n=== Cloning Results ===")
    for i, path in enumerate(cloned, 1):
        status = "✅" if path and Path(path).exists() else "❌"
        print(f"{i}. {path} {status}")
    
    print("\n=== Test Complete ===")
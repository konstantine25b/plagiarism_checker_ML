import os
import sys
import pytest
from pathlib import Path
from typing import List, Dict

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.repo_getter import RepoGetter
from src.code_finder import CodeFinder
from config.settings import settings

@pytest.fixture
def repo_getter():
    """Fixture that provides initialized RepoGetter"""
    return RepoGetter(repos_dir=settings.REPOS_ROOT)

@pytest.fixture
def code_finder():
    """Fixture that provides initialized CodeFinder with settings"""
    return CodeFinder(
        base_dir=settings.REPOS_ROOT,
        extensions=settings.CODE_EXTENSIONS,
        ignore_dirs=settings.IGNORE_DIRS,
        max_size=settings.MAX_FILE_SIZE
    )

@pytest.fixture
def cloned_repos(repo_getter):
    """Fixture that clones repositories and returns paths"""
    return repo_getter.clone_repos(settings.REPOSITORIES)

@pytest.fixture
def code_files(code_finder, cloned_repos):
    """Fixture that finds code files in cloned repositories"""
    return code_finder.find_all_code_files()

def test_github_cloning(cloned_repos):
    """Test repository cloning functionality"""
    print("\n=== Testing GitHub Repository Cloning ===")
    assert len(cloned_repos) > 0, "No repositories were cloned"
    
    print(f"Cloned {len(cloned_repos)} repositories:")
    for i, path in enumerate(cloned_repos, 1):
        status = "✅" if path and Path(path).exists() else "❌"
        print(f"{i}. {path} {status}")
        assert Path(path).exists(), f"Repository path {path} does not exist"

def test_code_finding(code_files):
    """Test code file discovery functionality"""
    print("\n=== Testing Code File Finding ===")
    assert len(code_files) > 0, "No code files found"
    
    print(f"Found {len(code_files)} code files matching criteria:")
    print(f"Extensions: {settings.CODE_EXTENSIONS}")
    print(f"Max size: {settings.MAX_FILE_SIZE} bytes")
    print(f"Ignored dirs: {settings.IGNORE_DIRS}")
    
    # Group by repository
    repos: Dict[str, List[Dict]] = {}
    for file in code_files:
        repos.setdefault(file['repo'], []).append(file)
    
    for repo_name, files in repos.items():
        print(f"\nRepository: {repo_name}")
        print(f"Files found: {len(files)}")
        print("Sample files:")
        for file in files[:3]:
            print(f"  - {file['relative_path']} ({file['size']} bytes)")
            assert Path(file['path']).exists(), f"File {file['path']} does not exist"

def test_file_reading(code_finder, code_files):
    """Test file content reading functionality"""
    print("\n=== Testing File Content Reading ===")
    test_files = [f for f in code_files if f['extension'] == '.py'][:3]
    assert len(test_files) > 0, "No Python files found for testing"
    
    for file in test_files:
        content = code_finder.read_file(file['path'])
        print(f"\nFile: {file['relative_path']}")
        print(f"Size: {file['size']} bytes")
        
        if content:
            print(f"First line: {content.splitlines()[0][:100]}...")
            assert len(content) > 0, "File content is empty"
        else:
            pytest.fail(f"Could not read file: {file['path']}")

if __name__ == "__main__":
    # Manual test execution
    print("Running tests directly...")
    
    # Initialize components
    getter = RepoGetter(repos_dir=settings.REPOS_ROOT)
    finder = CodeFinder(
        base_dir=settings.REPOS_ROOT,
        extensions=settings.CODE_EXTENSIONS,
        ignore_dirs=settings.IGNORE_DIRS,
        max_size=settings.MAX_FILE_SIZE
    )
    
    # 1. Test cloning
    cloned = getter.clone_repos(settings.REPOSITORIES)
    print("\n=== Cloning Results ===")
    for i, path in enumerate(cloned, 1):
        status = "✅" if path and Path(path).exists() else "❌"
        print(f"{i}. {path} {status}")
    
    # 2. Test file finding
    files = finder.find_all_code_files()
    print("\n=== Code Files ===")
    print(f"Found {len(files)} files")
    
    # 3. Test file reading
    # 3. Test file reading
    print("\n=== File Contents ===")
    test_files = [f for f in files if f['extension'] == '.py' and f['size'] > 0][:3]  # Skip empty files
    for file in test_files:
        content = finder.read_file(file['path'])
        if content:
            print(f"\n{file['relative_path']}:")
            print(content[:100] + ("..." if len(content) > 100 else ""))
        else:
            print(f"\nCould not read file: {file['path']} (size: {file['size']} bytes)")
    
    print("\n=== Test Complete ===")
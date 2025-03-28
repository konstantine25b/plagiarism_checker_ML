import os
import sys
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.github.repo_getter import RepoGetter
from src.github.code_finder import CodeFinder
from config.settings import settings

def test_github_cloning():
    print("=== Testing GitHub Repository Cloning ===")
    
    # Initialize the repo getter with settings
    getter = RepoGetter(repos_dir=settings.REPOS_ROOT)
    
    # Clone all repositories from settings
    print(f"\nCloning {len(settings.REPOSITORIES)} repositories...")
    cloned_paths = getter.clone_repos(settings.REPOSITORIES)
    
    print("\nCloning results:")
    for i, path in enumerate(cloned_paths, 1):
        print(f"{i}. {path} {'✅' if path else '❌'}")
    
    return cloned_paths

def test_code_finding():
    print("\n=== Testing Code File Finding ===")
    
    finder = CodeFinder()
    code_files = finder.find_all_code_files()
    
    print(f"\nFound {len(code_files)} code files matching criteria:")
    print(f"Extensions: {settings.CODE_EXTENSIONS}")
    print(f"Max size: {settings.MAX_FILE_SIZE} bytes")
    print(f"Ignored dirs: {settings.IGNORE_DIRS}")
    
    # Print summary by repository
    repos = {}
    for file in code_files:
        repos.setdefault(file['repo_name'], []).append(file)
    
    for repo_name, files in repos.items():
        print(f"\nRepository: {repo_name}")
        print(f"Files found: {len(files)}")
        print("Sample files:")
        for file in files[:3]:  # Show first 3 files per repo
            print(f"  - {file['relative_path']} ({file['size_bytes']} bytes)")
    
    return code_files

def test_file_reading(code_files):
    print("\n=== Testing File Content Reading ===")
    
    finder = CodeFinder()
    test_files = [f for f in code_files if f['extension'] == '.py'][:3]  # Test 3 Python files
    
    for file in test_files:
        content = finder.read_file_safely(file['file_path'])
        if content:
            print(f"\nFile: {file['relative_path']}")
            print(f"Size: {file['size_bytes']} bytes")
            print(f"First line: {content.splitlines()[0][:100]}...")
        else:
            print(f"\nCould not read file: {file['file_path']}")

if __name__ == "__main__":
    # Run all tests
    cloned_paths = test_github_cloning()
    found_files = test_code_finding()
    test_file_reading(found_files)
    
    print("\n=== GitHub Module Test Complete ===")
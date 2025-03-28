import os
import sys
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.github.repo_getter import RepoGetter
from src.github.file_finder import FileFinder
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

def test_file_finding(cloned_paths):
    print("\n=== Testing Code File Discovery ===")
    
    finder = FileFinder(repos_dir=settings.REPOS_ROOT)
    total_files = 0
    
    for repo_path in cloned_paths:
        if not repo_path:
            continue
            
        repo_name = os.path.basename(repo_path)
        print(f"\nFinding code files in {repo_name}...")
        
        code_files = finder.find_code_files(repo_name)
        print(f"Found {len(code_files)} code files")
        
        # Show first 5 files as sample
        for file in code_files[:5]:
            print(f"  - {file['name']} ({file['path']})")
        
        total_files += len(code_files)
    
    print(f"\nTotal code files found across all repos: {total_files}")

def test_file_reading(cloned_paths):
    print("\n=== Testing File Content Reading ===")
    
    finder = FileFinder(repos_dir=settings.REPOS_ROOT)
    
    for repo_path in cloned_paths[:2]:  # Test first 2 repos only
        if not repo_path:
            continue
            
        repo_name = os.path.basename(repo_path)
        code_files = finder.find_code_files(repo_name)[:3]  # Test first 3 files
        
        print(f"\nReading files from {repo_name}:")
        for file in code_files:
            content = finder.read_file(file['path'])
            if content:
                print(f"  - {file['name']}: {len(content)} chars")
            else:
                print(f"  - {file['name']}: ❌ Could not read")

if __name__ == "__main__":
    # Run all tests
    cloned = test_github_cloning()
    test_file_finding(cloned)
    test_file_reading(cloned)
    
    print("\n=== GitHub Module Test Complete ===")
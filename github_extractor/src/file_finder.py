import os
from pathlib import Path
from typing import List, Dict, Optional

class FileFinder:
    def __init__(
        self,
        repos_dir: str = "repositories",
        code_extensions: List[str] = None,
        ignore_dirs: List[str] = None,
        max_file_size: int = 100000  # 100KB default
    ):
        self.repos_dir = Path(repos_dir)
        self.code_extensions = code_extensions or ['.py', '.java', '.c', '.cpp', '.js']
        self.ignore_dirs = ignore_dirs or ['__pycache__', '.git', 'node_modules']
        self.max_file_size = max_file_size

    def find_code_files(self, repo_name: str) -> List[Dict]:
        """Find all code files in a repository with metadata"""
        repo_path = self.repos_dir / repo_name
        if not repo_path.exists():
            return []

        code_files = []
        
        for root, dirs, files in os.walk(repo_path):
            # Skip ignored directories
            dirs[:] = [d for d in dirs if d not in self.ignore_dirs]
            
            for file in files:
                file_path = Path(root) / file
                if self._is_valid_code_file(file_path):
                    code_files.append({
                        'path': str(file_path),
                        'repo': repo_name,
                        'name': file,
                        'extension': file_path.suffix,
                        'size': file_path.stat().st_size,
                        'relative_path': str(file_path.relative_to(repo_path))
                    })
                    
        return code_files

    def _is_valid_code_file(self, file_path: Path) -> bool:
        """Check if file meets all criteria"""
        return (
            file_path.is_file() and
            file_path.suffix in self.code_extensions and
            file_path.stat().st_size <= self.max_file_size
        )

    def read_file(self, file_path: str) -> Optional[str]:
        """Safely read file content with error handling"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except (IOError, UnicodeDecodeError) as e:
            print(f"Error reading {file_path}: {str(e)}")
            return None
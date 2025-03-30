from pathlib import Path
from typing import List, Dict, Optional
import os

class CodeFinder:
    def __init__(
        self,
        base_dir: str,
        extensions: List[str],
        ignore_dirs: List[str],
        max_size: int
    ):
        self.base_dir = Path(base_dir)
        self.extensions = extensions
        self.ignore_dirs = ignore_dirs
        self.max_size = max_size

    def find_all_code_files(self) -> List[Dict]:
        """Find all code files in all repositories"""
        code_files = []
        for repo_dir in self.base_dir.iterdir():
            if repo_dir.is_dir():
                code_files.extend(self._find_files_in_repo(repo_dir))
        return code_files

    def _find_files_in_repo(self, repo_path: Path) -> List[Dict]:
        """Find code files in a single repository"""
        files = []
        for root, dirs, files_in_dir in os.walk(repo_path):
            # Skip ignored directories
            dirs[:] = [d for d in dirs if d not in self.ignore_dirs]
            
            for file in files_in_dir:
                file_path = Path(root) / file
                if self._is_valid_code_file(file_path):
                    files.append({
                        'path': str(file_path),
                        'extension': file_path.suffix,
                        'size': file_path.stat().st_size,
                        'repo': repo_path.name,
                        'relative_path': str(file_path.relative_to(repo_path))
                    })
        return files

    def _is_valid_code_file(self, file_path: Path) -> bool:
        """Check if file meets all criteria"""
        return (
            file_path.is_file() and
            file_path.suffix in self.extensions and
            file_path.stat().st_size <= self.max_size
        )

    def read_file(self, file_path: str) -> Optional[str]:
        """Read file content with proper error handling"""
        try:
            # First check if file is empty
            if os.path.getsize(file_path) == 0:
                return "[Empty file]"
                
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()  # Remove whitespace
                return content if content else "[Empty file]"
        except (IOError, UnicodeDecodeError) as e:
            print(f"Error reading file {file_path}: {str(e)}")
            return None
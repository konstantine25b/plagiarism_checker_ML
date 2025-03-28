import os
from pathlib import Path
from typing import List, Dict, Optional
from config.settings import settings

class CodeFinder:
    def __init__(self):
        self.repos_root = Path(settings.REPOS_ROOT)
        self.code_extensions = settings.CODE_EXTENSIONS
        self.max_file_size = settings.MAX_FILE_SIZE
        self.ignore_dirs = settings.IGNORE_DIRS

    def find_all_code_files(self) -> List[Dict]:
        """
        Find all code files in repositories directory that match criteria
        Returns: List of dictionaries with file metadata
        """
        if not self.repos_root.exists():
            raise FileNotFoundError(f"Repositories directory not found: {self.repos_root}")

        code_files = []
        for repo_dir in self.repos_root.iterdir():
            if repo_dir.is_dir():
                code_files.extend(self._scan_repository(repo_dir))
        return code_files

    def _scan_repository(self, repo_dir: Path) -> List[Dict]:
        """Scan a single repository for valid code files"""
        valid_files = []
        
        for root, dirs, files in os.walk(repo_dir):
            # Filter out ignored directories
            dirs[:] = [d for d in dirs if d not in self.ignore_dirs]
            
            for filename in files:
                file_path = Path(root) / filename
                if self._is_valid_code_file(file_path):
                    valid_files.append({
                        'repo_name': repo_dir.name,
                        'file_path': str(file_path),
                        'relative_path': str(file_path.relative_to(repo_dir)),
                        'extension': file_path.suffix,
                        'size_bytes': file_path.stat().st_size,
                        'last_modified': file_path.stat().st_mtime
                    })
        return valid_files

    def _is_valid_code_file(self, file_path: Path) -> bool:
        """Check if a file meets all our criteria"""
        return (file_path.suffix in self.code_extensions and
                file_path.is_file() and
                file_path.stat().st_size <= self.max_file_size)

    def read_file_safely(self, file_path: str) -> Optional[str]:
        """Read file content with proper error handling"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if len(content) >= settings.MIN_CODE_LENGTH:
                    return content
        except OSError as e:
            print(f"Error reading {file_path}: {str(e)}")
        return None
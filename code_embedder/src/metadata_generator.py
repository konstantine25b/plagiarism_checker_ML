import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict
import logging

logger = logging.getLogger(__name__)

class MetadataGenerator:
    """Generates comprehensive metadata for code files"""
    
    @staticmethod
    def generate(file_path: str) -> Dict:
        """Generate complete metadata for a code file"""
        path = Path(file_path)
        
        try:
            stats = path.stat()
            return {
                "file_path": str(path),
                "file_name": path.name,
                "repo_name": MetadataGenerator._extract_repo_name(path),
                "language": MetadataGenerator._detect_language(path),
                "file_size": stats.st_size,
                "last_modified": datetime.fromtimestamp(stats.st_mtime).isoformat(),
                "file_hash": MetadataGenerator._calculate_hash(path),
                "file_extension": path.suffix.lower()
            }
        except Exception as e:
            logger.error(f"Metadata generation failed for {file_path}: {str(e)}")
            return None

    @staticmethod
    def _extract_repo_name(path: Path) -> str:
        """Extract repository name from path structure"""
        parts = path.parts
        try:
            if "repositories" in parts:
                repo_index = parts.index("repositories") + 1
                if repo_index < len(parts):
                    return parts[repo_index]
        except Exception as e:
            logger.warning(f"Couldn't extract repo name from {path}: {str(e)}")
        return "unknown"

    @staticmethod
    def _detect_language(path: Path) -> str:
        """Detect programming language from file extension"""
        language_map = {
            '.js': 'JavaScript',
            '.py': 'Python',
            '.java': 'Java',
            '.go': 'Go',
            '.c': 'C',
            '.cpp': 'C++',
            '.h': 'C/C++ Header',
            '.ts': 'TypeScript',
            '.sh': 'Shell',
            '.rb': 'Ruby',
            '.php': 'PHP',
            '.rs': 'Rust'
        }
        return language_map.get(path.suffix.lower(), 'unknown')

    @staticmethod
    def _calculate_hash(path: Path) -> str:
        """Calculate MD5 hash of file content"""
        hasher = hashlib.md5()
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                if not chunk:
                    break
                hasher.update(chunk)
        return hasher.hexdigest()
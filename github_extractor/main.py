#!/usr/bin/env python3
import logging
import sys
from pathlib import Path
from typing import Dict, List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def main() -> List[Dict]:
    """
    Clone repositories and find code files.
    Returns list of found code files with metadata.
    """
    try:
        # Dynamic import after ensuring src is in path
        sys.path.insert(0, str(Path(__file__).parent))
        from src.code_finder import CodeFinder
        from src.repo_getter import RepoGetter
        from config.settings import settings

        logger.info("Starting repository processing...")
        
        # Step 1: Clone repositories
        getter = RepoGetter(repos_dir=settings.REPOS_ROOT)
        cloned_repos = getter.clone_repos(settings.REPOSITORIES)
        
        if not cloned_repos:
            logger.error("No repositories were cloned successfully")
            return []

        # Step 2: Find code files
        finder = CodeFinder(
            base_dir=settings.REPOS_ROOT,
            extensions=settings.CODE_EXTENSIONS,
            ignore_dirs=settings.IGNORE_DIRS,
            max_size=settings.MAX_FILE_SIZE
        )
        code_files = finder.find_all_code_files()
        
        logger.info(f"Found {len(code_files)} code files across {len(cloned_repos)} repositories")
        return code_files
        
    except ImportError as e:
        logger.error(f"Import error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Processing failed: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
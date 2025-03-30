#!/usr/bin/env python3
import logging
import sys
from pathlib import Path
from typing import List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def main() -> List[str]:
    """
    Clone repositories only.
    Returns list of cloned repository paths.
    """
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from src.repo_getter import RepoGetter
        from config.settings import settings

        logger.info("Starting repository cloning...")
        
        # Use the correct path from settings
        getter = RepoGetter(repos_dir=settings.repos_root)  # Changed to use the property
        cloned_repos = getter.clone_repos(settings.REPOSITORIES)
        
        if not cloned_repos:
            logger.error("No repositories were cloned successfully")
            return []

        logger.info(f"Successfully cloned {len(cloned_repos)} repositories")
        return cloned_repos
        
    except ImportError as e:
        logger.error(f"Import error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Cloning failed: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
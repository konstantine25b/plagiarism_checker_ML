import os
from pathlib import Path
from typing import List, Optional
from git import Repo
from git.exc import GitError
import logging

logger = logging.getLogger(__name__)

class RepoGetter:
    def __init__(self, repos_dir: str = "repositories"):
        self.repos_dir = Path(repos_dir)
        os.makedirs(self.repos_dir, exist_ok=True)
        logger.info(f"Ensured repositories directory exists at: {self.repos_dir}")


    def clone_repo(self, repo_url: str) -> Optional[str]:
        """Clone or update a single repository"""
        try:
            logger.info(f"Attempting to clone/update repository from URL: {repo_url}")
     
            repo_name = self._extract_repo_name(repo_url)
            repo_path = self.repos_dir / repo_name
            
            if repo_path.exists():
                self._update_repo(repo_path)
            else:
                logger.info(f"Cloning repository from: {repo_url} to: {repo_path}")
                Repo.clone_from(repo_url, str(repo_path))
                logger.info(f"Successfully cloned repository from {repo_url} to {repo_path}.")

                
            return str(repo_path)
            
        except GitError as e:
            print(f"Failed to clone {repo_url}: {str(e)}")
            return None

    def clone_repos(self, repo_urls: List[str]) -> List[str]:
        """Clone multiple repositories with progress feedback"""
        return [path for url in repo_urls 
               if (path := self.clone_repo(url)) is not None]

    def _extract_repo_name(self, repo_url: str) -> str:
        """Extract repository name from URL"""
        return repo_url.split('/')[-1].replace('.git', '')

    def _update_repo(self, repo_path: Path):
        """Pull latest changes for existing repository"""
        print(f"Updating {repo_path.name}...")
        repo = Repo(str(repo_path))
        repo.remotes.origin.pull()
import os
from git import Repo
from git.exc import GitError

class RepoGetter:
    def __init__(self, repos_dir="repositories"):
        self.repos_dir = repos_dir
        os.makedirs(self.repos_dir, exist_ok=True)

    def clone_repo(self, repo_url):
        """Clone a single repository and return its local path"""
        try:
            repo_name = repo_url.split('/')[-1].replace('.git', '')
            repo_path = os.path.join(self.repos_dir, repo_name)
            
            if os.path.exists(repo_path):
                print(f"Repository already exists at {repo_path}")
                return repo_path
                
            print(f"Cloning {repo_url}...")
            Repo.clone_from(repo_url, repo_path)
            return repo_path
            
        except GitError as e:
            print(f"Failed to clone {repo_url}: {str(e)}")
            return None

    def clone_repos(self, repo_urls):
        """Clone multiple repositories"""
        return [path for url in repo_urls 
               if (path := self.clone_repo(url)) is not None]
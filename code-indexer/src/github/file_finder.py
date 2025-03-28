import os

class FileFinder:
    def __init__(self, repos_dir="repositories"):
        self.repos_dir = repos_dir
        self.code_extensions = ['.py', '.java', '.c', '.cpp', '.js']
        self.ignore_dirs = ['__pycache__', '.git', 'node_modules']

    def find_code_files(self, repo_name):
        """Find all code files in a repository"""
        repo_path = os.path.join(self.repos_dir, repo_name)
        if not os.path.exists(repo_path):
            return []
            
        code_files = []
        
        for root, dirs, files in os.walk(repo_path):
            # Skip ignored directories
            dirs[:] = [d for d in dirs if d not in self.ignore_dirs]
            
            for file in files:
                if any(file.endswith(ext) for ext in self.code_extensions):
                    file_path = os.path.join(root, file)
                    code_files.append({
                        'path': file_path,
                        'repo': repo_name,
                        'name': file
                    })
                    
        return code_files

    def read_file(self, file_path):
        """Read the content of a code file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception:
            print(f"Could not read file: {file_path}")
            return None
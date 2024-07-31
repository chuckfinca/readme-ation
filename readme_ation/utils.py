import os
import sys
import logging
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_python_version():
    return sys.version.split()[0]

def open_or_create_readme(readme_path):
    if os.path.exists(readme_path):
        with open(readme_path, 'r') as file:
            return file.read()
    else:
        return ""
    
def check_for_notebook(file_paths):
    if isinstance(file_paths, str):  # If it's a directory
        return any(file.endswith('.ipynb') for file in os.listdir(file_paths))
    elif isinstance(file_paths, list):  # If it's a list of files
        return any(file.endswith('.ipynb') for file in file_paths)
    else:
        raise ValueError("file_paths must be a string (directory) or a list of files")

def _get_repo_name(repo_url):
    # Remove .git extension if present
    repo_url = repo_url.rstrip('.git')
    # Get the last part of the URL (after the last slash)
    repo_name = os.path.basename(repo_url)
    # Remove any non-alphanumeric characters except hyphens and underscores
    repo_name = re.sub(r'[^\w-]', '', repo_name)
    return repo_name
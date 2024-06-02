import os
from readme_ation.utils import find_all_py_files
from readme_ation.readme_generator import add_setup_with_versions, add_project_description

def main():
    directory = input("Enter the directory to search for .py files: ").strip()
    readme_path = os.path.join(directory, "README.md")
    
    file_paths = find_all_py_files(directory)
    add_setup_with_versions(file_paths, readme_path)
    
    project_details = {
        "overview": "Your overview here",
        "motivation": "Your motivation here",
        "technologies": "Your technologies here",
        "approach": "Your approach here",
        "challenges": "Your challenges here",
        "key_takeaways": "Your key takeaways here",
        "acknowledgments": "Your acknowledgments here"
    }
    add_project_description(readme_path, project_details)

if __name__ == "__main__":
    main()

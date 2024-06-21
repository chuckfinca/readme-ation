import readme_ation

project_folder_path = "./examples/project_description/"

# Define the path to the README.md file in the current file's directory
readme_path = project_folder_path + "README.md"

# Example project details
project_details = {
    'title': 'Custom Title',
    'overview': 'This is an example project that demonstrates the usage of readme-ation.',
    'motivation': 'Automating README generation saves time and ensures consistency.',
    'technologies': 'Python, Mamba, and other dependencies.',
    'approach': 'Scanning files for imports and creating setup instructions automatically.',
    'challenges': 'Handling various edge cases in dependency detection.',
    'key_takeaways': 'Using readme-ation can significantly improve your project documentation workflow.',
    'acknowledgments': 'Thanks to all contributors and the open-source community.'
}

# Update the README.md file with the project details
readme_ation.add_project_description(readme_path, project_details)


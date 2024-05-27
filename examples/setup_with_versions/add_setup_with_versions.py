import torch
import numpy
import matplotlib
import readme_ation

project_folder_path = "./examples/setup_with_versions/"

# Get the .py file names in the project folder
files_in_examples_folder = readme_ation.find_all_py_files(project_folder_path)

# Define the path to the README.md file in the current file's directory
readme_path = project_folder_path + "README.md"

readme_ation.add_setup_with_versions(files_in_examples_folder, readme_path)
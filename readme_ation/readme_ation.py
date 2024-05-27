import subprocess
import sys
import re
import ast
import os
import shutil
import importlib.metadata

# List of standard library modules to ignore
IGNORED_LIB_MODULES = {'os', 'enum', 'random', 'readme_version_logger'}

def find_all_py_files(directory):
    py_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                py_files.append(os.path.join(root, file))
    return py_files

def open_or_create_readme(readme_path):
    if os.path.exists(readme_path):
        with open(readme_path, 'r') as file:
            return file.read()
    else:
        create_readme = input(f"{readme_path} does not exist. Do you want to create it? (yes/no): ").strip().lower()
        if create_readme in {'yes', 'y'}:
            print(f"Creating {readme_path}")
            return ""
        else:
            print("README.md creation aborted by user.")
            return None

def add_setup_with_versions(file_paths, readme_path):
    # Handle case where README.md does not exist
    readme_content = open_or_create_readme(readme_path)
    if readme_content is None:
        return

    python_version = _get_python_version()
    installed_packages = _get_installed_packages()
    imported_packages = _get_imported_packages(file_paths)
    specific_versions = _get_specific_packages_versions(imported_packages, installed_packages)

    # Define the new setup and run instructions
    packages_with_versions_list = [f"{pkg}={ver}" if ver else f"{pkg}" for pkg, ver in specific_versions.items()]
    packages_with_versions_list.sort()
    packages_with_versions_string = ', '.join(packages_with_versions_list)

    new_setup_instructions = f"""
## Setup and Run Instructions
NOTE: This section is autogenerated by {os.path.basename(__file__)}, manual updates will be overwritten

This will guide you through the process of setting up a Mamba environment and running the provided Python code to see it in action. It uses the last known working versions of Python and packages used.

### Prerequisites

Ensure you have [Mamba](https://mamba.readthedocs.io/en/latest/installation.html) installed on your system. Mamba is a fast, cross-platform package manager.

### Steps

1. **Create a Mamba Environment**
   
   Open your terminal and execute the following commands:

   ```bash
   mamba create -n myenv python={python_version} -y
   mamba activate myenv

2. **Install Necessary Packages**

    ```bash
    # Install each with mamba and fall back to pip if necessary
    for pkg in {packages_with_versions_string}; do mamba install $pkg -y || pip install $pkg; done

3. **Run the Script**

    Ensure you are in your project directory and run the file you added the readme-ation code to and run:

    ```bash
    python [FILE_NAME]

    Or click 'run' in your IDE of choice.

    <!-- END SETUP AND RUN INSTRUCTIONS -->
"""

    # Replace or append the setup instructions
    setup_instructions_marker = "## Setup and Run Instructions"
    setup_instructions_closing_marker = "<!-- END SETUP AND RUN INSTRUCTIONS -->"
    if setup_instructions_marker in readme_content:
        setup_instructions_pattern = re.compile(rf"{re.escape(setup_instructions_marker)}.*?{re.escape(setup_instructions_closing_marker)}", re.DOTALL)
        readme_content = setup_instructions_pattern.sub(new_setup_instructions, readme_content)
    else:
        readme_content += '\n' + new_setup_instructions

    with open(readme_path, 'w') as file:
        file.write(readme_content)


import re

def add_project_description(readme_path, project_details):
    readme_content = open_or_create_readme(readme_path)
    if readme_content is None:
        return

    # Define the section template with closing key
    section_template = f"""
## Neural Network from Scratch
NOTE: This section is autogenerated by readme_ation.py, manual updates will be overwritten

### Overview
{project_details['overview']}

### Motivation
{project_details['motivation']}

### Technologies Used
{project_details['technologies']}

### Approach
{project_details['approach']}

### Challenges and Learnings
{project_details['challenges']}

### Key Takeaways
{project_details['key_takeaways']}

### Acknowledgments
{project_details['acknowledgments']}

<!-- END OF PROJECT DETAILS -->
"""
    # Read the current contents of the README.md file
    try:
        with open(readme_path, 'r') as file:
            readme_contents = file.read()
    except FileNotFoundError:
        readme_contents = ""

    # Define the section regex with closing key
    section_regex = re.compile(r"## Neural Network from Scratch.*?<!-- END OF PROJECT DETAILS -->", re.DOTALL)

    # Check if the section already exists
    match = section_regex.search(readme_contents)

    if match:
        # If the section exists, replace it
        updated_readme_contents = readme_contents[:match.start()] + section_template + readme_contents[match.end():]
    else:
        # If the section does not exist, add it to the end
        updated_readme_contents = readme_contents + section_template

    # Write the updated contents back to the README.md file
    with open(readme_path, 'w') as file:
        file.write(updated_readme_contents)


def _get_python_version():
    return sys.version.split()[0]

def _run_subprocess(command):
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print(f"Error running command {' '.join(command)}: {result.stderr}")
            return []
        return result.stdout.splitlines()
    except Exception as e:
        print(f"Exception running command {' '.join(command)}: {e}")
        return []

def _get_installed_packages():
    packages = {}

    # Check if mamba is available
    if shutil.which('mamba'):
        # Get packages from mamba
        mamba_lines = _run_subprocess(['mamba', 'list'])
        for line in mamba_lines:
            if line.startswith('#'):
                continue
            parts = re.split(r'\s+', line)
            if len(parts) >= 2:
                package = parts[0]
                version = parts[1]
                packages[package] = version

    # Get packages from pip
    pip_lines = _run_subprocess([sys.executable, '-m', 'pip', 'freeze'])
    for line in pip_lines:
        if '==' in line:
            pkg, version = line.split('==')
            if pkg not in packages:  # Do not overwrite mamba-installed packages
                packages[pkg] = version

    return packages

def _get_imported_packages(script_paths):
    imports = set()
    for script_path in script_paths:
        with open(script_path, 'r') as file:
            tree = ast.parse(file.read(), filename=script_path)
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name.split('.')[0])
            elif isinstance(node, ast.ImportFrom):
                imports.add(node.module.split('.')[0])
    return list(imports)

def _get_specific_packages_versions(imported_packages, installed_packages):
    specific_versions = {}
    for package in imported_packages:
        if package in IGNORED_LIB_MODULES:
            continue
        if package in installed_packages:
            specific_versions[package] = installed_packages[package]
        else:
            try:
                version = importlib.metadata.version(package)
                specific_versions[package] = f"{version}"
            except importlib.metadata.PackageNotFoundError:
                specific_versions[package] = ""
    return specific_versions
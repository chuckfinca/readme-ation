import re
import readme_ation
from readme_ation.utils import get_python_version, open_or_create_readme, check_for_notebook, _get_repo_name
import pkg_vers

note_string = f"NOTE: The following section is autogenerated by {readme_ation.__name__}, manual updates will be overwritten"
# - i need to update the readme with the cli stuff
# - add git clone info to setup
def add_setup_with_versions(readme_path, file_paths, repo_url=None):
    readme_content = open_or_create_readme(readme_path)
    python_version = get_python_version()
    specific_versions = pkg_vers.get_pkg_vers(file_paths, include_pkg_vers=True)

    contains_notebook = check_for_notebook(file_paths)

    environment_name = "[ENVIRONMENT_NAME]"
    notebook_file = "[YOUR_NOTEBOOK_FILE_NAME]"

    supplemental_setup_instructions = ""
    if contains_notebook:
        specific_versions['notebook'] = ""
        supplemental_setup_instructions += f"\n\n### Running Jupyter Notebook\n\nTo start the Jupyter Notebook and run the file, use the following commands:\n\n```sh\n# Activate the environment\nmamba activate {environment_name}\n\n# Start Jupyter Notebook\njupyter notebook {notebook_file}\n```"

    packages_with_versions_list = [f"{pkg}=={ver}" if ver else f"{pkg}" for pkg, ver in specific_versions.items()]
    packages_with_versions_list.sort()
    packages_with_versions_string = ' '.join(packages_with_versions_list)

    setup_instructions_marker = note_string + "\n## Setup Instructions"
    setup_instructions_closing_marker = "<!-- END SETUP AND RUN INSTRUCTIONS -->"
    
    clone_instructions = ""
    if repo_url:
        repo_name = get_repo_name(repo_url)
        clone_instructions = f"""
### Clone the Repository

Open your terminal and execute the following commands:

```sh
git clone {repo_url}
cd {repo_name}
```

"""

    new_setup_instructions = f"""{setup_instructions_marker}

This will guide you through the process of setting up a Mamba environment and running the provided Python code to see it in action. It uses the last known working versions of Python and packages used.

### Prerequisites

Ensure you have {"[Git](https://git-scm.com/downloads) and " if repo_url else ""}[Mamba](https://mamba.readthedocs.io/en/latest/installation.html) installed on your system. Mamba is a fast, cross-platform package manager.

### Steps
{clone_instructions}
### Create a Mamba Environment
   
Execute the following commands:

```sh
mamba create -n {environment_name} python={python_version} -y
mamba activate {environment_name}
```

### Install Necessary Packages

```sh
# Ensure that pkg-vers is installed
pip install pkg-vers

# Use pkg-vers to install dependency with mamba. Fall back to pip if necessary.
python -m pkg_vers install_packages {packages_with_versions_string}
```

### Usage

Ensure you are in your project directory.

Open the project in your IDE of choice.{supplemental_setup_instructions}

{setup_instructions_closing_marker}"""

    if setup_instructions_marker in readme_content:
        setup_instructions_pattern = re.compile(rf"{re.escape(setup_instructions_marker)}.*?{re.escape(setup_instructions_closing_marker)}", re.DOTALL)
        readme_content = setup_instructions_pattern.sub(new_setup_instructions, readme_content)
    else:
        readme_content += '\n' + new_setup_instructions

    with open(readme_path, 'w') as file:
        file.write(readme_content)

def add_project_description(readme_path, project_details):
    # Define markers
    section_start_marker = note_string + f"\n## Project: "
    end_marker = "<!-- END OF PROJECT DETAILS -->"

    # Create the new section
    new_section = f"""{section_start_marker} {project_details['title']}
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
{end_marker}
"""

    # Read the existing content
    try:
        with open(readme_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        lines = []

    # Find the start and end of the existing section
    start_index = None
    end_index = None
    for i, line in enumerate(lines):
        if line.strip() == section_start_marker:
            start_index = i
        elif line.strip() == end_marker and start_index is not None:
            end_index = i
            break

    # Update or append the section
    if start_index is not None and end_index is not None:
        # Replace the existing section
        lines[start_index:end_index+1] = new_section.splitlines(True)
    else:
        # Append the new section
        lines.extend(['\n'] + new_section.splitlines(True))

    # Write the updated content back to the file
    with open(readme_path, 'w') as file:
        file.writelines(lines)

    print(f"Updated {readme_path}")
    print("Section replaced" if start_index is not None else "New section appended")
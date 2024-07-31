## Overview
`readme-ation` automates the generation of a `README.md` file with setup and run instructions tailored for your Python project. By analyzing your project's Python files, it identifies imported packages, determines their versions, and updates your README with precise environment setup instructions. Additionally, it allows you to seamlessly add comprehensive project descriptions.

## Features
- **Automated README Generation**: Scans Python files to identify imported packages and their versions, generating environment setup instructions for a Mamba environment.
- **Project Description Section**: Enhances your README with detailed project information, including an overview, motivation, technologies used, approach, challenges, key takeaways, and acknowledgments.

## Command Line Usage

You can use `readme-ation` directly from the command line:

1. **Add Setup Instructions with Versions**:
   To add setup instructions for all Python files in the current directory:
   ```sh
   python -m readme_ation add_setup_with_versions README.md .
   ```
   This command will analyze all Python files in the current directory, identify their dependencies and versions, and update the README.md file with setup instructions.

   Or for specific files:
   ```sh
   python -m readme_ation add_setup_with_versions README.md file1.py file2.py
   ```

2. **Add Project Description**:
   ```sh
   python -m readme_ation add_project_description README.md '{"title": "Your Title", "overview": "Your overview", "motivation": "Your motivation", "technologies": "Technologies used", "approach": "Your approach", "challenges": "Challenges faced", "key_takeaways": "Key takeaways", "acknowledgments": "Acknowledgments"}'
   ```
   Note: The project details must be provided as a valid JSON string.

   This command will add a detailed project description to your README.md file based on the provided JSON string.

## Python Script Usage

You can also use `readme-ation` in your Python scripts:

1. **Generate Setup Instructions**:
    ```python
    from readme_ation import find_all_py_files, add_setup_with_versions

    file_paths = find_all_py_files('your_project_directory')
    add_setup_with_versions('README.md', file_paths)
    ```

2. **Add Project Description**:
    ```python
    from readme_ation import add_project_description

    project_details = {
        'title': 'Your Title here.',
        'overview': 'Your project overview here.',
        'motivation': 'The motivation behind your project.',
        'technologies': 'Technologies and tools used in your project.',
        'approach': 'Your approach to solving the problem.',
        'challenges': 'Challenges faced during the project.',
        'key_takeaways': 'Key takeaways and learnings from the project.',
        'acknowledgments': 'Acknowledgments and credits.'
    }

    add_project_description('README.md', project_details)
    ```

## Contributing
Please email me at chuckfinca@gmail.com if you would like to contribute.

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/chuckfinca/readme-ation/blob/main/LICENSE.txt) file for details.
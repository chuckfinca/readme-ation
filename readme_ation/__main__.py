import argparse
import json
from readme_ation.generator import add_project_description
from readme_ation.generator import add_setup_with_versions

def main():
    parser = argparse.ArgumentParser(description='Package Manager CLI')
    subparsers = parser.add_subparsers(dest='command')

    # Parser for 'add_project_description'
    add_project_description_parser = subparsers.add_parser('add_project_description', help='Appends a detailed project description to a README file')
    add_project_description_parser.add_argument('readme_path', help='Path to the README.md file to create or modify.')
    add_project_description_parser.add_argument('project_details', help='JSON string containing project details')

    # Parser for 'add_setup_with_versions'
    add_setup_with_versions_parser = subparsers.add_parser('add_setup_with_versions', help='Updates README file with setup and run instructions, including package versions.')
    add_setup_with_versions_parser.add_argument('readme_path', help='Path to the README.md file to create or modify.')
    add_setup_with_versions_parser.add_argument('file_paths', nargs='+', help='File paths, list of file paths, or folder path to search for dependencies')

    args = parser.parse_args()

    if args.command == 'add_project_description':
        try:
            project_details = json.loads(args.project_details)
            add_project_description(args.readme_path, project_details)
        except json.JSONDecodeError:
            print("Error: Invalid JSON format in project_details")
    elif args.command == 'add_setup_with_versions':
        add_setup_with_versions(args.readme_path, args.file_paths)

if __name__ == "__main__":
    main()
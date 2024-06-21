import shutil
import unittest
import json
import os
import tempfile
from unittest.mock import patch
from readme_ation.generator import add_project_description, add_setup_with_versions

class TestReadmeAtion(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        self.readme_path = os.path.join(self.test_dir, 'README.md')
        # Create an empty README file
        open(self.readme_path, 'w').close()

    def tearDown(self):
        # Remove the directory and all its contents after the test
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_add_project_description(self):
        project_details = {
            "title": "Test Title",
            "overview": "Test Overview",
            "motivation": "Test Motivation",
            "technologies": "Test Technologies",
            "approach": "Test Approach",
            "challenges": "Test Challenges",
            "key_takeaways": "Test Key Takeaways",
            "acknowledgments": "Test Acknowledgments"
        }
        
        add_project_description(self.readme_path, project_details)
        
        with open(self.readme_path, 'r') as f:
            content = f.read()
        
        for key, value in project_details.items():
            self.assertIn(value, content)

    def test_add_setup_with_versions(self):
        # Create a dummy Python file with some imports
        dummy_file_path = os.path.join(self.test_dir, 'dummy_file.py')
        with open(dummy_file_path, 'w') as f:
            f.write("import numpy\nimport pandas")
        
        add_setup_with_versions(self.readme_path, [dummy_file_path])
        
        with open(self.readme_path, 'r') as f:
            content = f.read()
        
        self.assertIn('numpy', content)
        self.assertIn('pandas', content)

    def test_main_add_project_description(self):
        project_details = {
            "title": "Test Title",
            "overview": "Test Overview",
            "motivation": "Test Motivation",
            "technologies": "Test Technologies",
            "approach": "Test Approach",
            "challenges": "Test Challenges",
            "key_takeaways": "Test Key Takeaways",
            "acknowledgments": "Test Acknowledgments"
        }
        
        with patch('sys.argv', ['readme_ation', 'add_project_description', self.readme_path, json.dumps(project_details)]):
            from readme_ation.__main__ import main
            main()
        
        with open(self.readme_path, 'r') as f:
            content = f.read()
        
        for value in project_details.values():
            self.assertIn(value, content)

    def test_main_add_setup_with_versions(self):
        # Create a dummy Python file with some imports
        dummy_file_path = os.path.join(self.test_dir, 'dummy_file.py')
        with open(dummy_file_path, 'w') as f:
            f.write("import numpy\nimport pandas")
        
        with patch('sys.argv', ['readme_ation', 'add_setup_with_versions', self.readme_path, dummy_file_path]):
            from readme_ation.__main__ import main
            main()
        
        with open(self.readme_path, 'r') as f:
            content = f.read()
        
        self.assertIn('numpy', content)
        self.assertIn('pandas', content)

if __name__ == '__main__':
    unittest.main()
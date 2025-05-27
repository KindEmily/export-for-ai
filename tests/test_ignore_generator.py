import unittest
import os
import tempfile
import shutil
from src.export_for_ai.ignore_generator import generate_exportignore, PROJECT_TYPES, GENERAL_SUPPLEMENTAL_IGNORES, GENERIC_IGNORES_FULL

class TestIgnoreGenerator(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for each test
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)

    def _create_mock_file(self, file_name):
        """Helper to create a mock file in the test directory."""
        with open(os.path.join(self.test_dir, file_name), 'w') as f:
            f.write("mock content")

    def test_detect_python_project(self):
        self._create_mock_file("requirements.txt")
        output = generate_exportignore(self.test_dir)
        self.assertIn("# Python project detected", output)
        # Check for a key Python-specific pattern
        self.assertIn("__pycache__/", output)
        # Check for a key general supplemental pattern
        self.assertIn(".git/", output)
        self.assertIn(".vscode/", output)

    def test_detect_nodejs_project(self):
        self._create_mock_file("package.json")
        output = generate_exportignore(self.test_dir)
        self.assertIn("# Node.js project detected", output)
        self.assertIn("node_modules/", output)
        self.assertIn(".git/", output) # General supplemental

    def test_detect_csharp_project_csproj(self):
        self._create_mock_file("myproject.csproj")
        output = generate_exportignore(self.test_dir)
        self.assertIn("# C# (.NET) project detected", output)
        self.assertIn("[Bb]in/", output)
        self.assertIn(".git/", output) # General supplemental

    def test_detect_csharp_project_sln(self):
        self._create_mock_file("mysolution.sln")
        output = generate_exportignore(self.test_dir)
        self.assertIn("# C# (.NET) project detected", output)
        self.assertIn("[Oo]bj/", output) # Another C# specific pattern
        self.assertIn(".git/", output) # General supplemental
    
    def test_detect_generic_project_empty_dir(self):
        output = generate_exportignore(self.test_dir)
        self.assertIn("# No specific project type detected, using generic ignores.", output)
        # Check for a pattern that is in GENERIC_IGNORES_FULL but not in GENERAL_SUPPLEMENTAL_IGNORES
        self.assertIn(".hg/", output) 
        self.assertIn("Thumbs.db", output)
        # Check for a pattern that is also in GENERAL_SUPPLEMENTAL_IGNORES
        self.assertIn(".git/", output)


    def test_detect_generic_project_unrelated_files(self):
        self._create_mock_file("README.md")
        self._create_mock_file("image.jpg")
        output = generate_exportignore(self.test_dir)
        self.assertIn("# No specific project type detected, using generic ignores.", output)
        self.assertIn("*.bak", output) # From GENERIC_IGNORES_FULL
        self.assertIn(".vscode/", output) # From GENERIC_IGNORES_FULL and also GENERAL_SUPPLEMENTAL_IGNORES

    def test_pattern_generation_python(self):
        self._create_mock_file("setup.py") # Another Python fingerprint
        output = generate_exportignore(self.test_dir)
        self.assertIn("# Python project detected", output)
        for pattern in PROJECT_TYPES["Python"]["ignores"]:
            self.assertIn(pattern, output)
        for pattern in GENERAL_SUPPLEMENTAL_IGNORES:
            self.assertIn(pattern, output)
        # Ensure something from GENERIC_IGNORES_FULL not in GENERAL_SUPPLEMENTAL_IGNORES is NOT there
        self.assertNotIn(".hg/", output) 

    def test_pattern_generation_nodejs(self):
        self._create_mock_file("yarn.lock") # Another Node.js fingerprint
        output = generate_exportignore(self.test_dir)
        self.assertIn("# Node.js project detected", output)
        for pattern in PROJECT_TYPES["Node.js"]["ignores"]:
            self.assertIn(pattern, output)
        for pattern in GENERAL_SUPPLEMENTAL_IGNORES:
            self.assertIn(pattern, output)
        self.assertNotIn("Thumbs.db", output)

    def test_pattern_generation_csharp(self):
        self._create_mock_file("MyProject.csproj")
        output = generate_exportignore(self.test_dir)
        self.assertIn("# C# (.NET) project detected", output)
        for pattern in PROJECT_TYPES["C# (.NET)"]["ignores"]:
            self.assertIn(pattern, output)
        for pattern in GENERAL_SUPPLEMENTAL_IGNORES:
            self.assertIn(pattern, output)
        self.assertNotIn("temp/", output)

    def test_pattern_generation_generic(self):
        output = generate_exportignore(self.test_dir) # Empty dir
        self.assertIn("# No specific project type detected, using generic ignores.", output)
        for pattern in GENERIC_IGNORES_FULL:
            self.assertIn(pattern, output)
        # Ensure no project-specific patterns are present
        self.assertNotIn("__pycache__/", output)
        self.assertNotIn("node_modules/", output)
        self.assertNotIn("[Bb]in/", output)

    def test_non_existent_directory(self):
        non_existent_path = os.path.join(self.test_dir, "non_existent_subdir")
        # Do not create non_existent_subdir
        output = generate_exportignore(non_existent_path)
        self.assertIn("# No specific project type detected, using generic ignores.", output)
        for pattern in GENERIC_IGNORES_FULL:
            self.assertIn(pattern, output)

if __name__ == '__main__':
    unittest.main()

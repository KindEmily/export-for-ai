import unittest
import os
import tempfile
import shutil
from pathspec import PathSpec
from src.export_for_ai.ignore_parser import load_template_patterns, parse_ignore_file

# Assuming the script is run from the project root, so paths to actual templates are correct.
# src/export_for_ai/ignore_templates/default.template
# src/export_for_ai/ignore_templates/light.template

class TestIgnoreParser(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        # Path to the ignore_templates directory, assuming tests are run from project root
        # or src is in PYTHONPATH
        self.templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                          '..', 'src', 'export_for_ai', 'ignore_templates')
        if not os.path.exists(self.templates_dir):
             # Fallback if running from tests/ directory directly
            self.templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                          '../src/export_for_ai/ignore_templates')


    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_load_template_default(self):
        patterns = load_template_patterns("default")
        self.assertTrue(len(patterns) > 0)
        self.assertIn("__pycache__/", patterns) # A common pattern from default
        self.assertIn(".git/", patterns)       # Another common one
        self.assertIn("*.md", patterns)        # From default template
        self.assertNotIn("# Light template additions", patterns) # Comment from light
        
    def test_load_template_light(self):
        patterns = load_template_patterns("light")
        self.assertTrue(len(patterns) > 0)
        self.assertIn("__pycache__/", patterns) # From default part of light
        self.assertIn("docs/", patterns)        # Specific to light
        self.assertIn("tests/", patterns)       # Specific to light
        self.assertIn("*.md", patterns)         # Both have it, should be present
        # Check if a comment from the light template is NOT loaded
        self.assertNotIn("# Light template additions", patterns)

    def test_load_non_existent_template(self):
        patterns = load_template_patterns("nonexistent_template_blah_blah")
        self.assertEqual(patterns, [])

    def test_load_dummy_template_with_comments_and_empty_lines(self):
        dummy_template_content = (
            "# This is a comment\n"
            "pattern1/\n"
            "\n"
            "pattern2 # Inline comment (PathSpec might handle this differently, but our parser strips full line comments)\n"
            "  pattern3  \n" # Should be stripped of whitespace
        )
        dummy_template_path = os.path.join(self.templates_dir, "dummy.template")
        
        # Create the dummy template file
        # For this test, we'll place it where load_template_patterns expects it.
        # This requires that `ignore_templates` directory exists relative to ignore_parser.py
        # We will mock the path construction or create it within the actual templates folder for this test
        
        # Simpler: create it in the test_dir and mock load_template_patterns's path finding logic
        # or temporarily adjust where load_template_patterns looks.
        # For now, let's assume we can write to the actual template dir for the test.
        # This is not ideal for unit tests as it modifies source structure.
        # A better approach would be to mock open() or pass base_dir to load_template_patterns.
        
        # Let's create the dummy template file within the *actual* templates directory
        # This requires `src/export_for_ai/ignore_templates` to be writable by the test runner
        # This is generally bad practice for unit tests.
        # The `load_template_patterns` function has `base_dir = os.path.dirname(os.path.abspath(__file__))`
        # in `ignore_parser.py`. So it will always look in `src/export_for_ai/ignore_templates`.
        
        created_dummy_in_src = False
        try:
            if not os.path.exists(self.templates_dir):
                 os.makedirs(self.templates_dir) # Should exist from previous subtask
            
            with open(dummy_template_path, 'w') as f:
                f.write(dummy_template_content)
            created_dummy_in_src = True

            patterns = load_template_patterns("dummy")
            self.assertIn("pattern1/", patterns)
            self.assertIn("pattern2", patterns) # Assuming inline comments are not handled by our strip, PathSpec handles them.
                                               # The current load_template_patterns only strips full line comments.
            self.assertIn("pattern3", patterns)
            self.assertEqual(len(patterns), 3)

        finally:
            if created_dummy_in_src and os.path.exists(dummy_template_path):
                os.remove(dummy_template_path)


    def _create_mock_exportignore(self, patterns_list):
        with open(os.path.join(self.test_dir, ".exportignore"), 'w') as f:
            f.write("\n".join(patterns_list))

    def test_parse_ignore_file_default_template_no_local(self):
        # No .exportignore in self.test_dir
        spec = parse_ignore_file(self.test_dir, template_name="default")
        self.assertIsInstance(spec, PathSpec)
        # Check if it matches a known pattern from default.template
        self.assertTrue(spec.match_file("__pycache__/somefile.pyc"))
        self.assertTrue(spec.match_file(".git/config"))
        # Check a file that should NOT be ignored by default
        self.assertFalse(spec.match_file("src/main.py"))


    def test_parse_ignore_file_light_template_no_local(self):
        spec = parse_ignore_file(self.test_dir, template_name="light")
        self.assertIsInstance(spec, PathSpec)
        self.assertTrue(spec.match_file("docs/README.md")) # specific to light
        self.assertTrue(spec.match_file("tests/test_app.py")) # specific to light
        self.assertTrue(spec.match_file("*.md")) # from light template
        self.assertFalse(spec.match_file("src/main.py"))


    def test_parse_ignore_file_default_template_with_local(self):
        local_patterns = ["my_local_folder/", "*.local_ext"]
        self._create_mock_exportignore(local_patterns)
        
        spec = parse_ignore_file(self.test_dir, template_name="default")
        self.assertTrue(spec.match_file("__pycache__/some.pyc")) # From default
        self.assertTrue(spec.match_file("my_local_folder/file.txt")) # From local
        self.assertTrue(spec.match_file("another.local_ext")) # From local
        self.assertFalse(spec.match_file("src/app.py"))


    def test_parse_ignore_file_light_template_with_local(self):
        local_patterns = ["custom_reports/", "data.csv"]
        self._create_mock_exportignore(local_patterns)

        spec = parse_ignore_file(self.test_dir, template_name="light")
        self.assertTrue(spec.match_file("docs/guide.html")) # From light
        self.assertTrue(spec.match_file("custom_reports/report1.pdf")) # From local
        self.assertTrue(spec.match_file("data.csv")) # From local
        self.assertFalse(spec.match_file("src/app.py"))

    def test_parse_ignore_file_non_existent_template_with_local(self):
        local_patterns = ["only_this_folder/", "*.specific_only"]
        self._create_mock_exportignore(local_patterns)

        spec = parse_ignore_file(self.test_dir, template_name="nonexistent_template_xyz")
        # Should only use local patterns as template loading returns empty list
        self.assertTrue(spec.match_file("only_this_folder/file.txt"))
        self.assertTrue(spec.match_file("test.specific_only"))
        # Patterns from default or light should not be present
        self.assertFalse(spec.match_file("__pycache__/some.pyc"))
        self.assertFalse(spec.match_file("docs/guide.html"))
        self.assertFalse(spec.match_file("src/app.py")) # Should not be ignored

    def test_parse_ignore_file_empty_local_exportignore(self):
        self._create_mock_exportignore(["# This is a comment only", ""]) # Empty or comments only
        spec = parse_ignore_file(self.test_dir, template_name="default")
        # Should behave as if no local .exportignore, i.e., only default patterns
        self.assertTrue(spec.match_file(".vscode/settings.json")) # From default
        self.assertFalse(spec.match_file("my_local_folder/file.txt")) # No local patterns added

    def test_parse_ignore_file_no_template_no_local(self):
        # This tests the case where template loading fails AND no .exportignore exists
        # parse_ignore_file calls load_template_patterns("bad_template_name")
        # which returns [], and there's no local .exportignore.
        # The spec should be empty and not match anything (i.e., include everything).
        spec = parse_ignore_file(self.test_dir, template_name="non_existent_template_for_sure")
        self.assertIsInstance(spec, PathSpec)
        self.assertFalse(spec.match_file("anything.txt"))
        self.assertFalse(spec.match_file("__pycache__/some.pyc"))
        # Check if the patterns list in spec is indeed empty
        self.assertEqual(len(spec.patterns), 0)


if __name__ == '__main__':
    unittest.main()

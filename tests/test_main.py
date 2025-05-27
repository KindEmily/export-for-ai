import unittest
import sys
import os
from unittest.mock import patch
from src.export_for_ai.main import parse_arguments

# To ensure parse_arguments can resolve abspath, we might need to be in a dir
# or ensure the paths given are not problematic. For these tests, using relative
# paths like 'some/path' and letting abspath work on them should be fine.

class TestMainArgParsing(unittest.TestCase):

    def _get_abs_path(self, p):
        # Helper to ensure consistent path comparison, especially on Windows
        return os.path.abspath(p)

    @patch('sys.argv')
    def test_parse_generate_ignore_command(self, mock_argv):
        mock_argv[:] = ['export-for-ai', 'generate-ignore', 'my_project_dir']
        command, directory_path, template_name = parse_arguments()
        self.assertEqual(command, 'generate-ignore')
        self.assertEqual(directory_path, self._get_abs_path('my_project_dir'))
        self.assertEqual(template_name, 'default') # Default template name, though not used by generate-ignore

    @patch('sys.argv')
    def test_parse_export_command_simple(self, mock_argv):
        mock_argv[:] = ['export-for-ai', 'another/path']
        command, directory_path, template_name = parse_arguments()
        self.assertEqual(command, 'export')
        self.assertEqual(directory_path, self._get_abs_path('another/path'))
        self.assertEqual(template_name, 'default') # Default template for export

    @patch('sys.argv')
    def test_parse_export_command_with_template_short(self, mock_argv):
        mock_argv[:] = ['export-for-ai', '-t', 'light', 'project/folder']
        command, directory_path, template_name = parse_arguments()
        self.assertEqual(command, 'export')
        self.assertEqual(directory_path, self._get_abs_path('project/folder'))
        self.assertEqual(template_name, 'light')

    @patch('sys.argv')
    def test_parse_export_command_with_template_long(self, mock_argv):
        mock_argv[:] = ['export-for-ai', '--template', 'custom_template', 'some/other/dir']
        command, directory_path, template_name = parse_arguments()
        self.assertEqual(command, 'export')
        self.assertEqual(directory_path, self._get_abs_path('some/other/dir'))
        self.assertEqual(template_name, 'custom_template')

    @patch('sys.argv')
    def test_parse_export_command_path_first_then_template(self, mock_argv):
        # parse_arguments in main.py expects path first for export if template is specified
        mock_argv[:] = ['export-for-ai', 'my_proj', '-t', 'special']
        command, directory_path, template_name = parse_arguments()
        self.assertEqual(command, 'export')
        self.assertEqual(directory_path, self._get_abs_path('my_proj'))
        self.assertEqual(template_name, 'special')

    @patch('sys.argv')
    def test_parse_invalid_generate_ignore_no_path(self, mock_argv):
        mock_argv[:] = ['export-for-ai', 'generate-ignore']
        # Assuming parse_arguments logs an error and returns (None, None, None)
        with patch('logging.error') as mock_log_error:
            command, directory_path, template_name = parse_arguments()
            self.assertIsNone(command)
            self.assertIsNone(directory_path)
            self.assertIsNone(template_name) # template_name is None on error
            mock_log_error.assert_called()

    @patch('sys.argv')
    def test_parse_invalid_export_no_path(self, mock_argv):
        mock_argv[:] = ['export-for-ai'] # No command, no path
        with patch('logging.error') as mock_log_error:
            command, directory_path, template_name = parse_arguments()
            self.assertIsNone(command)
            self.assertIsNone(directory_path)
            self.assertIsNone(template_name)
            mock_log_error.assert_called()

    @patch('sys.argv')
    def test_parse_invalid_template_option_no_name(self, mock_argv):
        mock_argv[:] = ['export-for-ai', 'my_project_path', '-t'] # Missing template name
        with patch('logging.error') as mock_log_error:
            command, directory_path, template_name = parse_arguments()
            self.assertIsNone(command)
            self.assertIsNone(directory_path)
            self.assertIsNone(template_name)
            mock_log_error.assert_called()
            
    @patch('sys.argv')
    def test_parse_unknown_option_for_export(self, mock_argv):
        mock_argv[:] = ['export-for-ai', 'my_project_path', '--unknown-option']
        with patch('logging.error') as mock_log_error:
            command, directory_path, template_name = parse_arguments()
            self.assertIsNone(command)
            self.assertIsNone(directory_path)
            self.assertIsNone(template_name)
            mock_log_error.assert_called()

    @patch('sys.argv')
    def test_parse_path_looks_like_option(self, mock_argv):
        # Test if a path like "-myfolder" is treated as an error if it's where a path is expected
        mock_argv[:] = ['export-for-ai', '-myfolder', '-t', 'light']
        with patch('logging.error') as mock_log_error:
            command, directory_path, template_name = parse_arguments()
            self.assertIsNone(command)
            self.assertIsNone(directory_path)
            self.assertIsNone(template_name)
            mock_log_error.assert_called_with(f"Invalid directory path: {self._get_abs_path('-myfolder')}. Path cannot start with '-'.")


    @patch('sys.argv')
    def test_parse_export_command_with_template_path_containing_spaces(self, mock_argv):
        # This test case might depend on shell quoting, sys.argv should receive it as one item.
        path_with_spaces = "my project/folder with spaces"
        mock_argv[:] = ['export-for-ai', path_with_spaces, '--template', 'light']
        command, directory_path, template_name = parse_arguments()
        self.assertEqual(command, 'export')
        self.assertEqual(directory_path, self._get_abs_path(path_with_spaces))
        self.assertEqual(template_name, 'light')

    @patch('sys.argv')
    def test_parse_generate_ignore_path_containing_spaces(self, mock_argv):
        path_with_spaces = "my project/other folder"
        mock_argv[:] = ['export-for-ai', 'generate-ignore', path_with_spaces]
        command, directory_path, template_name = parse_arguments()
        self.assertEqual(command, 'generate-ignore')
        self.assertEqual(directory_path, self._get_abs_path(path_with_spaces))
        self.assertEqual(template_name, 'default') # Default

if __name__ == '__main__':
    unittest.main()

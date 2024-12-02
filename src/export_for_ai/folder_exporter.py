import logging
import os
import re

from .ignore_parser import parse_ignore_file, should_include_item


def minify_code(content):
    # Remove single-line comments
    content = re.sub(r"#.*", "", content)
    # Remove multi-line comments
    content = re.sub(r"\'\'\'[\s\S]*?\'\'\'|\"\"\"[\s\S]*?\"\"\"", "", content)
    # Remove excessive whitespace
    content = "\n".join(line.strip() for line in content.splitlines() if line.strip())
    return content


def export_folder_content(path):
    """
    Export the content of all included files in the folder.

    :param path: The root directory to export.
    :return: A string containing the exported content.
    """
    spec = parse_ignore_file(path)
    content = []
    for root, dirs, files in os.walk(path):
        # Compute relative path from the root directory
        rel_root = os.path.relpath(root, path)
        if rel_root == ".":
            rel_root = ""

        # Modify dirs in-place to skip ignored directories
        dirs[:] = [
            d for d in dirs if should_include_item(os.path.join(rel_root, d), spec)
        ]

        for dir_name in dirs:
            logging.debug(f"Including directory: {os.path.join(rel_root, dir_name)}")

        for file in files:
            rel_file_path = os.path.join(rel_root, file) if rel_root else file
            if should_include_item(rel_file_path, spec):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        file_content = f.read()
                        if file_content.strip():
                            content.append(f"# File: {rel_file_path}\n")
                            content.append("```\n")
                            content.append(file_content)
                            content.append("\n```\n\n")
                        else:
                            content.append(f"# File: {rel_file_path}\n")
                            content.append("`File is empty`\n\n")
                except UnicodeDecodeError as e:
                    # Handle binary files or files with encoding issues
                    logging.error(f"Error reading {rel_file_path}: {e}")
                    content.append(f"# File: {rel_file_path}\n")
                    content.append("`Binary or unreadable file`\n\n")
                except Exception as e:
                    content.append(f"Error reading {rel_file_path}: {str(e)}\n\n")
            else:
                logging.debug(f"Skipping file: {rel_file_path}")
    return "".join(content)

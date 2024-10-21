import os
import logging
from .ignore_parser import parse_ignore_file, should_include_item

def export_folder_content(path):
    """Export the content of all included files in the folder."""
    ignore_patterns = parse_ignore_file(path)
    content = []
    for root, dirs, files in os.walk(path):
        # Modify dirs in-place to skip ignored directories
        dirs_to_remove = []
        for dir_name in dirs:
            dir_path = os.path.relpath(os.path.join(root, dir_name), path)
            if not should_include_item(dir_path, ignore_patterns):
                dirs_to_remove.append(dir_name)
                logging.debug(f"Skipping directory: {dir_path}")
        for dir_name in dirs_to_remove:
            dirs.remove(dir_name)
        
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, path)
            if should_include_item(relative_path, ignore_patterns):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        file_content = f.read()
                        if file_content.strip():
                            content.append(f"# File: {relative_path}\n")
                            content.append("```\n")
                            content.append(file_content)
                            content.append("\n```\n\n")
                        else:
                            content.append(f"# File: {relative_path}\n")
                            content.append("`File is empty`\n\n")
                except Exception as e:
                    content.append(f"Error reading {relative_path}: {str(e)}\n\n")
            else:
                logging.debug(f"Skipping file: {relative_path}")
    return ''.join(content)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(export_folder_content(sys.argv[1]))
    else:
        print("Please provide a path as an argument.")

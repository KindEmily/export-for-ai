import os

def should_include_file(file_path):
    """Determine if a file should be included in the export."""
    excluded_extensions = {'.svg', '.css', '.gitignore', '.jpg', '.png', '.gif', '.git', '.gitignore'}
    _, ext = os.path.splitext(file_path)
    return ext.lower() not in excluded_extensions and not os.path.basename(file_path).startswith('.')

def export_folder_content(path):
    """Export the content of all included files in the folder."""
    content = []
    for root, _, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            if should_include_file(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content.append(f"File: {os.path.relpath(file_path, path)}\n")
                        content.append(f.read())
                        content.append("\n\n")
                except Exception as e:
                    content.append(f"Error reading {file_path}: {str(e)}\n\n")
    return ''.join(content)

if __name__ == "__main__":
    # This allows the module to be run standalone for testing
    import sys
    if len(sys.argv) > 1:
        print(export_folder_content(sys.argv[1]))
    else:
        print("Please provide a path as an argument.")

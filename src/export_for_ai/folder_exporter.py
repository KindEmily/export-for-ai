import os

def should_include_file(file_path):
    """Determine if a file should be included in the export."""
    excluded_extensions = {'.svg', '.css', '.jpg', '.png', '.git', '.gitignore', '.binder', '.otf', '.pyc', '.toml'}
    excluded_directories = {'.git', '__pycache__', '.vs'}
    _, ext = os.path.splitext(file_path)
    
    # Check if the file is within an excluded directory or starts with 'exported-from-'
    path_parts = file_path.split(os.sep)
    if any(part.startswith('exported-from-') or part in excluded_directories for part in path_parts):
        return False
    
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
                        file_content = f.read()
                        if file_content.strip():
                            content.append(f"# File: {os.path.relpath(file_path, path)}\n")
                            content.append("```\n")
                            content.append(file_content)
                            content.append("\n```\n\n")
                        else:
                            content.append(f"# File: {os.path.relpath(file_path, path)}\n")
                            content.append("`File is empty`\n\n")
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
import os
import logging
from .ignore_parser import parse_ignore_file, should_include_item

def visualize_folder_structure(path, root_path, ignore_patterns, prefix="", is_last=True):
    output = []
    basename = os.path.basename(path)
    relative_path = os.path.relpath(path, root_path)
    
    if os.path.isdir(path):
        if prefix == "":
            output.append(basename + "/")
        else:
            output.append(prefix + ("└── " if is_last else "├── ") + basename + "/")
        
        items = sorted(os.listdir(path))
        items = [item for item in items if should_include_item(os.path.join(relative_path, item), ignore_patterns)]
        
        for index, item in enumerate(items):
            item_path = os.path.join(path, item)
            is_last_item = index == len(items) - 1
            
            output.extend(
                visualize_folder_structure(
                    item_path,
                    root_path,
                    ignore_patterns,
                    prefix + ("    " if is_last else "│   "),
                    is_last_item
                )
            )
    else:
        output.append(prefix + ("└── " if is_last else "├── ") + basename)
    
    return output

def get_tree_structure(path):
    """Generate a string representation of the folder structure."""
    ignore_patterns = parse_ignore_file(path)
    tree = visualize_folder_structure(path, path, ignore_patterns)
    return "\n".join(tree)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(get_tree_structure(sys.argv[1]))
    else:
        print("Please provide a path as an argument.")
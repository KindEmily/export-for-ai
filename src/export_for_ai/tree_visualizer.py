import logging
import os
from anytree import Node, RenderTree
from export_for_ai.ignore_parser import parse_ignore_file, should_include_item

def build_tree(path, root_path, spec):
    """
    Recursively builds a tree structure using anytree based on the directory contents.
    
    :param path: Current directory path.
    :param root_path: Root directory path for relative calculations.
    :param spec: PathSpec object containing ignore patterns.
    :return: The root Node of the tree.
    """
    basename = os.path.basename(os.path.abspath(path))
    root_node = Node(basename + '/')
    
    def add_children(current_path, current_node):
        try:
            items = sorted(os.listdir(current_path))
        except PermissionError:
            logging.warning(f"Permission denied: {current_path}")
            return
        
        dirs = [item for item in items if os.path.isdir(os.path.join(current_path, item))]
        files = [item for item in items if os.path.isfile(os.path.join(current_path, item))]
        
        # Filter directories and files based on ignore patterns
        dirs = [d for d in dirs if should_include_item(os.path.relpath(os.path.join(current_path, d), root_path), spec)]
        files = [f for f in files if should_include_item(os.path.relpath(os.path.join(current_path, f), root_path), spec)]
        
        for d in dirs:
            dir_path = os.path.join(current_path, d)
            node = Node(d + '/', parent=current_node)
            add_children(dir_path, node)
        
        for f in files:
            Node(f, parent=current_node)
    
    add_children(path, root_node)
    return root_node

def get_tree_structure(path):
    """
    Generate a string representation of the folder structure.
    
    :param path: The root directory path.
    :return: A string representing the tree structure.
    """
    spec = parse_ignore_file(path)
    tree = build_tree(path, path, spec)
    tree_lines = []
    for pre, _, node in RenderTree(tree):
        tree_lines.append(pre + node.name)
    return "\n".join(tree_lines)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(get_tree_structure(sys.argv[1]))
    else:
        print("Please provide a path as an argument.")

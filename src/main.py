import sys
import os
import shlex

from export_for_ai.tree_visualizer import get_tree_structure

def main():
    if len(sys.argv) != 2:
        print("Usage: export-for-ai <directory_path>")
        sys.exit(1)
    
    # Use shlex.split to properly handle quoted arguments
    args = shlex.split(sys.argv[1])
    directory_path = args[0]
    
    # Normalize the path to handle potential issues with backslashes
    directory_path = os.path.normpath(directory_path)
    
    if not os.path.isdir(directory_path):
        print(f"Error: '{directory_path}' is not a valid directory")
        sys.exit(1)
    
    # Export the tree structure
    print("Exporting directory structure:")
    tree_structure = get_tree_structure(directory_path)
    print(tree_structure)
    
    # Optionally, save the tree structure to a file
    output_file = "directory_structure.txt"
    with open(output_file, "w") as f:
        f.write(tree_structure)
    print(f"\nTree structure exported to {output_file}")

if __name__ == "__main__":
    main()
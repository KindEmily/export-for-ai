import sys
import os
import logging
from typing import Optional

from export_for_ai.tree_visualizer import get_tree_structure

def setup_logging() -> None:
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def parse_arguments() -> Optional[str]:
    if len(sys.argv) != 2:
        logging.error("Usage: export-for-ai <directory_path>")
        return None
    
    return os.path.normpath(sys.argv[1])

def validate_directory(directory_path: str) -> bool:
    if not os.path.isdir(directory_path):
        logging.error(f"Error: '{directory_path}' is not a valid directory")
        return False
    return True

def export_tree_structure(directory_path: str) -> Optional[str]:
    try:
        logging.info("Exporting directory structure...")
        return get_tree_structure(directory_path)
    except Exception as e:
        logging.error(f"Error generating tree structure: {e}")
        return None

def save_tree_structure(tree_structure: str, output_file: str = "directory_structure.txt") -> bool:
    try:
        full_path = os.path.abspath(output_file)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(tree_structure)
        logging.info(f"Tree structure exported to {output_file} (full path: {full_path})")
        return True
    except IOError as e:
        logging.error(f"Error writing to file: {e}")
        return False

def main() -> None:
    setup_logging()
    
    directory_path = parse_arguments()
    if not directory_path:
        return

    if not validate_directory(directory_path):
        return

    tree_structure = export_tree_structure(directory_path)
    if not tree_structure:
        return

    print(tree_structure)

    if not save_tree_structure(tree_structure):
        return

if __name__ == "__main__":
    main()

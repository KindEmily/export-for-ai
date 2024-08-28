import sys
import os
import logging
from typing import Optional

from export_for_ai.tree_visualizer import get_tree_structure
from export_for_ai.folder_exporter import export_folder_content
from export_for_ai.readme_generator import create_readme

def setup_logging() -> None:
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def parse_arguments() -> Optional[str]:
    if len(sys.argv) != 2:
        logging.error("Usage: export-for-ai <directory_path>")
        return None

    return os.path.abspath(sys.argv[1])

def validate_directory(directory_path: str) -> bool:
    if not os.path.isdir(directory_path):
        logging.error(f"Error: '{directory_path}' is not a valid directory")
        return False
    return True

def get_folder_name(directory_path: str) -> str:
    return os.path.basename(os.path.abspath(directory_path))

def create_export_directory(directory_path: str) -> str:
    folder_name = get_folder_name(directory_path)
    export_dir_name = f"exported-from-{folder_name}"
    export_dir_path = os.path.join(directory_path, export_dir_name)
    
    try:
        os.makedirs(export_dir_path, exist_ok=True)
        logging.info(f"Created export directory: {export_dir_path}")
        return export_dir_path
    except OSError as e:
        logging.error(f"Error creating export directory: {e}")
        return ""

def export_tree_structure(directory_path: str) -> Optional[str]:
    try:
        logging.info("Exporting directory structure...")
        return get_tree_structure(directory_path)
    except Exception as e:
        logging.error(f"Error generating tree structure: {e}")
        return None

def save_content(content: str, output_file: str) -> bool:
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)
        logging.info(f"Content exported to {output_file}")
        return True
    except IOError as e:
        logging.error(f"Error writing to file: {e}")
        return False

def export_folder_contents(directory_path: str) -> Optional[str]:
    try:
        logging.info("Exporting folder contents...")
        return export_folder_content(directory_path)
    except Exception as e:
        logging.error(f"Error exporting folder contents: {e}")
        return None

def main() -> None:
    setup_logging()

    directory_path = parse_arguments()
    if not directory_path:
        return

    if not validate_directory(directory_path):
        return

    export_dir = create_export_directory(directory_path)
    if not export_dir:
        return

    tree_structure = export_tree_structure(directory_path)
    if tree_structure:
        if not save_content(tree_structure, os.path.join(export_dir, "project_structure.txt")):
            return

    folder_contents = export_folder_contents(directory_path)
    if folder_contents:
        if not save_content(folder_contents, os.path.join(export_dir, "project_contents.txt")):
            return

    readme_content = create_readme(get_folder_name(directory_path))
    if not save_content(readme_content, os.path.join(export_dir, "README.md")):
        return

    logging.info(f"Export completed successfully. Files saved in {export_dir}")

if __name__ == "__main__":
    main()
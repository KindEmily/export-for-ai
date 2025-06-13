import html
import logging
import os
import re
import sys
import json
import shutil
from typing import Optional, List, Dict

import pyperclip
import yaml

from export_for_ai.folder_exporter import export_folder_content, minify_code
from export_for_ai.tree_visualizer import get_tree_structure


def setup_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def parse_arguments() -> Dict[str, str]:
    args = {}
    if len(sys.argv) == 3 and sys.argv[1] == '--config':
        args['config_path'] = sys.argv[2]
    elif len(sys.argv) == 2:
        args['directory_path'] = os.path.abspath(sys.argv[1])
    else:
        # This is the error message you were seeing
        logging.error("Usage: export-for-ai <directory_path> OR export-for-ai --config <config_path>")
        sys.exit(1)
    return args


def validate_directory(directory_path: str) -> bool:
    if not os.path.isdir(directory_path):
        logging.error(f"Error: '{directory_path}' is not a valid directory")
        return False
    return True


def get_folder_name(directory_path: str) -> str:
    return os.path.basename(os.path.abspath(directory_path))


def create_export_directory(directory_path: str) -> Optional[tuple[str, str]]:
    folder_name = get_folder_name(directory_path)
    export_dir_name = f"exported-from-{folder_name}"
    export_dir_path = os.path.join(directory_path, export_dir_name)

    try:
        os.makedirs(export_dir_path, exist_ok=True)
        return export_dir_path, folder_name
    except OSError as e:
        logging.error(f"Error creating temporary export directory: {e}")
        return None


def export_project_md(
    tree_structure: str, folder_contents: str, export_dir: str, folder_name: str
) -> Optional[str]:
    """
    Combines tree structure and folder contents into project-....md file.
    Returns the path to the created file.
    """
    try:
        dynamic_sections = """
# Previous step

# The goal

# Core Design Philosophy
Seek a most minimal, simple, fewest LOC, lowest complexity design plans or paths to the required functionality. Preserve the robust, clutter-free design, and avoid any code, features, or decorations that do not directly contribute to the strictly essential functionality. It must be raw, and should aim to retain most or all existing functionality, unless the task is to, or requires that you, remove it. Aim to avoid creating divergent code pathways, and instead seek unified routes without branching where possible. Don't attempt to improvise, innovate, make unspecified improvements or changes, or move outside the scope of your specified task. Do not blindly follow the task instructions and analysis. Verify for yourself that the conclusions are accurate, and will not cause unanticipated side effects.
"""
        content = (
            f"{dynamic_sections}"
            "\n\n# SolutionTreeView \n```\n"
            f"{tree_structure}\n"
            "```\n\n"
            "\n\n# Entire Solution Code start \n"
            f"{folder_contents}\n"
            "# EntireSolution Code end \n"
        )

        project_md_filename = f"project-{folder_name}.md"
        project_md_path = os.path.join(export_dir, project_md_filename)
        with open(project_md_path, "w", encoding="utf-8") as f:
            f.write(content)
        logging.info(f"Generated '{project_md_filename}' in {export_dir}")

        try:
            pyperclip.copy(content)
            logging.info("Content for clipboard updated.")
        except Exception as e:
            logging.warning(f"Could not copy to clipboard: {e}")

        return project_md_path
    except Exception as e:
        logging.error(f"Error exporting project.md: {e}")
        return None

def process_single_repository(directory_path: str) -> Optional[str]:
    """Processes a single repository and returns the path to the generated markdown file."""
    if not validate_directory(directory_path):
        return None

    logging.info(f"--- Processing repository: {directory_path} ---")

    export_dir, folder_name = create_export_directory(directory_path)
    if export_dir is None:
        return None

    logging.info("Exporting directory structure...")
    tree_structure = get_tree_structure(directory_path)

    logging.info("Exporting folder contents...")
    folder_contents = export_folder_content(directory_path)

    if tree_structure and folder_contents:
        md_file_path = export_project_md(tree_structure, folder_contents, export_dir, folder_name)
        return md_file_path
    
    return None


def main() -> None:
    setup_logging()
    args = parse_arguments()

    if 'directory_path' in args:
        md_file = process_single_repository(args['directory_path'])
        if md_file:
            logging.info(f"\nExport completed successfully.")
            logging.info(f"Final file path: {md_file}")

    elif 'config_path' in args:
        config_path = args['config_path']
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            export_destination = config.get("export_destination")
            repositories = config.get("repositories", [])

            if not export_destination or not os.path.isdir(export_destination):
                logging.error(f"Export destination '{export_destination}' is not a valid directory.")
                return

            if not repositories:
                logging.warning("No repositories listed in config file.")
                return
            
            logging.info(f"Loaded {len(repositories)} repositories from config.")
            logging.info(f"Aggregated export destination: {export_destination}")

            for repo_path in repositories:
                md_file_path = process_single_repository(repo_path)
                if md_file_path:
                    try:
                        shutil.copy(md_file_path, export_destination)
                        logging.info(f"Copied '{os.path.basename(md_file_path)}' to {export_destination}\n")
                        shutil.rmtree(os.path.dirname(md_file_path))
                    except (shutil.Error, IOError) as e:
                        logging.error(f"Failed to copy '{md_file_path}' to destination: {e}\n")
            
            logging.info("All repositories processed.")

        except FileNotFoundError:
            logging.error(f"Config file not found: {config_path}")
        except json.JSONDecodeError:
            logging.error(f"Error decoding JSON from config file: {config_path}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()


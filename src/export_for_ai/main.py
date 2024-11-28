# main.py
import html
import logging
import os
import re
import sys
from typing import Optional

from export_for_ai.folder_exporter import export_folder_content, minify_code
from export_for_ai.readme_generator import create_readme
from export_for_ai.tree_visualizer import get_tree_structure


def setup_logging() -> None:
    logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")


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


def create_export_directory(directory_path: str) -> Optional[str]:
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


def build_tag(
    tag: str, content: str, attributes: dict = None, self_closing: bool = False
) -> str:
    """
    Builds an XML/HTML-like tag with optional attributes and content.

    :param tag: The name of the tag.
    :param content: The inner content of the tag.
    :param attributes: A dictionary of attributes for the tag.
    :param self_closing: If True, creates a self-closing tag.
    :return: The constructed tag as a string.
    """
    # Validate tag name (simple regex for tag names)
    if not re.match(r"^[A-Za-z_][A-Za-z0-9_.-]*$", tag):
        raise ValueError(f"Invalid tag name: {tag}")

    attrs = ""
    if attributes:
        attrs = " " + " ".join(
            f'{key}="{html.escape(str(value), quote=True)}"'
            for key, value in attributes.items()
        )

    if self_closing:
        return f"<{tag}{attrs} />"
    else:
        escaped_content = html.escape(content)
        return f"<{tag}{attrs}>\n\n{escaped_content}\n\n</{tag}>"


def save_content(
    content: str, output_file: str, tag: str = "LogicalBlock", attributes: dict = None
) -> bool:
    """
    Saves the content wrapped in a specified tag to an output file.

    :param content: The content to wrap and save.
    :param output_file: The path to the output file.
    :param tag: The tag to wrap the content with.
    :param attributes: Optional dictionary of attributes for the tag.
    :return: True if successful, False otherwise.
    """
    try:
        minify = minify_code(content)

        wrapped_content = build_tag(tag, minify, attributes)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(wrapped_content)
        logging.info(f"Content exported to {output_file}")
        return True
    except (IOError, ValueError) as e:
        logging.error(f"Error writing to file: {e}")
        return False


def export_tree_structure(directory_path: str) -> Optional[str]:
    try:
        logging.info("Exporting directory structure...")
        return get_tree_structure(directory_path)
    except Exception as e:
        logging.error(f"Error generating tree structure: {e}")
        return None


def export_folder_contents(directory_path: str) -> Optional[str]:
    try:
        logging.info("Exporting folder contents...")
        return export_folder_content(directory_path)
    except Exception as e:
        logging.error(f"Error exporting folder contents: {e}")
        return None


# File: src/export_for_ai/main.py

from typing import Optional

from export_for_ai.section_manager import section_manager  # Import the section manager

# ... (rest of the imports and existing code)


def export_project_md(
    tree_structure: str, folder_contents: str, export_dir: str
) -> bool:
    """
    Combines the dynamically added sections, tree structure, and folder contents into project.md.

    :param tree_structure: The string representation of the tree structure.
    :param folder_contents: The string representation of the folder contents.
    :param export_dir: The directory where project.md will be saved.
    :return: True if successful, False otherwise.
    """
    try:
        # Get dynamically added sections
        dynamic_sections = section_manager.get_sections_content()

        content = (
            f"{dynamic_sections}"
            "<SolutionTreeView>\n"
            f"{tree_structure}\n"
            "</SolutionTreeView>\n\n"
            "<EntireSolutionCode>\n"
            f"{folder_contents}\n"
            "</EntireSolutionCode>\n"
        )
        project_md_path = os.path.join(export_dir, "project.md")
        with open(project_md_path, "w", encoding="utf-8") as f:
            f.write(content)
        logging.info(f"Project.md exported to {project_md_path}")
        return True
    except Exception as e:
        logging.error(f"Error exporting project.md: {e}")
        return False


# File: src/export_for_ai/main.py

# ... (existing imports)


def load_config(config_path: str) -> dict:
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        logging.error(f"Error loading config file: {e}")
        return {}


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

    # Load section contents from config.yaml
    config = load_config(os.path.join(directory_path, "config.yaml"))
    if config:
        for block_name, block_content in config.items():
            # Convert snake_case to CamelCase for block names if necessary
            formatted_block_name = "".join(
                word.capitalize() for word in block_name.split("_")
            )
            section_manager.add_section(formatted_block_name, block_content)
    else:
        # Fallback to default sections if config is not available or empty
        section_manager.add_section(
            "CurrentGoal",
            "### Current Goal\n\nYour current goal description goes here.\nIt can span multiple lines.",
        )

        section_manager.add_section(
            "MainGoal",
            "### Main Goal\n\nYour main goal description goes here.\nIt can span multiple lines.",
        )

        section_manager.add_section(
            "ProjectDetails",
            """### Project Details

            This section provides detailed information about the project.

            - **Objective**: Describe the primary objective.
            - **Scope**: Outline the scope of the project.
            - **Technologies Used**: List the technologies involved.
            - **Team Members**: Mention the team members and their roles.
            """,
        )

    # Export Directory Structure
    tree_structure = export_tree_structure(directory_path)
    if tree_structure:
        tree_output_file = os.path.join(export_dir, "project_structure.txt")
        if not save_content(tree_structure, tree_output_file, "SolutionTreeView"):
            return

    # Export Folder Contents with Correct Tag and File Path
    folder_contents = export_folder_contents(directory_path)
    if folder_contents:
        folder_output_file = os.path.join(export_dir, "project_contents.md")
        if not save_content(
            folder_contents, folder_output_file, tag="EntireSolutionCode"
        ):
            return

    # Generate project.md combining tree and code with dynamic sections
    if tree_structure and folder_contents:
        if not export_project_md(tree_structure, folder_contents, export_dir):
            return

    # Create README.md
    readme_content = create_readme(get_folder_name(directory_path))
    if not save_content(readme_content, os.path.join(export_dir, "README.md")):
        return

    logging.info(f"Export completed successfully. Files saved in {export_dir}")


if __name__ == "__main__":
    main()

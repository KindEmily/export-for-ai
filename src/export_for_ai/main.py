# main.py
import html
import logging
import os
import re
import sys
from typing import Optional

import pyperclip
import yaml

from export_for_ai.folder_exporter import export_folder_content, minify_code
from export_for_ai.tree_visualizer import get_tree_structure
from export_for_ai.ignore_generator import generate_exportignore


def setup_logging() -> None:
    logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")


def parse_arguments() -> tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Parses command line arguments.
    Returns a tuple (command, directory_path, template_name).
    Command can be 'export' or 'generate-ignore'.
    Template_name is for the 'export' command.
    Returns (None, None, None) if arguments are invalid.
    """
    args = sys.argv[1:] # Exclude script name

    command: Optional[str] = None
    directory_path: Optional[str] = None
    template_name: Optional[str] = "default" # Default template

    if not args:
        logging.error(
            "Usage: \n"
            "  export-for-ai <directory_path> [-t <template_name>|--template <template_name>] (Exports the project)\n"
            "  export-for-ai generate-ignore <directory_path>                               (Generates .exportignore content)"
        )
        return None, None, None

    if args[0] == "generate-ignore":
        command = "generate-ignore"
        if len(args) == 2:
            directory_path = os.path.abspath(args[1])
            # Template name is not used for generate-ignore, keep it as default or None
        else:
            logging.error("Usage: export-for-ai generate-ignore <directory_path>")
            return None, None, None
    else: # Default command is 'export'
        command = "export"
        if not args: # Should be caught by the initial `if not args` but good for clarity
             logging.error("Usage: export-for-ai <directory_path> [-t <template_name>|--template <template_name>]")
             return None, None, None

        directory_path = os.path.abspath(args[0])
        
        # Parse template option
        i = 1
        while i < len(args):
            if args[i] in ("-t", "--template"):
                if i + 1 < len(args):
                    template_name = args[i+1]
                    i += 2
                else:
                    logging.error(f"{args[i]} option requires a template name.")
                    return None, None, None
            else:
                # If it's not a recognized option for export, it's an error
                logging.error(f"Unknown option for export: {args[i]}")
                logging.error(
                    "Usage: \n"
                    "  export-for-ai <directory_path> [-t <template_name>|--template <template_name>] (Exports the project)\n"
                    "  export-for-ai generate-ignore <directory_path>                               (Generates .exportignore content)"
                )
                return None, None, None
        
        # Check if directory_path was actually the first argument
        # This is implicitly handled by directory_path = os.path.abspath(args[0])
        # and the loop for options starting at i = 1.
        # If args[0] was -t or --template, it would error as not a valid path.
        # However, let's ensure directory_path is not an option itself.
        if directory_path.startswith("-"):
            logging.error(f"Invalid directory path: {directory_path}. Path cannot start with '-'.")
            logging.error(
                "Usage: \n"
                "  export-for-ai <directory_path> [-t <template_name>|--template <template_name>] (Exports the project)\n"
                "  export-for-ai generate-ignore <directory_path>                               (Generates .exportignore content)"
            )
            return None, None, None


    return command, directory_path, template_name


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

# ... (rest of the imports and existing code)


def export_project_md(
        tree_structure: str, folder_contents: str, export_dir: str
) -> bool:
    """
    Combines the dynamically added sections, tree structure, and folder contents into project.md.
    Also copies the content to system clipboard.

    :param tree_structure: The string representation of the tree structure.
    :param folder_contents: The string representation of the folder contents.
    :param export_dir: The directory where project.md will be saved.
    :return: True if successful, False otherwise.
    """
    try:
        # Get dynamically added sections
        dynamic_sections = """
# Previous step 

# The goal

# Core Design Philosophy
Seek a most minimal, simple, fewest LOC, lowest complexity design plans or paths to the required functionality. Preserve the robust, clutter-free design, and avoid any code, features, or decorations that do not directly contribute to the strictly essential functionality. It must be raw, and should aim to retain most or all existing functionality, unless the task is to, or requires that you, remove it. Aim to avoid creating divergent code pathways, and instead seek unified routes without branching where possible. Don't attempt to improvise, innovate, make unspecified improvements or changes, or move outside the scope of your specified task. Do not blindy follow the task instructions and analysis. Verify for yourself that the conclusions are accurate, and will not cause unanticipated side effects.

### Requirement:
Leverages existing libraries when possible to minimize manual implementation.

### Requirement:
Use already existing implementation when possible.

### Requirement:
Create reusable code and reuse existing code.

### Requirement:
Implement abstractions like base classes and common interfaces.

### Requirement:
Utilize the best libraries to minimize manual coding
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
        project_md_path = os.path.join(export_dir, "project.md")
        with open(project_md_path, "w", encoding="utf-8") as f:
            f.write(content)
        logging.info(f"Project.md exported to {project_md_path}")

        # Copy content to clipboard
        try:
            pyperclip.copy(content)
            logging.info("Content successfully copied to clipboard")
        except Exception as e:
            logging.warning(f"Could not copy to clipboard: {e}")

        return True
    except Exception as e:
        logging.error(f"Error exporting project.md: {e}")
        return False


def load_config(config_path: str) -> dict:
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        logging.error(f"Error loading config file: {e}")
        return {}


def main() -> None:
    setup_logging()

    command, directory_path, template_name = parse_arguments()

    if not command or not directory_path: # template_name can be None or default
        return

    if command == "generate-ignore":
        # Validate directory for generate-ignore command
        if not os.path.isdir(directory_path): 
            logging.error(f"Error: '{directory_path}' is not a valid directory for generating ignore file.")
            return
        ignore_content = generate_exportignore(directory_path) # generate_exportignore doesn't use templates
        print(ignore_content)
        return  # Exit after printing ignore content
    
    # Proceed with export logic if command is "export"
    if command == "export":
        # Validate directory for export command
        if not validate_directory(directory_path): # validate_directory checks os.path.isdir
            return

        # Use "default" if template_name is None (it's set to "default" in parse_arguments if not provided)
        current_template_name = template_name if template_name else "default"
        logging.info(f"Using template: {current_template_name}")


        export_dir = create_export_directory(directory_path)
        if not export_dir:
            return

        # Load section contents from config.yaml
        # Skipped

        # Export Directory Structure, passing the template name
        tree_structure = export_tree_structure(directory_path, template_name=current_template_name)
        if tree_structure:
            tree_output_file = os.path.join(export_dir, "project_structure.txt")
            if not save_content(tree_structure, tree_output_file, "SolutionTreeView"):
                return

        # Export Folder Contents, passing the template name
        folder_contents = export_folder_contents(directory_path, template_name=current_template_name)
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

        logging.info(f"Export completed successfully. Files saved in {export_dir}")


if __name__ == "__main__":
    main()

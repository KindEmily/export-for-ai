import os
import logging
from typing import List
from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern

# DEFAULT_IGNORE_PATTERNS is removed

def load_template_patterns(template_name: str) -> List[str]:
    """
    Loads ignore patterns from a specified template file.

    :param template_name: The name of the template (e.g., "default", "light").
    :return: A list of pattern strings.
    """
    # Construct the path relative to this script's location or a known base path
    # Assuming this script is in src/export_for_ai/
    base_dir = os.path.dirname(os.path.abspath(__file__)) 
    template_file_path = os.path.join(base_dir, 'ignore_templates', f"{template_name}.template")
    
    patterns = []
    try:
        with open(template_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    patterns.append(line)
        logging.info(f"Successfully loaded ignore patterns from template: {template_name}.template")
    except FileNotFoundError:
        logging.warning(f"Template file not found: {template_file_path}. Returning empty list of patterns.")
        # Optionally, return a minimal default like ['.git/'] instead of an empty list
        # For this task, returning an empty list as specified.
    except Exception as e:
        logging.error(f"Error loading template {template_name}.template: {e}")
        # Fallback to empty list or minimal sensible default
    return patterns

def parse_ignore_file(directory: str, template_name: str = "default") -> PathSpec:
    """
    Parses the .exportignore file and combines it with patterns from a specified template.
    
    :param directory: The root directory of the project.
    :param template_name: The name of the template to use for base patterns.
    :return: A PathSpec object containing all ignore patterns.
    """
    # Load base patterns from the specified template
    patterns = load_template_patterns(template_name)
    
    # Load patterns from .exportignore file in the project directory
    ignore_file_path = os.path.join(directory, '.exportignore')
    if os.path.exists(ignore_file_path):
        try:
            with open(ignore_file_path, 'r', encoding='utf-8') as f:
                project_specific_patterns = []
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        project_specific_patterns.append(line)
                
                if project_specific_patterns:
                    patterns.extend(project_specific_patterns)
                    logging.info(f"Loaded and combined ignore patterns from .exportignore in {directory}")
                else:
                    logging.info(f".exportignore file found in {directory} but it's empty or contains only comments.")
        except Exception as e:
            logging.error(f"Error reading .exportignore file at {ignore_file_path}: {e}")
    else:
        logging.info(f"No .exportignore file found in {directory}. Using patterns from '{template_name}' template.")
        # If no .exportignore, patterns list already contains template patterns.
        # If template also failed to load, patterns might be empty.

    if not patterns:
        logging.warning(f"No ignore patterns loaded (template '{template_name}' failed or was empty, and no .exportignore found or it was empty). Proceeding with an empty spec, which means nothing will be ignored.")
        # PathSpec with empty patterns will match nothing, effectively including all files.
        
    spec = PathSpec.from_lines(GitWildMatchPattern, patterns)
    logging.debug(f"Final combined ignore patterns for PathSpec (template: {template_name}): {patterns}")
    return spec

def should_include_item(item, spec):
    """
    Determines whether an item should be included based on ignore patterns.
    
    :param item: The relative path of the item.
    :param spec: The PathSpec object containing ignore patterns.
    :return: True if the item should be included, False otherwise.
    """
    return not spec.match_file(item)

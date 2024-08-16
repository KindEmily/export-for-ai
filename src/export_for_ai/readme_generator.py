def create_readme(project_name):
    """Create a README file explaining the exported content."""
    return f"""# {project_name} Export

This folder contains an export of the {project_name} project structure and its contents.

Files:
1. project_structure.txt: A text representation of the project's folder structure.
2. project_contents.txt: The contents of all relevant files in the project.
3. README.md: This file, explaining the contents of the export.

This export was created to easily share project contents and structure, particularly for use in AI-assisted development contexts.
"""

if __name__ == "__main__":
    # This allows the module to be run standalone for testing
    print(create_readme("Test Project"))

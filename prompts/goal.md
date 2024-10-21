# Current objective 
<CurrentObjective>
    Fix bug where `.venv` folder is being added to the result .md file (`project_contents.md) 
    The Code also checking all the files in the repo. We need to optimize this - if the root folder is on the skipped list - do not even open that fodler for an export list
</CurrentObjective>

# The main goal 
<MainGoal>

</MainGoal>

<ImportantInstruction>
    Do incorporate all the enhancements at once and provide final code snippets or entire files if needed only. FOCUS ON FINAL SOLUTION
</ImportantInstruction>

# Solution code: 
<SolutionCode> 
# File: .exportignore
```
# Python byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
.DS_Store
*.DS_Store

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# pyenv
.python-version

# celery beat schedule file
celerybeat-schedule

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/

# IDE settings
.vscode/
.idea/

# Project-specific
exported-from-*

# Images 
*.jpg
*.jpeg
*.png
*.svg

/output/
/bin/
```

# File: README.md
```
# export-for-ai
![usage gif](https://github.com/KindEmily/export-for-ai/blob/main/demo/export-for-ai-usage.gif?raw=true)

## Why this tool? 
THis is a tool to export data for AI processing into services like ChatGPT or Claude.ai. 
Just export, drag and drop to the context.

```
cd C:\Users\probl\Work\ExampleFolder\awesome-app
export-for-ai C:\Users\probl\Work\ExampleFolder\
``` 

# To use this:


Run pip install -e . in the directory containing setup.py to install your package in editable mode.

You should then be able to run `export-for-ai` from the command line, which will execute the `main() function in `src/export_for_ai/main.py`.`

```

# File: setup.py
```
# setup.py

from setuptools import setup, find_packages

setup(
    name="export-for-ai", # export-here-from 
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "export-for-ai=main:main",  # Note the underscore in the package name
        ],
    },
    install_requires=[
        # Add any dependencies here
    ],
    author="Emily Vlasiuk",
    #author_email="your.email@example.com",
    description="A tool to export data for AI processing.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    #url="https://github.com/yourusername/export-for-ai",  # Replace with your repo URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
```

# File: prompts\goal.md
```
# Current objective 
<CurrentObjective>

</CurrentObjective>

# The main goal 
<MainGoal>

</MainGoal>

<ImportantInstruction>
    Do incorporate all the enhancements at once and provide final code snippets or entire files if needed only. FOCUS ON FINAL SOLUTION
</ImportantInstruction>

# Solution code: 
<SolutionCode> 

</SolutionCode> 
```

# File: prompts\template.md
```
# Current objective 
<CurrentObjective>
    Fix bug where `.venv` folder is being added to the result .md file (`project_contents.md) 
    The Code also checking all the files in the repo. We need to optimize this - if the root folder is on the skipped list - do not even open that fodler for an export list
</CurrentObjective>

<Logs>

</Logs>

# The main goal 
<MainGoal>
Code application to export all files from root folder into a sinlge .md file. Skip specific folders if specified 
</MainGoal>

<ImportantInstruction>
    Do incorporate all the enhancements at once and provide final code snippets or entire files if needed only. FOCUS ON FINAL SOLUTION
</ImportantInstruction>

# Solution code: 
<SolutionCode> 

</SolutionCode> 
```

# File: src\main.py
```
import sys
import os
import logging
from typing import Optional

from export_for_ai.tree_visualizer import get_tree_structure
from export_for_ai.folder_exporter import export_folder_content
from export_for_ai.readme_generator import create_readme

def setup_logging() -> None:
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

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
        if not save_content(folder_contents, os.path.join(export_dir, "project_contents.md")):
            return

    readme_content = create_readme(get_folder_name(directory_path))
    if not save_content(readme_content, os.path.join(export_dir, "README.md")):
        return

    logging.info(f"Export completed successfully. Files saved in {export_dir}")

if __name__ == "__main__":
    main()
```

# File: src\export_for_ai\folder_exporter.py
```
import os
import logging
from .ignore_parser import parse_ignore_file, should_include_item

def export_folder_content(path):
    """Export the content of all included files in the folder."""
    ignore_patterns = parse_ignore_file(path)
    content = []
    for root, _, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, path)
            if should_include_item(relative_path, ignore_patterns):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        file_content = f.read()
                        if file_content.strip():
                            content.append(f"# File: {relative_path}\n")
                            content.append("```\n")
                            content.append(file_content)
                            content.append("\n```\n\n")
                        else:
                            content.append(f"# File: {relative_path}\n")
                            content.append("`File is empty`\n\n")
                except Exception as e:
                    content.append(f"Error reading {relative_path}: {str(e)}\n\n")
            else:
                logging.debug(f"Skipping file: {relative_path}")
    return ''.join(content)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(export_folder_content(sys.argv[1]))
    else:
        print("Please provide a path as an argument.")
```

# File: src\export_for_ai\ignore_parser.py
```
import os
import fnmatch
import logging

DEFAULT_IGNORE_PATTERNS = [
    '*.git*',
    '__pycache__',
    '*.pyc',
    '*.pyo',
    '*.pyd',
    '*.so',
    '*.dll',
    '*.exe',
    '*.bin',
    '*.obj',
    '*.bak',
    '*.tmp',
    '*.swp',
    '*.vscode',
    '*.DS_Store',
    '.DS_Store',
    'output',
    'output/**',
    'exported-from-*',
    'exported-from-**',
    '*.vs',
    'bin',
    'obj',
    '*.idea',
    'exported-from-*',
    '*.egg-info',
    '*.egg-info/**',  # This will match all contents of egg-info directories
    '*.png',
    '*.jpg',
    '*.jpeg',
    '*.gif',
    '*.bmp',
    '*.tiff',
    '*.webp',

    '*.jpg',

    '*.json',
    '.csv'
    '*.csv'
    '*.venv'
]

def parse_ignore_file(directory):
    ignore_patterns = DEFAULT_IGNORE_PATTERNS.copy()
    ignore_file_path = os.path.join(directory, '.exportignore')
    
    if os.path.exists(ignore_file_path):
        with open(ignore_file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    ignore_patterns.append(line)
        logging.info(f"Loaded {len(ignore_patterns)} ignore patterns from .exportignore")
    else:
        logging.warning("No .exportignore file found. Using default exclusion rules.")
    
    return ignore_patterns

def should_include_item(item, ignore_patterns):
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(item, pattern) or any(fnmatch.fnmatch(part, pattern) for part in item.split(os.sep)):
            logging.debug(f"Ignoring {item} due to pattern {pattern}")
            return False
    return True
```

# File: src\export_for_ai\readme_generator.py
```
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

```

# File: src\export_for_ai\tree_visualizer.py
```
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
```

# File: src\export_for_ai\__init__.py
`File is empty`


</SolutionCode> 
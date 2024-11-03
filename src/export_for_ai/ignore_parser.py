import os
import logging
from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern

DEFAULT_IGNORE_PATTERNS = [
    '__pycache__/',
    '*.py[cod]',
    '.DS_Store',
    '.git',
    '.git/**',
    '.vs',
    '.vs/**',
    '*.so',
    '.Python',
    'build/',
    'develop-eggs/',
    'dist/',
    'downloads/',
    'eggs/',
    '.eggs/',
    'lib/',
    'lib64/',
    'parts/',
    'sdist/',
    'var/',
    'wheels/',
    '*.egg-info/',
    '.installed.cfg',
    '*.egg',
    '*.manifest',
    '*.spec',
    'pip-log.txt',
    'pip-delete-this-directory.txt',
    'htmlcov/',
    '.tox/',
    '.coverage',
    '.coverage.*',
    'nosetests.xml',
    'coverage.xml',
    '*.cover',
    '.hypothesis/',
    '*.mo',
    '*.pot',
    '*.log',
    'local_settings.py',
    'instance/',
    '.webassets-cache',
    '.scrapy',
    'docs/_build/',
    'target/',
    '.ipynb_checkpoints',
    '.python-version',
    'celerybeat-schedule',
    '*.sage.py',
    '.env',
    '.venv',
    'env/',
    'venv/',
    'ENV/',
    '.spyderproject',
    '.spyproject',
    '.ropeproject',
    '/site',
    '.mypy_cache/',
    '.vscode/',
    '.idea/',
    '*.jpg',
    '*.jpeg',
    '*.png',
    '*.svg',
    '*.md',
    '*.txt',
    '/output/',
    '.bin/',
]

def parse_ignore_file(directory):
    """
    Parses the .exportignore file and combines it with default ignore patterns.
    
    :param directory: The root directory of the project.
    :return: A PathSpec object containing all ignore patterns.
    """
    ignore_file_path = os.path.join(directory, '.exportignore')
    patterns = DEFAULT_IGNORE_PATTERNS.copy()
    
    if os.path.exists(ignore_file_path):
        with open(ignore_file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    patterns.append(line)
        logging.info(f"Loaded ignore patterns from .exportignore")
    else:
        logging.warning("No .exportignore file found. Using default exclusion rules.")
    
    spec = PathSpec.from_lines(GitWildMatchPattern, patterns)
    logging.debug(f"Final ignore patterns: {patterns}")
    return spec

def should_include_item(item, spec):
    """
    Determines whether an item should be included based on ignore patterns.
    
    :param item: The relative path of the item.
    :param spec: The PathSpec object containing ignore patterns.
    :return: True if the item should be included, False otherwise.
    """
    return not spec.match_file(item)

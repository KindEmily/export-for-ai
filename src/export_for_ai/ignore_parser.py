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
    '*.egg-info',
    '*.egg-info/**',  # This will match all contents of egg-info directories
    '*.png',
    '*.jpg',
    '*.jpeg',
    '*.gif',
    '*.bmp',
    '*.tiff',
    '*.webp',
    '*.json',
    '.csv',
    '*.csv',
    '.venv',
    '*.jpg',
    '*.venv', 
    
    '*.log',
    '*.md',
    '*.txt'
    '.pytest_cache', 
    '*.pytest_cache', 
    '.pytest_cache/**',
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

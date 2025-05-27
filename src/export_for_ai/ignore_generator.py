import os
import glob

# Define project types and their fingerprints/ignores
PROJECT_TYPES = {
    "Python": {
        "fingerprints": ["requirements.txt", "pyproject.toml", "setup.py"],
        "ignores": [
            "__pycache__/",
            "*.py[cod]",
            ".venv/",
            "venv/",
            "env/",
            "*.egg-info/",
            "build/",
            "dist/",
            ".pytest_cache/",
            ".mypy_cache/",
        ],
    },
    "Node.js": {
        "fingerprints": ["package.json", "package-lock.json", "yarn.lock"],
        "ignores": [
            "node_modules/",
            "*.log",
            "npm-debug.log*",
            "yarn-debug.log*",
            "yarn-error.log*",
            "build/",
            "dist/",
        ],
    },
    "C# (.NET)": {
        "fingerprints": ["*.csproj", "*.sln"], # These are globs
        "ignores": [
            "[Bb]in/",
            "[Oo]bj/",
            "*.user",
            "*.suo",
            ".vs/",
        ],
    },
}

# Generic ignores for fallback when no specific project type is detected
GENERIC_IGNORES_FULL = [
    ".git/",
    ".hg/",
    ".svn/",
    ".DS_Store",
    "Thumbs.db",
    "temp/",
    "tmp/",
    "*~",
    "*.bak",
    "*.swp",
    ".vscode/",
    "exported-from-*/",
]

# Subset of generic ignores to be added to detected projects, as per example for Python
GENERAL_SUPPLEMENTAL_IGNORES = [
    ".git/",
    ".DS_Store",
    ".vscode/",
]


def generate_exportignore(directory_path: str) -> str:
    """
    Generates .exportignore patterns based on detected project type in the given directory.
    """
    detected_project_type = None
    output_lines = []

    try:
        # Ensure directory exists. If not, treat as "no specific type detected".
        if not os.path.isdir(directory_path):
            output_lines.append("# No specific project type detected, using generic ignores.")
            output_lines.extend(GENERIC_IGNORES_FULL)
            return "\n".join(output_lines)

        # Scan for project type
        for project_name, details in PROJECT_TYPES.items():
            for fingerprint in details["fingerprints"]:
                search_path = os.path.join(directory_path, fingerprint)
                # Check for glob patterns (e.g., *.csproj)
                if "*" in fingerprint or "?" in fingerprint: # Simple check for glob characters
                    if glob.glob(search_path): # glob.glob handles the path joining correctly
                        detected_project_type = project_name
                        break
                # Check for direct file existence
                elif os.path.exists(search_path):
                    detected_project_type = project_name
                    break
            if detected_project_type:
                break

        if detected_project_type:
            output_lines.append(f"# {detected_project_type} project detected")
            project_ignores = PROJECT_TYPES[detected_project_type]["ignores"]
            output_lines.extend(project_ignores)

            # Add supplemental general ignores
            if project_ignores: # Only add newline if there were project-specific ignores
                output_lines.append("") 
            output_lines.append("# General")
            
            # Add supplemental ignores, avoiding duplicates if they were already in project_ignores
            current_project_ignores_set = set(project_ignores)
            for pattern in GENERAL_SUPPLEMENTAL_IGNORES:
                if pattern not in current_project_ignores_set:
                    output_lines.append(pattern)
        else:
            output_lines.append("# No specific project type detected, using generic ignores.")
            output_lines.extend(GENERIC_IGNORES_FULL)

    except Exception as e:
        # Fallback to generic ignores in case of any error during detection
        # This ensures the function always returns a valid string of ignore patterns.
        output_lines = [f"# Error scanning directory: {str(e)}, using generic ignores."]
        output_lines.extend(GENERIC_IGNORES_FULL)

    # Ensure final output is a single string with newlines, and stripped of any leading/trailing whitespace.
    return "\n".join(output_lines).strip()

if __name__ == '__main__':
    # Example usage (for testing purposes)

    def setup_test_dir(name, files_to_create=None, globs_to_create=None):
        # Simplified cleanup and setup
        if os.path.exists(name):
            import shutil
            shutil.rmtree(name)
        os.makedirs(name, exist_ok=True)

        if files_to_create:
            for f_name in files_to_create:
                with open(os.path.join(name, f_name), "w") as f:
                    f.write("test content")
        if globs_to_create:
             for g_name in globs_to_create: # e.g., ["myproj.csproj"]
                with open(os.path.join(name, g_name), "w") as f:
                    f.write("test content")

    def cleanup_test_dir(name):
        if os.path.exists(name):
            import shutil
            shutil.rmtree(name)

    # Test Python Project
    PYTHON_DIR = "test_proj_py_actual"
    setup_test_dir(PYTHON_DIR, files_to_create=["requirements.txt"])
    print("--- Python Project Test ---")
    print(generate_exportignore(PYTHON_DIR))
    cleanup_test_dir(PYTHON_DIR)
    # Expected for Python:
    # # Python project detected
    # __pycache__/
    # *.py[cod]
    # .venv/
    # venv/
    # env/
    # *.egg-info/
    # build/
    # dist/
    # .pytest_cache/
    # .mypy_cache/
    #
    # # General
    # .git/
    # .DS_Store
    # .vscode/

    # Test Node.js Project
    NODE_DIR = "test_proj_node_actual"
    setup_test_dir(NODE_DIR, files_to_create=["package.json"])
    print("\n--- Node.js Project Test ---")
    print(generate_exportignore(NODE_DIR))
    cleanup_test_dir(NODE_DIR)

    # Test C# Project (csproj)
    CSHARP_CSPROJ_DIR = "test_proj_cs_csproj_actual"
    setup_test_dir(CSHARP_CSPROJ_DIR, globs_to_create=["MyProject.csproj"])
    print("\n--- C# Project Test (.csproj) ---")
    print(generate_exportignore(CSHARP_CSPROJ_DIR))
    cleanup_test_dir(CSHARP_CSPROJ_DIR)
    
    # Test C# Project (sln)
    CSHARP_SLN_DIR = "test_proj_cs_sln_actual"
    setup_test_dir(CSHARP_SLN_DIR, globs_to_create=["MySolution.sln"])
    print("\n--- C# Project Test (.sln) ---")
    print(generate_exportignore(CSHARP_SLN_DIR))
    cleanup_test_dir(CSHARP_SLN_DIR)

    # Test Generic Project (empty directory)
    GENERIC_EMPTY_DIR = "test_proj_generic_empty_actual"
    setup_test_dir(GENERIC_EMPTY_DIR)
    print("\n--- Generic Project Test (Empty Dir) ---")
    print(generate_exportignore(GENERIC_EMPTY_DIR))
    cleanup_test_dir(GENERIC_EMPTY_DIR)
    # Expected for Generic (Empty or no match):
    # # No specific project type detected, using generic ignores.
    # .git/
    # .hg/
    # .svn/
    # .DS_Store
    # Thumbs.db
    # temp/
    # tmp/
    # *~
    # *.bak
    # *.swp
    # .vscode/
    # exported-from-*/

    # Test Generic Project (directory with non-fingerprint files)
    GENERIC_OTHER_DIR = "test_proj_generic_other_actual"
    setup_test_dir(GENERIC_OTHER_DIR, files_to_create=["README.md"])
    print("\n--- Generic Project Test (Other Files) ---")
    print(generate_exportignore(GENERIC_OTHER_DIR))
    cleanup_test_dir(GENERIC_OTHER_DIR)
    
    # Test non-existent directory
    NON_EXISTENT_DIR = "non_existent_dir_actual"
    # Ensure it's not there by trying to clean it up if it somehow exists
    cleanup_test_dir(NON_EXISTENT_DIR) 
    print("\n--- Non-existent Dir Test ---")
    print(generate_exportignore(NON_EXISTENT_DIR))

```

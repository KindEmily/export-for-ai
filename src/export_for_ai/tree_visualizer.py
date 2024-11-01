import logging
import os

from export_for_ai.ignore_parser import should_include_item, parse_ignore_file  # Added parse_ignore_file import


def visualize_folder_structure(path, root_path, ignore_patterns, prefix="", is_last=True):
    output = []
    basename = os.path.basename(path)
    relative_path = os.path.relpath(path, root_path)

    if os.path.isdir(path):
        if prefix == "":
            output.append(basename + "/")
        else:
            output.append(prefix + ("└── " if is_last else "├── ") + basename + "/")

        try:
            items = sorted(os.listdir(path))
        except PermissionError:
            logging.warning(f"Permission denied: {path}")
            return output

        # Separate directories and files
        dirs = [item for item in items if os.path.isdir(os.path.join(path, item))]
        files = [item for item in items if not os.path.isdir(os.path.join(path, item))]

        # Filter out ignored directories
        dirs = [
            d for d in dirs
            if should_include_item(os.path.relpath(os.path.join(path, d), root_path), ignore_patterns)
        ]

        # Filter out ignored files
        files = [
            f for f in files
            if should_include_item(os.path.relpath(os.path.join(path, f), root_path), ignore_patterns)
        ]

        combined = dirs + files
        for index, item in enumerate(combined):
            item_path = os.path.join(path, item)
            is_last_item = index == len(combined) - 1

            if os.path.isdir(item_path):
                output.extend(
                    visualize_folder_structure(
                        item_path,
                        root_path,
                        ignore_patterns,
                        prefix + ("    " if is_last_item else "│   "),
                        is_last_item
                    )
                )
            else:
                output.append(prefix + ("└── " if is_last_item else "├── ") + item)
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

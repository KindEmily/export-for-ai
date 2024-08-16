import os

def visualize_folder_structure(path, prefix="", is_last=True):
    output = []
    basename = os.path.basename(path)
    
    if os.path.isdir(path):
        if prefix == "":
            output.append(basename + "/")
        else:
            output.append(prefix + ("└── " if is_last else "├── ") + basename + "/")
        
        items = sorted(os.listdir(path))
        items = [item for item in items if not item.startswith('.')]
        
        for index, item in enumerate(items):
            item_path = os.path.join(path, item)
            is_last_item = index == len(items) - 1
            
            output.extend(
                visualize_folder_structure(
                    item_path,
                    prefix + ("    " if is_last else "│   "),
                    is_last_item
                )
            )
    else:
        output.append(prefix + ("└── " if is_last else "├── ") + basename)
    
    return output

def get_tree_structure(path):
    """Generate a string representation of the folder structure."""
    tree = visualize_folder_structure(path)
    return "\n".join(tree)

if __name__ == "__main__":
    # This allows the module to be run standalone for testing
    import sys
    if len(sys.argv) > 1:
        print(get_tree_structure(sys.argv[1]))
    else:
        print("Please provide a path as an argument.")

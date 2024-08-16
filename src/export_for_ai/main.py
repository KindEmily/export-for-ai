import sys
import os
import shlex

def main():
    if len(sys.argv) != 2:
        print("Usage: export-for-ai <directory_path>")
        sys.exit(1)
    
    # Use shlex.split to properly handle quoted arguments
    args = shlex.split(sys.argv[1])
    directory_path = args[0]
    
    # Normalize the path to handle potential issues with backslashes
    directory_path = os.path.normpath(directory_path)
    
    if not os.path.isdir(directory_path):
        print(f"Error: '{directory_path}' is not a valid directory")
        sys.exit(1)
    
    # Your export logic here
    print(f"Exporting directory: {directory_path}")
    # Add your actual export code here
    
    print(f"Add your actual export code here:")
    print(f"Add your actual export code here:")
    print(f"Add your actual export code here:")
    print(f"Simulation ended")

if __name__ == "__main__":
    main()
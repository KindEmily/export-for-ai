# export-for-ai (v0.3.1)
![usage gif](https://github.com/KindEmily/export-for-ai/blob/main/demo/export-for-ai-usage.gif?raw=true)

## Why this tool? 
This is a tool to export data for AI processing into services like ChatGPT or Claude.ai. 
Just export, drag and drop to the context.

## Installation Guide 

### Step 1: Check Your Python Installation
1. Open Command Prompt (CMD)
2. Type this command to check if Python is installed:
   ```cmd
   python --version
   ```
   You should see something like `Python 3.10.x`

### Step 2: Install the Package
1. Clone the repository:
   ```cmd
   git clone https://github.com/KindEmily/export-for-ai.git
   cd export-for-ai
   ```

2. Install in development mode:
   ```cmd
   python -m pip install -e .
   ```

3. Verify the installation:
   ```cmd
   python -m pip show export-for-ai
   ```
   You should see the package information including the version number.

### Step 3: Test the Installation
Try running:
```cmd
export-for-ai --help
```

## How to Update to New Versions

When a new version is released, follow these steps:

1. Go to the package directory:
   ```cmd
   cd export-for-ai
   ```

2. Get the latest code:
   ```cmd
   git pull origin main
   ```

3. Reinstall the package:
   ```cmd
   python -m pip install -e .
   ```

4. Verify the update:
   ```cmd
   python -m pip show export-for-ai
   ```
   Check that the version number matches the latest version.

## Troubleshooting

If you see an old version after updating:
1. Close all Command Prompt windows
2. Open a new Command Prompt
3. Check the version again:
   ```cmd
   python -m pip show export-for-ai
   ```

If you have multiple Python versions installed and want to make sure you're using the right one:
1. Find your Python installation:
   ```cmd
   where python
   ```
2. Use the full path to Python:
   ```cmd
   C:\Users\YourUsername\AppData\Local\Programs\Python\Python310\python.exe -m pip install -e .
   ```

## Usage

```bash
export-for-ai <directory_path>
```
Example:
```bash
export-for-ai C:\Users\username\MyProject
```
This will create a new directory named "exported-from-MyProject" containing:
- project.md with your project's structure and contents
- A comprehensive tree view of your project
- Properly formatted and minified code

----

## Using `.exportignore` with `export-for-ai`

The `export-for-ai` tool allows you to export your project's structure and content while excluding specific files and directories using an `.exportignore` file. This file functions similarly to a `.gitignore` file, enabling you to define patterns for items you want to exclude from the export.

### How to Use `.exportignore`

1. **Create the `.exportignore` File**: In the root directory of your project (the directory you will pass to `export-for-ai`), create a file named `.exportignore`.

2. **Define Ignore Patterns**: Inside `.exportignore`, list the files and directories you wish to exclude. Each pattern should be on a new line. You can use standard glob patterns (e.g., `*.log` to exclude all `.log` files).

   **Example `.exportignore` file:**
   ```
   # Exclude lock files
   poetry.lock
   package-lock.json

   # Exclude compiled Python files
   __pycache__/
   *.py[cod]

   # Exclude environment directories
   .env/
   venv/
   env/

   # Exclude documentation and logs
   *.md
   *.txt
   *.log
   ```

3. **Run `export-for-ai`**: Execute the tool by pointing it to your project's root directory.
   ```bash
   export-for-ai /path/to/your/project
   ```

### Examples

Below are some examples of how to specify patterns in your `.exportignore` file to exclude certain files and directories:

#### 1. Exclude an Entire Folder

To exclude a folder and all its contents, add the folder name followed by a slash:

```
node_modules/
```

This pattern will exclude the `node_modules` directory and everything inside it from the export.

#### 2. Exclude a Specific File

To exclude a specific file, simply write its relative path:

```
config/settings.py
```

This will exclude the `settings.py` file located in the `config` directory.

#### 3. Exclude Files or Folders Matching a Pattern

You can use glob patterns to match multiple files or directories:

- **Exclude all folders starting with `exported-from-`:**

  ```
  exported-from-*/
  ```

  This pattern matches any directory whose name starts with `exported-from-`, excluding them and their contents.

- **Exclude all files ending with `.bak`:**

  ```
  *.bak
  ```

  This will exclude all files with the `.bak` extension.

- **Exclude all log files in any directory:**

  ```
  **/*.log
  ```

  This pattern excludes all `.log` files in any subdirectory.

### Notes

- **Pattern Syntax**: The patterns in `.exportignore` are relative to the root directory of your project. Use glob patterns for flexible matching.
  - `folder/` ignores a directory named `folder` and all its contents.
  - `*.ext` ignores all files with the `.ext` extension.
  - `!important.txt` includes `important.txt` even if it was excluded by a previous pattern.

- **Verification**: To ensure your patterns are working as intended, you can check the log output. The tool will inform you which files and directories are being excluded based on your `.exportignore` settings.

- **Default Exclusions**: If no `.exportignore` file is found, `export-for-ai` uses a set of default patterns to exclude common unnecessary files (e.g., `__pycache__`, `.git` directories).

By customizing the `.exportignore` file, you can control precisely what content is included in your export, ensuring that only relevant files are processed and shared.
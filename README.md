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
node_modules/**
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
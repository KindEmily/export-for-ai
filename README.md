# export-for-ai 
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

![how to use](https://github.com/KindEmily/export-for-ai/blob/main/demo/how-to-install-or-update.png?raw=true)


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
export-for-ai <directory_path> [-t <template_name>|--template <template_name>]
export-for-ai generate-ignore <directory_path>
```

**Main Export Command:**
```bash
export-for-ai C:\Users\username\MyProject
```
Or with a specific template:
```bash
export-for-ai --template light C:\Users\username\MyProject
```
This will create a new directory named "exported-from-MyProject" containing:
- project.md with your project's structure and contents
- A comprehensive tree view of your project
- Properly formatted and minified code (based on selected ignore patterns)

**Generate .exportignore Command:**
```bash
export-for-ai generate-ignore C:\Users\username\MyProject
```
This will print a suggested `.exportignore` file content to the console.

----

## Controlling Exported Content with `.exportignore` and Templates

`export-for-ai` provides a flexible system to control which files and directories are included in your export, using a combination of ignore templates and a local `.exportignore` file.

### What is `.exportignore`?

The `.exportignore` file, much like a `.gitignore` file, allows you to specify patterns for files and directories that should be excluded from the export. You create this file in the root directory of your project.

### Creating Your `.exportignore` File

#### 1. Manual Creation
You can create and edit a file named `.exportignore` in your project's root directory. Add patterns one per line.
   **Example `.exportignore` file:**
   ```
   # Exclude specific config files
   config/local_settings.py

   # Exclude temporary data
   *.tmp
   temp_data/
   ```

#### 2. Auto-generating .exportignore
If you're unsure what to include in your `.exportignore` file, or want a good starting point, `export-for-ai` can help generate one for you. The tool can detect the type of project in your directory (e.g., Python, Node.js, C#) and suggest a set of ignore patterns tailored to that project type, along with common general exclusions.

To use this feature, run the following command:

```bash
export-for-ai generate-ignore /path/to/your/project
```

This will print the suggested `.exportignore` content to your terminal. You can then review it and save it to your `.exportignore` file.

To save the output directly to an `.exportignore` file in your project's root directory, you can use:

```bash
export-for-ai generate-ignore /path/to/your/project > .exportignore
```
This generated file can then be further customized to meet your specific needs by editing it directly.

### Using Ignore Templates

`export-for-ai` uses a template system to define the base set of ignore patterns for your project export. You can choose a template using the `--template` (or `-t`) option with the main export command:

```bash
export-for-ai --template <template_name> <directory_path>
```
Example:
```bash
export-for-ai -t light C:\Users\username\MyProject
```

**Available templates:**

*   **`default`**: This is the standard template, providing a comprehensive set of ignore patterns for common files and directories (like `.git`, `__pycache__`, `node_modules/`, build artifacts, various OS-specific files, IDE folders, and common binary file types like images). It is used automatically if no template is specified.
*   **`light`**: This template is designed for a more minimal export, suitable when you want to focus primarily on source code. It includes all patterns from the `default` template but **adds further exclusions** for common documentation directories (`docs/`, `examples/`, `samples/`), test directories (`tests/`, `test/`, `spec/`), and Markdown files (`*.md`).

### How Templates and Local `.exportignore` Interact

1.  **Template First**: When you run `export-for-ai`, it first loads all ignore patterns from the specified template (or the `default` template if none is chosen).
2.  **Local Customization**: Then, it looks for an `.exportignore` file in your project's root directory. If found, any patterns defined in your local `.exportignore` are **added** to the list of patterns from the template.
3.  **Combined Effect**: The final set of ignore rules is the combination of both the template's patterns and your local `.exportignore` patterns. This allows you to rely on a template for general exclusions while fine-tuning the export for your specific project needs.

This means your local `.exportignore` file can be used to:
*   Add more specific exclusions not covered by the template.
*   (Currently, PathSpec does not support direct un-ignoring of patterns that were previously ignored by a more general pattern in the same spec. To include something that a template might exclude, you would need to customize the template or use a more specific pattern that isn't overridden.)

### Pattern Syntax and Examples

The patterns in `.exportignore` are relative to the root directory of your project. Use glob patterns for flexible matching.

#### 1. Exclude an Entire Folder
To exclude a folder and all its contents, add the folder name followed by a slash:
```
node_modules/
my_build_outputs/
```

#### 2. Exclude a Specific File
To exclude a specific file, simply write its relative path:
```
config/settings.py
src/legacy_code.js
```

#### 3. Exclude Files or Folders Matching a Pattern
You can use glob patterns to match multiple files or directories:

- **Exclude all folders starting with `exported-from-`:**
  ```
  exported-from-*/
  ```
- **Exclude all files ending with `.bak`:**
  ```
  *.bak
  ```
- **Exclude all log files in any directory:**
  ```
  **/*.log
  ```
- **Exclude specific file types in a directory and its subdirectories:**
  ```
  assets/images/*.jpg
  assets/images/**/*.png
  ```

### Notes

- **Pattern Syntax Details**:
  - `folder/` ignores a directory named `folder` and all its contents.
  - `*.ext` ignores all files with the `.ext` extension in the current directory. Use `**/*.ext` to ignore them in any directory.
  - `!pattern` (negation): PathSpec, the library used, supports negation patterns. If a file matches a negated pattern and an earlier non-negated pattern, it will be included. If it matches a negated pattern and a later non-negated pattern, it will be excluded. Generally, place negations after general exclusions:
    ```
    *.log       # Ignore all logs
    !debug.log  # But include debug.log
    ```
- **Verification**: Check the log output when `export-for-ai` runs. It will indicate which template is being used and if a local `.exportignore` file is found and loaded. Verbose logging (if enabled) might show specific files being skipped.
- **Default Behavior**: If no template is specified, the `default` template is used. If no local `.exportignore` file is found, only the template patterns are used.

By understanding and utilizing ignore templates and the `.exportignore` file, you can precisely control what content is included in your export, ensuring that only relevant files are processed and shared.
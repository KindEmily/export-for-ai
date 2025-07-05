# API Reference

## Web API Endpoints

### Configuration Management

#### GET /api/config
Returns current configuration settings.

**Response:**
```json
{
  "export_destination": "string",
  "repositories": ["array", "of", "paths"],
  "assets_to_copy": ["array", "of", "assets"]
}
```

#### POST /api/config
Updates configuration settings.

**Request Body:**
```json
{
  "export_destination": "string",
  "repositories": ["array", "of", "paths"],
  "assets_to_copy": ["array", "of", "assets"]
}
```

**Response:**
```json
{
  "status": "success" | "error",
  "message": "string" // Only present on error
}
```

### Export Operations

#### POST /api/run-export
Executes export process with real-time streaming logs.

**Request Body:**
```json
{
  "export_destination": "string",
  "repositories": ["array", "of", "paths"],
  "assets_to_copy": ["array", "of", "assets"]
}
```

**Response:**
Server-Sent Events stream with `text/event-stream` content type.

**Event Format:**
```
data: [LOG_LEVEL] Log message content\n\n
```

**Log Levels:**
- `Starting process...`
- `Processing repository: {path}`
- `Generated export file: {filename}`
- `Copied '{filename}' to {destination}`
- `[ERROR] Error description`
- `[WARN] Warning message`
- `All tasks completed.`

## CLI Interface

### Commands

#### export-for-ai <directory_path>
Exports a single directory to AI-friendly format.

**Arguments:**
- `directory_path`: Absolute path to directory to export

**Output:**
- Creates `exported-from-{folder_name}/` directory
- Generates `project-{folder_name}.md` with structured content
- Copies content to system clipboard

#### export-for-ai --config <config_path>
Batch processes multiple repositories from configuration file.

**Arguments:**
- `config_path`: Path to JSON configuration file

**Configuration File Format:**
```json
{
  "export_destination": "/path/to/output/directory",
  "repositories": [
    "/path/to/repo1",
    "/path/to/repo2"
  ],
  "assets_to_copy": [
    "/path/to/asset1",
    "/path/to/asset2"
  ]
}
```

#### efa <directory_path>
Alternative command name for export-for-ai.

## System Tray Interface

### Hotkeys

#### Ctrl+Shift+Q
Opens web UI in default browser.

#### Ctrl+Shift+E
Triggers export process using current ui_config.json settings.

### Menu Options

#### Open UI
Opens web interface at http://127.0.0.1:8000

#### Run Export
Executes export process with current configuration

#### Quit
Shuts down system tray application and web server

## Python API

### Core Functions

#### export_folder_content(path: str) -> str
Extracts and formats all file contents from directory.

**Parameters:**
- `path`: Directory path to export

**Returns:**
- Formatted markdown string with file contents

**Raises:**
- `OSError`: Directory access issues
- `UnicodeDecodeError`: File encoding issues (handled gracefully)

#### get_tree_structure(path: str) -> str
Generates visual directory tree representation.

**Parameters:**
- `path`: Directory path to visualize

**Returns:**
- Tree structure as formatted string

#### parse_ignore_file(directory: str) -> pathspec.PathSpec
Parses .exportignore file and returns pattern matcher.

**Parameters:**
- `directory`: Directory containing .exportignore file

**Returns:**
- PathSpec object for pattern matching

#### should_include_item(item: str, spec: pathspec.PathSpec) -> bool
Determines if file/directory should be included in export.

**Parameters:**
- `item`: Relative path to test
- `spec`: PathSpec object with ignore patterns

**Returns:**
- True if item should be included, False otherwise

#### process_single_repository(directory_path: str) -> Optional[str]
Processes single repository and returns generated markdown file path.

**Parameters:**
- `directory_path`: Repository path to process

**Returns:**
- Path to generated markdown file or None on error

### Configuration Classes

#### Config (Pydantic Model)
```python
class Config(BaseModel):
    export_destination: str
    repositories: List[str]
    assets_to_copy: Optional[List[str]] = []
```

## File Format Specifications

### Generated Markdown Structure

```markdown
# Previous step

# The goal

# Core Design Philosophy
[Template content with development principles]

# SolutionTreeView
```
[Directory tree using anytree visualization]
```

# Entire Solution Code start
[File contents with headers]
# EntireSolution Code end
```

### .exportignore Format

Follows gitignore syntax with pathspec library:

```
# Comments start with #
__pycache__/
*.py[cod]
.DS_Store
.git/**
*.log
!important.txt  # Negation patterns
```

### ui_config.json Format

```json
{
  "export_destination": "C:\\path\\to\\export\\directory",
  "repositories": [
    "C:\\path\\to\\repo1",
    "C:\\path\\to\\repo2"
  ],
  "assets_to_copy": [
    "C:\\path\\to\\file.txt",
    "C:\\path\\to\\directory"
  ]
}
```

## Error Codes and Messages

### Common Errors

#### Directory Validation
- `"Error: '{path}' is not a valid directory"`
- `"Export destination '{path}' is not a valid directory"`

#### File Processing
- `"Error reading {file}: {error}"`
- `"Binary or unreadable file"`
- `"Permission denied: {path}"`

#### Configuration
- `"Could not read ui_config.json: {error}"`
- `"Config file not found: {path}"`
- `"Error decoding JSON from config file: {path}"`

#### Server Operations
- `"Failed to start server, port might be in use"`
- `"Could not start Web UI: Port 8000 is likely in use"`
- `"Failed to start or connect to the server"`
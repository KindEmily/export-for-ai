# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Export-for-AI is a tool that exports codebases for AI processing (ChatGPT, Claude, etc.). It provides both CLI and GUI interfaces with systray integration.

## Architecture

The project uses a multi-interface architecture:

### Core Components
- **src/export_for_ai/main.py** - CLI entry point and core export logic
- **app_main.py** - Batch processing logic for multiple repositories
- **systray_app.py** - System tray application with hotkey support
- **web_ui.py** - FastAPI web interface for GUI management

### Key Modules
- **folder_exporter.py** - Handles file content extraction and minification
- **tree_visualizer.py** - Generates directory tree structures
- **ignore_parser.py** - Processes .exportignore files (similar to .gitignore)
- **section_manager.py** - Manages content sections and templates

## Common Commands

### Development Setup
```bash
# Using Makefile (recommended)
make install          # Auto-detect Poetry/pip and install
make install-poetry   # Install with Poetry
make install-pip     # Install with pip

# Manual installation
poetry install
# OR
python -m pip install -e .
```

### Running the Application
```bash
# Using Makefile (recommended)
make run-systray     # Start system tray app (main interface)
make run-web         # Start web UI
make run-cli         # Test CLI with sample project
make start           # Install and run systray in one command

# Manual execution
python systray_app.py  # System tray with hotkeys
python web_ui.py       # Web UI on http://127.0.0.1:8000
export-for-ai <path>   # CLI usage
efa <path>            # Alternative CLI command
```

### Maintenance Commands
```bash
make reinstall       # Clean and reinstall dependencies (after code changes)
make clean           # Clean temporary files and build artifacts
make test            # Run manual tests
make version         # Show version information
make help            # Show all available commands
```

### Testing
No formal test suite exists. Test manually with:
```bash
# Test CLI
python -m export_for_ai test_project/

# Test web UI
python web_ui.py

# Test system tray
python systray_app.py
```

## Configuration

### ui_config.json
Main configuration file containing:
- `export_destination` - Where to save exported files
- `repositories` - List of repository paths to process
- `assets_to_copy` - Additional files/folders to copy

### config.yaml
Template configuration for project metadata sections.

### .exportignore
Gitignore-style file to exclude files/directories from export.

## Key Features

### Export Process
1. **Tree Structure Generation** - Creates visual directory tree
2. **Content Extraction** - Processes files with respect to .exportignore
3. **Code Minification** - Removes excess whitespace while preserving structure
4. **Markdown Generation** - Creates project-{folder_name}.md with structured content
5. **Clipboard Integration** - Automatically copies content to clipboard

### Multiple Interfaces
- **CLI** - Direct command-line usage
- **Web UI** - Browser-based interface with real-time progress
- **System Tray** - Background service with global hotkeys

## Development Notes

### Dependencies
- **Core**: pathspec, anytree, pyyaml, pyperclip
- **GUI**: fastapi, uvicorn, pystray, pynput, Pillow
- **Utilities**: requests

### Entry Points
- `efa` command points to `systray_app:main`
- Web UI runs on port 8000
- System tray provides global hotkeys

### File Structure
```
exported-from-{folder_name}/
├── project-{folder_name}.md    # Main export file
├── project_structure.txt       # Tree structure only
└── project_contents.md         # Code contents only
```

## Architecture Patterns

### Export Flow
1. Validate input directory
2. Create temporary export directory
3. Generate tree structure using anytree
4. Export folder contents with ignore patterns
5. Combine into final markdown with template sections
6. Copy to clipboard and clean up temp files

### Multi-Repository Processing
The system can process multiple repositories in batch mode, copying all generated markdown files to a central destination directory.

### Error Handling
- Comprehensive logging throughout all components
- Graceful fallbacks for missing assets (generates placeholder icons)
- Crash logging for system tray application

## Best Practices and Tools

### Documentation
- Use mermaid diagrams in .md files for visualization 
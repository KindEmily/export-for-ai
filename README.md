# Export-for-AI

![usage gif](https://github.com/KindEmily/export-for-ai/blob/main/demo/export-for-ai-usage.gif?raw=true)

## Overview

Export-for-AI streamlines the process of sharing codebases with AI assistants like ChatGPT, Claude, or other AI development tools. Instead of manually copying files or struggling with context limitations, Export-for-AI automatically packages your entire project into a structured, AI-friendly format.

## Key Features

### Multiple Interface Options
- **Command Line Interface**: Quick single-directory exports via terminal
- **Web Interface**: Browser-based dashboard for managing multiple repositories
- **System Tray Integration**: Background service with global hotkeys for instant access

### Intelligent Content Processing
- **Smart Filtering**: Automatically excludes build artifacts, dependencies, and irrelevant files
- **Custom Ignore Patterns**: `.exportignore` file support for project-specific exclusions
- **Directory Tree Visualization**: Clear project structure overview for AI context
- **Code Minification**: Reduces file sizes while preserving code readability

### Batch Processing Capabilities
- **Multi-Repository Support**: Process multiple projects simultaneously
- **Asset Management**: Include additional files like documentation, configs, or datasets
- **Centralized Output**: Aggregate all exports in a single destination folder

### Seamless Integration
- **Automatic Clipboard Copy**: Exported content ready for immediate pasting
- **Real-time Progress Tracking**: Live updates during export process
- **Global Hotkeys**: Instant access with Ctrl+Shift+E (export) and Ctrl+Shift+Q (UI)

## Use Cases

### Individual Developers
- Share specific features or bug fixes with AI assistants
- Get code reviews on entire modules or projects
- Quickly export proof-of-concepts for AI analysis

### Development Teams
- Standardize code sharing processes across team members
- Maintain consistent export formats for AI-assisted development
- Batch process multiple microservices or components

### Code Analysis & Documentation
- Generate AI-powered documentation from codebase exports
- Perform cross-project code analysis
- Create training datasets from multiple repositories

## Getting Started

### Installation
```bash
git clone https://github.com/KindEmily/export-for-ai.git
cd export-for-ai
python -m pip install -e .
```

### Quick Start
```bash
# Export single directory
export-for-ai /path/to/your/project

# Launch web interface
python web_ui.py
# Navigate to http://127.0.0.1:8000

# Start system tray (background service)
python systray_app.py
```

### Basic Usage
1. **CLI Export**: Point the tool at your project directory
2. **Web Dashboard**: Configure multiple repositories and export settings
3. **System Tray**: Use hotkeys for instant exports while working

## Export Output

Each export generates:
- **project-{name}.md**: Complete project export with structure and code
- **Directory tree visualization**: Clear project hierarchy
- **Filtered content**: Only relevant files based on ignore patterns
- **Clipboard integration**: Ready for immediate AI assistant use

## Project Structure Control

### .exportignore File
Control what gets exported using gitignore-style patterns:

```
# Exclude build artifacts
dist/
build/
__pycache__/

# Exclude dependencies
node_modules/
venv/

# Exclude logs and temp files
*.log
*.tmp
```

### Default Exclusions
The tool automatically excludes common unnecessary files:
- Build outputs and compiled files
- Version control directories
- IDE configuration files
- Dependency directories
- Log files and temporary data

## Documentation

For detailed technical information, see:
- [Architecture Overview](docs/architecture.md) - System design and component structure
- [Technical Implementation](docs/technical-implementation.md) - Implementation details and algorithms
- [API Reference](docs/api-reference.md) - Complete API documentation
- [Development Guide](docs/development-guide.md) - Developer setup and contribution guidelines

## Support

For help with installation, usage, or troubleshooting:
- Check the [Development Guide](docs/development-guide.md) for common issues
- Review the [API Reference](docs/api-reference.md) for configuration options
- Submit issues on the GitHub repository
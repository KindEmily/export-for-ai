# Architecture

## Overview

Export-for-AI implements a multi-interface architecture supporting CLI, web UI, and system tray interactions for exporting code repositories to AI-friendly formats.

## Component Architecture

```mermaid
graph TB
    CLI[CLI Interface<br/>main.py] --> Core[Core Logic<br/>app_main.py]
    Web[Web Interface<br/>web_ui.py] --> Core
    Tray[System Tray UI<br/>systray_app.py] --> Core
    
    Core --> FE[folder_exporter<br/>- File content<br/>- Minification]
    Core --> TV[tree_visualizer<br/>- Directory tree view<br/>- anytree integration]
    Core --> IP[ignore_parser<br/>- .exportignore<br/>- Pattern matching]
    
    FE --> Output[Export Output]
    TV --> Output
    IP --> Output
    
    style CLI fill:#e1f5fe
    style Web fill:#f3e5f5
    style Tray fill:#e8f5e8
    style Core fill:#fff3e0
    style Output fill:#ffebee
```

## Data Flow

### Export Process

```mermaid
flowchart TD
    Start[Directory Input] --> Validate[Input Validation]
    Validate --> Parse[Parse .exportignore]
    Parse --> Tree[Generate Tree Structure<br/>using anytree]
    Tree --> Extract[Extract File Contents<br/>with filtering]
    Extract --> Assemble[Assemble Markdown<br/>tree + content + template]
    Assemble --> Output[Write Files & Clipboard]
    Output --> End[Export Complete]
    
    style Start fill:#e3f2fd
    style Validate fill:#fff3e0
    style Parse fill:#f3e5f5
    style Tree fill:#e8f5e8
    style Extract fill:#ffebee
    style Assemble fill:#fce4ec
    style Output fill:#e0f2f1
    style End fill:#e8f5e8
```

### Configuration Flow

```mermaid
graph LR
    Config[ui_config.json] --> WebUI[Web UI]
    WebUI --> FastAPI[FastAPI Endpoints]
    FastAPI --> Batch[Batch Processing]
    
    Config --> SysTray[System Tray]
    SysTray --> Hotkeys[Hotkey Triggers]
    Hotkeys --> Export[Background Export]
    
    style Config fill:#e3f2fd
    style WebUI fill:#f3e5f5
    style SysTray fill:#e8f5e8
    style Export fill:#fff3e0
```

## Core Components

### Export Engine (`src/export_for_ai/`)
- **folder_exporter.py**: File content extraction with ignore pattern support
- **tree_visualizer.py**: Directory tree visualization using anytree
- **ignore_parser.py**: .exportignore file parsing with pathspec
- **main.py**: CLI interface and export orchestration

### Interface Layer
- **app_main.py**: Batch processing coordinator
- **web_ui.py**: FastAPI server for web interface
- **systray_app.py**: System tray integration with global hotkeys

### Frontend
- **templates/index.html**: Single-page web application
- Real-time log streaming via Server-Sent Events
- Repository and asset management interface

## Key Design Patterns

### Separation of Concerns
- Export logic isolated from interface implementations
- Configuration management centralized
- Error handling consistent across interfaces

### Plugin-like Architecture
- Each interface (CLI, Web, Systray) can operate independently
- Shared core logic through app_main.py
- Modular component design

### Streaming Architecture
- Real-time log output for web interface
- Asynchronous processing for non-blocking operations
- Background thread execution for system tray

## Dependencies

### Core Dependencies
- **pathspec**: .exportignore pattern matching
- **anytree**: Directory tree structure generation
- **pyyaml**: Configuration file parsing
- **pyperclip**: System clipboard integration

### Interface Dependencies
- **FastAPI/uvicorn**: Web server framework
- **pystray**: System tray integration
- **pynput**: Global hotkey support
- **Pillow**: Icon image processing

## Configuration Management

### ui_config.json Structure
```json
{
  "export_destination": "string",
  "repositories": ["array", "of", "paths"],
  "assets_to_copy": ["array", "of", "assets"]
}
```

### Runtime Configuration
- Default ignore patterns in ignore_parser.py
- Project-specific .exportignore files
- Template sections via config.yaml

## Error Handling Strategy

### Graceful Degradation
- Missing icons fallback to generated placeholders
- Encoding errors handled with descriptive messages
- Network failures in web UI display user-friendly errors

### Logging Strategy
- Structured logging throughout all components
- Crash logging for system tray application
- Real-time log streaming for web interface

## Output Structure

### Generated File Hierarchy

```mermaid
graph TD
    Root[exported-from-{folder_name}/] --> Main[project-{folder_name}.md<br/>📄 Main export file]
    Root --> Tree[project_structure.txt<br/>🌳 Tree structure only]  
    Root --> Contents[project_contents.md<br/>📝 Code contents only]
    
    Main --> Sections[Combined Sections:<br/>- Previous step<br/>- The goal<br/>- Design Philosophy<br/>- Solution Tree View<br/>- Entire Solution Code]
    
    style Root fill:#e3f2fd
    style Main fill:#ffebee
    style Tree fill:#f3e5f5
    style Contents fill:#e8f5e8
    style Sections fill:#fff3e0
```

## Processing Sequence

### Export Flow Sequence

```mermaid
sequenceDiagram
    participant CLI as CLI/Web/Tray
    participant Core as app_main.py
    participant FE as folder_exporter
    participant TV as tree_visualizer
    participant IP as ignore_parser
    
    CLI->>Core: process_single_repository()
    Core->>IP: parse_ignore_file()
    IP-->>Core: PathSpec patterns
    Core->>TV: get_tree_structure()
    TV->>IP: should_include_item()
    TV-->>Core: tree structure
    Core->>FE: export_folder_content()
    FE->>IP: should_include_item()
    FE-->>Core: file contents
    Core->>Core: export_project_md()
    Core-->>CLI: markdown file path
```
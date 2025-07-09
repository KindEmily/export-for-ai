# Export-for-AI Makefile
# Compatible with Windows (WSL/Git Bash) and Unix systems

# Variables
PYTHON := python
PIP := pip
POETRY := poetry

# Default target
.DEFAULT_GOAL := help

# Colors for output (works in Git Bash and WSL)
GREEN := \033[32m
YELLOW := \033[33m
BLUE := \033[34m
RED := \033[31m
NC := \033[0m # No Color

.PHONY: help install install-poetry install-pip update run-systray run-web run-cli test clean check-python

## Show this help message
help:
	@echo "$(BLUE)Export-for-AI Development Commands$(NC)"
	@echo ""
	@echo "$(GREEN)Installation:$(NC)"
	@echo "  make install-poetry    Install dependencies using Poetry"
	@echo "  make install-pip      Install dependencies using pip"
	@echo "  make install          Auto-detect and install (Poetry preferred)"
	@echo "  make reinstall        Clean and reinstall dependencies"
	@echo ""
	@echo "$(GREEN)Running the Application:$(NC)"
	@echo "  make run-systray      Start system tray application (auto-detects Poetry)"
	@echo "  make run-web          Start web UI server (auto-detects Poetry)"
	@echo "  make run-cli          Run CLI with test project (auto-detects Poetry)"
	@echo ""
	@echo "$(GREEN)Development:$(NC)"
	@echo "  make test             Run manual tests"
	@echo "  make clean            Clean temporary files"
	@echo "  make check-python     Check Python installation"
	@echo "  make version          Show version information"
	@echo ""
	@echo "$(YELLOW)Hotkeys when systray is running:$(NC)"
	@echo "  Ctrl+Shift+Q         Open web UI"
	@echo "  Ctrl+Shift+E         Run export process"

## Check Python installation
check-python:
	@echo "$(BLUE)Checking Python installation...$(NC)"
	@$(PYTHON) --version || (echo "$(RED)Python not found! Please install Python 3.10+$(NC)" && exit 1)
	@echo "$(GREEN)Python found and working$(NC)"

## Install dependencies using Poetry (preferred)
install-poetry: check-python
	@echo "$(BLUE)Installing with Poetry...$(NC)"
	@command -v poetry >/dev/null 2>&1 || (echo "$(RED)Poetry not found! Installing Poetry...$(NC)" && curl -sSL https://install.python-poetry.org | python3 -)
	@poetry install
	@echo "$(GREEN)Installation complete with Poetry$(NC)"

## Install dependencies using pip
install-pip: check-python
	@echo "$(BLUE)Installing with pip...$(NC)"
	@$(PIP) install -e .
	@echo "$(GREEN)Installation complete with pip$(NC)"

## Auto-detect installation method (Poetry preferred)
install: check-python
	@if command -v poetry >/dev/null 2>&1; then \
		echo "$(BLUE)Poetry detected, using Poetry installation...$(NC)"; \
		$(MAKE) install-poetry; \
	else \
		echo "$(BLUE)Poetry not found, using pip installation...$(NC)"; \
		$(MAKE) install-pip; \
	fi

## Clean and reinstall dependencies (useful after code changes)
reinstall: clean
	@echo "$(BLUE)Reinstalling dependencies...$(NC)"
	@if command -v poetry >/dev/null 2>&1; then \
		echo "$(BLUE)Reinstalling with Poetry...$(NC)"; \
		poetry install; \
	else \
		echo "$(BLUE)Reinstalling with pip...$(NC)"; \
		$(PIP) install -e .; \
	fi
	@echo "$(GREEN)Reinstallation complete!$(NC)"
	@echo "$(YELLOW)Restart the systray app to use the updated version$(NC)"

## Start system tray application (main application)
run-systray: check-python
	@echo "$(BLUE)Starting Export-for-AI System Tray...$(NC)"
	@echo "$(YELLOW)Use Ctrl+Shift+Q to open UI, Ctrl+Shift+E to export$(NC)"
	@echo "$(YELLOW)Press Ctrl+C to stop$(NC)"
	@if command -v poetry >/dev/null 2>&1; then \
		echo "$(BLUE)Using Poetry...$(NC)"; \
		poetry run python systray_app.py; \
	else \
		$(PYTHON) systray_app.py; \
	fi

## Start web UI server
run-web: check-python
	@echo "$(BLUE)Starting Export-for-AI Web UI...$(NC)"
	@echo "$(YELLOW)Open http://127.0.0.1:8000 in your browser$(NC)"
	@echo "$(YELLOW)Press Ctrl+C to stop$(NC)"
	@if command -v poetry >/dev/null 2>&1; then \
		echo "$(BLUE)Using Poetry...$(NC)"; \
		poetry run python web_ui.py; \
	else \
		$(PYTHON) web_ui.py; \
	fi

## Run CLI with test project
run-cli: check-python
	@echo "$(BLUE)Running CLI export on test project...$(NC)"
	@if [ ! -d "test_project" ]; then \
		echo "$(YELLOW)Creating test project...$(NC)"; \
		mkdir -p test_project; \
		echo "print('Hello from test project')" > test_project/test.py; \
		echo "# Test Project" > test_project/README.md; \
		echo "*.log" > test_project/.exportignore; \
	fi
	@if command -v poetry >/dev/null 2>&1; then \
		echo "$(BLUE)Using Poetry...$(NC)"; \
		poetry run python -m export_for_ai test_project/; \
	else \
		$(PYTHON) -m export_for_ai test_project/; \
	fi
	@echo "$(GREEN)CLI export complete! Check the exported-from-test_project/ directory$(NC)"

## Run manual tests
test: check-python
	@echo "$(BLUE)Running manual tests...$(NC)"
	@echo "$(YELLOW)Testing CLI interface...$(NC)"
	@$(MAKE) run-cli
	@echo ""
	@echo "$(YELLOW)Testing import functionality...$(NC)"
	@$(PYTHON) -c "import export_for_ai; print('✓ Core module imports successfully')"
	@$(PYTHON) -c "import app_main; print('✓ App main imports successfully')"
	@$(PYTHON) -c "import web_ui; print('✓ Web UI imports successfully')"
	@$(PYTHON) -c "import systray_app; print('✓ Systray app imports successfully')"
	@echo "$(GREEN)All tests passed!$(NC)"

## Clean temporary files and build artifacts
clean:
	@echo "$(BLUE)Cleaning temporary files...$(NC)"
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "exported-from-*" -exec rm -rf {} + 2>/dev/null || true
	@rm -f systray_crash.log 2>/dev/null || true
	@echo "$(GREEN)Cleanup complete$(NC)"

## Quick start - install and run systray
start: install run-systray

## Show version information
version: check-python
	@echo "$(BLUE)Version Information:$(NC)"
	@echo "Python: $$($(PYTHON) --version)"
	@if command -v poetry >/dev/null 2>&1; then echo "Poetry: $$(poetry --version)"; fi
	@echo "Git: $$(git describe --tags --always 2>/dev/null || echo 'no git info')"
	@echo "Export-for-AI: $$(grep version pyproject.toml | head -1 | cut -d'\"' -f2)"

## Show system information
info: version
	@echo ""
	@echo "$(BLUE)System Information:$(NC)"
	@echo "OS: $$(uname -s 2>/dev/null || echo 'Windows')"
	@echo "Architecture: $$(uname -m 2>/dev/null || echo 'unknown')"
	@echo "Current directory: $$(pwd)"

# Windows-specific targets
ifeq ($(OS),Windows_NT)
## Windows: Install using Windows Python launcher
install-windows:
	@echo "$(BLUE)Installing on Windows...$(NC)"
	@py -m pip install -e .
	@echo "$(GREEN)Windows installation complete$(NC)"

## Windows: Run systray with Windows Python launcher
run-systray-windows:
	@echo "$(BLUE)Starting Export-for-AI System Tray (Windows)...$(NC)"
	@py systray_app.py
endif
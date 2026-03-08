# Agora Automation Engineer Assignment

This repository contains the automation assignment for the Agora Automation Engineer position. It implements a robust, scalable test automation framework using Python and Pytest, covering both UI automation (using Selenium against SauceDemo) and API automation (against JSONPlaceholder).

## Purpose of this Project

The primary goal of this project is to demonstrate an enterprise-ready test automation architecture. It is not just about writing scripts that pass, but about building a framework that can scale across multiple domains (UI, API, Mobile) and integrate seamlessly with modern CI/CD pipelines and reporting tools.

## Scalability and Architecture

This project is built with scalability at its core. You will notice that the `framework/` directory is deeply nested and modularized. 

**Important Note:** *Some directories and files (like `framework/reporting/testrail`, `framework/mobile`, or empty `__init__.py` files) may currently be empty or act as dummy placeholders. They are explicitly included to demonstrate how this project is designed to scale up. By establishing these architectural boundaries early, new engineers can easily add mobile app tests, specialized API data models, or third-party integrations (like Slack or TestRail) exactly where they belong, without cluttering the core framework logic.*

### Key Architectural Decisions:
- **Separation of Concerns:** Distinct boundaries between the `framework` (core logic, clients, clients, locators) and the `tests` (actual test cases).
- **Page Object Model (POM):** UI tests leverage POM with fluent interfaces and custom decorators for clean, readable test steps.
- **Dependency Management:** Built with `uv` for blistering fast, reproducible, and strictly isolated environment management.
- **Centralized Configuration:** A unified approach to environment variables and configuration via Pytest fixtures.

## How to Fetch and Run Locally

This project uses `uv` as its Python package and environment manager for maximum speed and reliability.

### 1. Prerequisites
- **Python 3.13+**: [Download Python](https://www.python.org/downloads/)
- **uv**: [Download & Install uv](https://docs.astral.sh/uv/getting-started/installation/)

### 2. Setup

Clone the repository and sync the dependencies. `uv` will automatically create the virtual environment (`.venv`) and install everything required by `pyproject.toml` and `uv.lock`.

```bash
git clone <repository_url>
cd AgoraAutomationEngineerAsignment
uv sync
```

### 3. Execution

You can run the tests using the `uv run` command, which ensures Pytest is executed within the project's isolated environment.

**Run All Tests:**
```bash
uv run pytest
```

**Run Only UI Tests:**
```bash
uv run pytest tests/ui
```

**Run Only API Tests:**
```bash
uv run pytest tests/api
```

## Continuous Integration

This project includes a GitHub Actions workflow:
- **Code Quality (`code-quality-check.yml`)**: Runs `flake8` linting and Pytest collection to ensure code health and prevent syntax errors from being merged.

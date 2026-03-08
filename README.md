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

## Enterprise Testing Capabilities

This framework goes beyond basic automation scripts by implementing several enterprise-grade features designed for massive scalability, traceability, and easy maintenance:

### 1. Extensible Pytest Markers
Tests are decorated with custom markers (configured in `pyproject.toml` and `helper_functions.py`):
- `@pytest.mark.case_id("C1001")`: Links the test method directly to a Test Management System (like TestRail). This enables automated result reporting and metric tracking across releases.
- `@pytest.mark.test_name("E2E Checkout Flow")`: Provides a rich, human-readable name for reporting tools like Allure or Slack, drastically improving log readability.
- `@pytest.mark.dependency(depends=["test_name"])`: Prevents cascading failures. For instance, if an API `POST` test fails, subsequent `GET`/`PUT`/`DELETE` tests are intelligently skipped, saving execution time and reducing noise in CI failure logs.

### 2. Automated Workspace Hygiene (Screenshot Cleanup)
UI test failures automatically capture full-page screenshots for debugging. To prevent developers' local environments from bloating over time, a custom `pytest_sessionfinish` hook in `conftest.py` automatically detects local executions and wipes the `screenshots/` directory at the end of the run. When running in CI (GitHub Actions), this hook leaves the directory intact so the images can be uploaded as build artifacts.

## Continuous Integration

This project includes a GitHub Actions workflow:
- **Code Quality (`code-quality-check.yml`)**: Runs `uvx flake8` linting and Pytest collection to ensure code health and prevent syntax errors from being merged, fetching tools on the fly without cluttering the project dependency tree.

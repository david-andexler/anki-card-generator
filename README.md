# Template - Python, Poetry, Docker, Devcontainers

This repository provides a template for developing Python applications using **Poetry** for dependency management, **Docker** for containerization, and **Devcontainers** for a seamless development environment in **VS Code**. It includes configurations for local development, testing, and production deployment.

## Features

- **Python 3.13**: Latest Python version with modern features.
- **Poetry**: Dependency and environment management.
- **Docker Compose**: Pre-configured services for local development and documentation.
- **Devcontainers**: Ready-to-use development environment in VS Code.
- **Sphinx Documentation**: Build and serve project documentation.
- **Pre-commit Hooks**: Automated linting and formatting with tools like `ruff` and `mypy`.
- **GitHub Actions**: CI/CD pipeline for linting, testing, and building.

## Directory Structure

- app: Application source code.
- compose: Docker Compose configurations for local and production environments.
  - `local/`: Local development services (e.g., `local-app`, docs).
  - `production/`: Production-ready services (e.g., `prod-app`, `postgres`).
- docs: Sphinx documentation source files.
- .devcontainer: Devcontainer configuration for VS Code.
- .envs: Environment variable files for local and production environments.

## Setup

### Prerequisites

1. Install **Docker**:
   - [Docker Desktop](https://www.docker.com/products/docker-desktop)
   - Verify installation: `docker --version`

2. Install **VS Code** (optional, recommended):
   - [Download VS Code](https://code.visualstudio.com/download)
   - Install the **Devcontainers** extension: `ms-vscode-remote.remote-containers`

### Local Development

1. **Using Devcontainers**:
   - Open the project in VS Code.
   - Run `Dev Containers: Rebuild and Reopen in Container` from the Command Palette.

2. **Without Devcontainers**:
   - Start the application:
     ```bash
     docker compose -f compose/local/docker-compose.local.yml up
     ```

### Documentation

- Build and serve documentation:
  ```bash
  docker compose -f compose/local/docker-compose.docs.yml up
  ```

## Development Workflow

- **Install Dependencies**:
  Inside the devcontainer:
  ```bash
  poetry add <package-name>
  poetry install
  ```

- **Linting**:
  ```bash
  make lint
  ```

- **Type Checking**:
  ```bash
  make typecheck
  ```

- **Run Tests**:
  ```bash
  make test
  ```

- **Test Coverage**:
  ```bash
  coverage run -m pytest
  coverage html
  open htmlcov/index.html
  ```

## Deployment

- Modify .production files for production configurations.
- Use docker-compose.production.yml for production builds.

## CI/CD

- **GitHub Actions**: Automatically runs linting, testing, and builds on pull requests and pushes to `main` or `master`.

## License

This project is licensed under the MIT License.

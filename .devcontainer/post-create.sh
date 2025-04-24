#!/bin/bash
set -e  # Stop on error
cat .devcontainer/bashrc.override.sh >> ~/.bashrc
git config --global --add safe.directory /app
pre-commit install --install-hooks

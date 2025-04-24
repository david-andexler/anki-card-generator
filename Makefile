# Description: This is the main Makefile for the project.

# Include all makefiles in scripts/ directory
# Within each makefile, the first line should be a comment with the format:
# Description: <description>
# The help target will print the description and the targets in each makefile
# Usage: make help

include $(wildcard scripts/*.mk)

help:
	@echo "Available targets:"
	@for mkfile in $(MAKEFILE_LIST); do \
		filename=$$(basename $$mkfile); \
		desc=$$(awk -F': ' '/^# Description:/ {print $$2; exit}' $$mkfile); \
		echo "\n\033[1;34mFrom $$filename:\033[0m $${desc:-No description}"; \
		awk -F':|#' '/^[a-zA-Z0-9_.-]+:.*?#/ {printf "  \033[1;32m%-20s\033[0m %s\n", $$1, $$3}' $$mkfile; \
	done

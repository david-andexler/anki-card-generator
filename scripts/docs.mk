# Description: Sphinx docs helpers

.PHONY: docs
docs: # Build and serve docs
	docker compose -f compose/local/docker-compose.docs.yml up --build

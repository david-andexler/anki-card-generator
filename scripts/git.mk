# Description: Git/Hub helpers

push: # aliases git push and sets upstream if not set
	@git push --set-upstream origin $(shell git rev-parse --abbrev-ref HEAD)

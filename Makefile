##
 # Makefile
 # ______________________________________________________________________________
 #
 # Created by brightSPARK Labs
 # www.brightsparklabs.com
 ##

# Warn whenever make sees a reference to an undefined variable.
MAKEFLAGS += --warn-undefined-variables
# Disable implicit rules as they were not designed for python.
MAKEFLAGS += --no-builtin-rules

VENV_NAME?=.venv
VENV_ACTIVATE=. $(VENV_NAME)/bin/activate
PYTHON=${VENV_NAME}/bin/python
APP_VERSION=$(shell git describe --always --dirty)

# The below `awk` is a simple variation for self-documenting Makefiles. See:
# https://ricardoanderegg.com/posts/makefile-python-project-tricks/
#
# Basically this allows task documentation to be appended to the task name
# with two hashes and it will be picked up in help output.
.DEFAULT: help
.PHONY: help
help: ## Display this help section
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z\$$/]+.*:.*?##\s/ {printf "\033[36m%-38s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: venv
venv: ${VENV_NAME}/bin/activate  ## Create and update virtual environment.
$(VENV_NAME)/bin/activate: pyproject.toml
	uv sync
	touch ${VENV_NAME}/bin/activate

.PHONY: lint
lint: venv ## Lint all code
	${PYTHON} -m ruff check --config prek/ruff.toml .

.PHONY: format
format: venv ## Format all code
	${PYTHON} -m ruff format --config prek/ruff.toml .

# IMPORTANT: Run this as `make -s precommit` so that the parent make command
# does not interfere with the nested make commands.
.PHONY: precommit
precommit: venv ## Check pre-commit hooks (run as `make -s precommit`).
	$(VENV_NAME)/bin/prek run -c prek.toml

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = {{ cookiecutter.repo_name }}
PYTHON_VERSION = {{ cookiecutter.python_version_number }}

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Delete all compiled Python files
.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete


.PHONY: precommit
precommit:
	uv run --frozen pre-commit run --all-files

## Refresh Python Dependencies
.PHONY: env_refresh
env_refresh:
	uv sync

## Install Python dependencies without updating
.PHONY: env
env:
	uv sync --frozen

.PHONY: paper
paper:
	uv run --frozen quarto render paper/paper.qmd

.PHONY: slides
slides:
	uv run --frozen quarto render slides/slides.qmd

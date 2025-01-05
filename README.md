# Cookie cutter research project

## Setup

Prerequisites:

- the Python package manager uv
- `cookiecutter` package
- an installation of Quarto
- an installation of LaTeX

To install cookiecutter:

```bash
uv tool install cookiecutter
```

To create a new project folder based on this cookie cutter:

```bash
uv tool run cookiecutter https://github.com/aeturrell/cookie-cutter-research-project.git
```

The new project folder will appear within the folder you ran the command in.

## Using the create project

This assumes you are in the project root.

First, run `uv sync` to create the Python environment (it installs into `.venv`)

To create the paper, use `make paper`.

To create the slides, use `make slides`.

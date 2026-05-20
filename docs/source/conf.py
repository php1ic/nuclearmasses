# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

from pathlib import Path
import sys
import tomllib

# Get the root path of the project
ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(ROOT / "src"))

# Project information
with open(ROOT / "pyproject.toml", "rb") as f:
    pyproject = tomllib.load(f)

project = pyproject["project"]["name"]
release = pyproject["project"]["version"]
version = release
copyright = "2026, php1ic"
author = "php1ic"

# General configuration
extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

napoleon_numpy_docstring = True
napoleon_google_docstring = False
autosummary_generate = True

exclude_patterns = []

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# Options for HTML output
html_theme = "furo"

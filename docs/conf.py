"""Sphinx configuration."""
project = "epyfun"
author = "Eduardo Alfonso-Sierra"
copyright = "2020, Eduardo Alfonso-Sierra"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"

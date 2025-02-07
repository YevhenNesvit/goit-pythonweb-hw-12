# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
sys.path.insert(0, os.path.abspath('../../'))

project = 'Contacts API'
copyright = '2025, Yevhen Nesvit'
author = 'Yevhen Nesvit'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",  # Для підтримки Google/Numpy-стилю докстрінгів
    "sphinx.ext.viewcode",
]

autosummary_generate = True
autodoc_default_options = {
    "members": True,
    "undoc-members": True,  # Включає навіть ті, що без докстрінгів
    "private-members": True, # Додає методи, що починаються з "_"
    "special-members": "__init__",  # Додає docstring для `__init__`
    "show-inheritance": True,
}
autoclass_content = "both"  # Включає докстрінги класів і їх `__init__`
autodoc_typehints = "description"  # Виносить тайпхінти в опис

templates_path = ['_templates']
exclude_patterns = []

language = 'uk'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

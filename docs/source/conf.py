# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#

import os
import sys
import django
src_path = os.path.join('..', '..', 'src')
core_path = os.path.abspath(os.path.join(src_path, 'core'))
desktop_path = os.path.abspath(os.path.join(src_path, 'desktop'))
web_path = os.path.abspath(os.path.join(src_path, 'web'))
sys.path.insert(0, core_path)
sys.path.insert(0, desktop_path)
sys.path.insert(0, web_path)
print("\nPath info:")
print("Core path : ", core_path)
print("Desktop path : ", desktop_path)
print("Web path : ", web_path)
print(os.path.dirname(sys.modules['__main__'].__file__), '\n', sep='')
os.environ["DJANGO_SETTINGS_MODULE"] = "network_confrontation_web.settings"
django.setup()


# -- Project information -----------------------------------------------------

project = 'Network Confrontation'
copyright = '2020, ms103'
author = 'ms103'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
import sphinx_rtd_theme

extensions = [
"sphinx.ext.autodoc",
"sphinx.ext.viewcode",
"sphinx_rtd_theme",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
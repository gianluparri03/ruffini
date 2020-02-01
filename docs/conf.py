# Configuration file for the Sphinx documentation builder.

# -- Path setup --------------------------------------------------------------
import os, sys

sys.path.insert(0, os.path.abspath('../src/'))


# -- Project information -----------------------------------------------------
project = 'ruffini'
copyright = '2019, Parri Gianluca'
author = 'Parri Gianluca'
version = 'v1.2'


# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest'
]
autodoc_member_order = 'bysource'
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
language = None
exclude_patterns = []
pygments_style = 'sphinx'


# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']


# -- Options for HTMLHelp output ---------------------------------------------
htmlhelp_basename = 'ruffinidoc'


# -- Options for LaTeX output ------------------------------------------------
latex_elements = {}
latex_documents = [
    (master_doc, 'ruffini.tex', u'ruffini Documentation',
     u'Parri Gianluca', 'manual'),
]


# -- Options for manual page output ------------------------------------------
man_pages = [
    (master_doc, 'ruffini', u'ruffini Documentation',
     [author], 1)
]


# -- Options for Texinfo output ----------------------------------------------
texinfo_documents = [
    (master_doc, 'ruffini', u'ruffini Documentation',
     author, 'ruffini', 'Python implementation of Monomials and Polynomials',
     'Miscellaneous'),
]

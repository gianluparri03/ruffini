import os
import sys
from json import load

sys.path.insert(0, os.path.abspath('../src/'))

# Project information
project = 'ruffini'
copyright = '2019, Parri Gianluca'
author = 'Parri Gianluca'
version = 'v1.2'

# Sphinx configurations
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest'
]

autodoc_member_order = 'bysource'

# HTML Template
html_theme = 'sphinx_rtd_theme'

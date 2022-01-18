# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html


# -- Path setup --------------------------------------------------------------
import os
import sys
d_root = os.path.dirname(
         os.path.dirname(
         os.path.dirname(
         os.path.realpath(__file__))))
sys.path.insert(0, d_root)
sys.path.insert(1, os.path.join(d_root, 'pdvalidate'))
from datetime import datetime as dt
from pdvalidate._version import __version__


# -- Project information -----------------------------------------------------

project = 'pdvalidate'
copyright = f'2022 | S3DEV | version {__version__}'
author = 'M. Englund, J. Berendt'
master_doc = 'index'
version = __version__
release = __version__


# -- General configuration ---------------------------------------------------

html_theme = 'sphinx_rtd_theme'
#exclude_patterns = ['htg__*.rst', 'auth.rst']
extensions = ['sphinx.ext.autodoc', 
              'sphinx.ext.ifconfig', 
              'sphinx.ext.napoleon', 
              'sphinx.ext.todo',
              'sphinx.ext.intersphinx',
              'sphinx_copybutton',
              'sphinx_git',
              'sphinx.ext.viewcode',
              'sphinxcontrib.spelling']
html_copy_source = False
#html_css_files = ['_static/css/s5defs-rules.css']
html_logo = '_static/img/s3dev_tri_white_sm.png'
html_static_path = ['_static']
html_search_language = 'en'
html_show_copyright = True
html_show_sourcelink = False
html_show_sphinx = False
html_title = f'{project} Documentation'
mathjax_path = 'js/mathjax.js'
numfig = True
pygments_style = 'sphinx'
source_suffix = '.rst'
templates_path = ['_templates']
todo_include_todos = True

# -- Spell checker configuration ---------------------------------------------
spelling_lang = 'en_UK'
tokenizer_lang = 'en_UK'
spelling_word_list_filename = 'spellinglist.txt'

# -- Epilog ------------------------------------------------------------------
# These items are included at the end of each source file.
# This is a useful place to keep file paths or variables which are used 
# throughout.

dtme = dt.now().strftime('%d %b %Y')
rst_epilog = f"""

.. |lastupdated| replace:: Last updated: {dtme}

.. include:: _static/css/s5defs.txt

"""


# -*- coding: utf-8 -*-

import sys, os

sys.path.insert(0, os.path.abspath('../../'))
import goslate as module

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.doctest']
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = module.__name__
copyright = module.__copyright__
version = module.__version__
release = version
exclude_patterns = []
add_function_parentheses = True
add_module_names = True
show_authors = True
pygments_style = 'sphinx'
#modindex_common_prefix = []
#keep_warnings = False

# -- Options for HTML output ---------------------------------------------------

html_theme = 'haiku'
# html_theme_options = {'collapsiblesidebar':True}
#html_theme_path = []
# "<project> v<release> documentation".
#html_title = None
#html_short_title = None
#html_logo = None
#html_favicon = None
html_static_path = ['_static']
html_last_updated_fmt = '%Y-%m-%d'
#html_use_smartypants = True
#html_sidebars = {}
#html_additional_pages = {}
html_domain_indices = False
# html_use_index = False
#html_split_index = False
html_show_sourcelink = True
html_show_sphinx = False
html_show_copyright = True
#html_use_opensearch = ''
#html_file_suffix = None
# htmlhelp_basename = 'goslatedoc'

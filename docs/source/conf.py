"""Configuration file for the Sphinx documentation builder."""

import os
from datetime import datetime

import pyml_datasets

# ================================================================================= #
# ----------------------------- Project Configurations ---------------------------- #
# ================================================================================= #
project = "pyml-datasets"
author = pyml_datasets.__author__
release = pyml_datasets.__version__
version = release
year = 2026
current_year = datetime.now().year
year_str = str(year) if current_year == year else f"{year}-{current_year}"
copyright = f"{year_str}, {author}"
source_suffix = {
    ".rst": "restructuredtext",
}

# ================================================================================= #
# --------------------------- RST Substitutions ----------------------------------- #
# ================================================================================= #
_HOME_DESCRIPTION = (
    "Classic tabular datasets in NPZ format for pyml — a machine learning library"
    " built from scratch"
)

rst_prolog = f"""
.. |home_description| replace:: {_HOME_DESCRIPTION}
"""


# ================================================================================= #
# ------------------------------ Canonical URL ------------------------------------ #
# ================================================================================= #
_READTHEDOCS_CANONICAL_URL = os.environ.get("READTHEDOCS_CANONICAL_URL")
_CANONICAL_URL = _READTHEDOCS_CANONICAL_URL or "https://pyml-datasets.readthedocs.io/en/latest/"

# ================================================================================= #
# ----------------------------------- Extensions ---------------------------------- #
# ================================================================================= #
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.doctest",
    "sphinx_autodoc_typehints",
    "sphinx_copybutton",
    "sphinx_design",
    "notfound.extension",
    "sphinxext.opengraph",
    "sphinx_sitemap",
]

# ================================================================================= #
# ------------------------------------ Autodoc ------------------------------------ #
# ================================================================================= #
autodoc_default_options = {
    "member-order": "bysource",
    "undoc-members": False,
    "private-members": False,
    "inherited-members": "object",
    "autosummary": True,
}
autodoc_typehints_format = "short"
autosummary_generate = False

# ================================================================================= #
# ------------------------------------ Napoleon ----------------------------------- #
# ================================================================================= #
napoleon_numpy_docstring = True
napoleon_google_docstring = False
napoleon_include_init_with_doc = False
napoleon_use_rtype = False
napoleon_use_ivar = False
napoleon_custom_sections = [
    ("Attributes", "params_style"),
]

# ================================================================================= #
# ----------------------------- Code Syntax & Styling ----------------------------- #
# ================================================================================= #
toc_object_entries_show_parents = "hide"
pygments_style = "friendly"
default_role = "literal"
add_module_names = False

# ================================================================================= #
# -------------------------- Sphinx Autodoc Typehints ----------------------------- #
# ================================================================================= #
typehints_fully_qualified = False
typehints_use_signature = True
typehints_use_signature_return = True
typehints_defaults = "comma"

# ================================================================================= #
# -------------------------------- Intersphinx ------------------------------------ #
# ================================================================================= #
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
}

# ================================================================================= #
# --------------------------------- CopyButton ------------------------------------ #
# ================================================================================= #
copybutton_prompt_text = r">>> |\$ "
copybutton_prompt_is_regexp = True
copybutton_only_copy_prompt_lines = True

# ================================================================================= #
# ------------------------------- OpenGraph --------------------------------------- #
# ================================================================================= #
ogp_site_url = _CANONICAL_URL
ogp_image = "_static/branding/og-image.png"
ogp_description_length = 200
ogp_type = "website"
ogp_custom_meta_tags = [
    '<meta property="og:image:width" content="1200" />',
    '<meta property="og:image:height" content="630" />',
]

# ================================================================================= #
# ------------------------------- Sphinx Sitemap ---------------------------------- #
# ================================================================================= #
html_baseurl = _CANONICAL_URL
sitemap_url_scheme = "{link}"
sitemap_excludes = [
    "search.html",
    "genindex.html",
]

# ================================================================================= #
# ------------------------------- Sphinx Linkcheck -------------------------------- #
# ================================================================================= #
linkcheck_allowed_redirects = {
    r"https://doi\.org/10\.24432/C5PC7J": r"https://archive\.ics\.uci\.edu/dataset/109/wine",
}

# ================================================================================= #
# -------------------------- Options For Html Output ------------------------------ #
# ================================================================================= #
templates_path = [
    "_templates",
]
html_extra_path = [
    "_extra",
]
exclude_patterns = []

# ================================================================================= #
# ---------------------------- Theme & Branding ----------------------------------- #
# ================================================================================= #
html_theme = "pydata_sphinx_theme"
html_title = "pyml-datasets"
html_context = {
    "default_mode": "light",
}
html_domain_indices = False
html_last_updated_fmt = "%b %d, %Y"
html_copy_source = False

# ================================================================================= #
# --------------------------- Theme Customizations -------------------------------- #
# ================================================================================= #
html_theme_options = {
    "logo": {
        "image_light": "_static/branding/logo.svg",
        "image_dark": "_static/branding/logo-dark.svg",
        "text": "",
    },
    "github_url": "https://github.com/sherzod-juraev/pyml-datasets",
    "show_prev_next": True,
    "navigation_with_keys": True,
    "collapse_navigation": True,
    "show_nav_level": False,
    "navbar_end": ["theme-switcher", "navbar-icon-links"],
}

# ================================================================================= #
# ------------------------------------- CSS Files --------------------------------- #
# ================================================================================= #
html_static_path = [
    "_static",
]
html_css_files = [
    "css/header.css",
    "css/cards.css",
    "css/left_sidebar.css",
    "css/right_sidebar.css",
    "css/breadcrumb.css",
    "css/footer_nav.css",
    "pygments.css",
    "css/code_blocks.css",
    "css/installation.css",
]

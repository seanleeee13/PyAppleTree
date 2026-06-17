import os

extensions = [
    "myst_parser"
]
project = "PyAppleTree"
copyright = "2026, seanleeeee13"
author = "seanleeeee13"
html_theme = "sphinx_rtd_theme"
source_suffix = {
    ".md": "markdown",
}
rtd_language = os.environ.get("READTHEDOCS_LANGUAGE", "en")
root_doc = f"{rtd_language}/index"
master_doc = f"{rtd_language}/index"
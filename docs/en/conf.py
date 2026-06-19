from pygments.lexers import get_lexer_by_name
from sphinx.highlighting import lexers

lexers["pip"] = get_lexer_by_name("bash")
lexers["pipx"] = get_lexer_by_name("bash")
lexers["uv"] = get_lexer_by_name("bash")
lexers["poetry"] = get_lexer_by_name("bash")

extensions = [
    "myst_parser",
    "sphinx_rtd_theme",
    "sphinx_design"
]
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "fieldlist",
    "html_image",
]
project = "PyAppleTree"
copyright = "2026, seanleeeee13"
author = "seanleeeee13"
html_theme = "sphinx_rtd_theme"
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown"
}
language = "en"
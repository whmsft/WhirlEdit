import re

from pygments.lexer import Lexer, include, bygroups, using, this, default
from pygments.token import Text, Comment, Operator, Keyword, Name, String, \
    Punctuation, Generic, Number, Whitespace

class Text(Lexer):
    """
    "Null" lexer, doesn't highlight anything.
    """
    name = 'Text only'
    aliases = ['text']
    filenames = ['*.txt']
    mimetypes = ['text/plain']
    priority = 0.01

    def get_tokens_unprocessed(self, text):
        yield 0, Text, text

    def analyse_text(text):
        return TextLexer.priority
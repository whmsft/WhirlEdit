import re

from pygments.lexer import RegexLexer, include, bygroups, default, using, \
    this, words, combined
from pygments.token import Text, Comment, Operator, Keyword, Name, String, \
    Number, Punctuation, Other
from pygments.util import get_bool_opt
import pygments.unistring as uni

JS_IDENT_START = ('(?:[$_' + uni.combine('Lu', 'Ll', 'Lt', 'Lm', 'Lo', 'Nl') +
                  ']|\\\\u[a-fA-F0-9]{4})')
JS_IDENT_PART = ('(?:[$' + uni.combine('Lu', 'Ll', 'Lt', 'Lm', 'Lo', 'Nl',
                                       'Mn', 'Mc', 'Nd', 'Pc') +
                 '\u200c\u200d]|\\\\u[a-fA-F0-9]{4})')
JS_IDENT = JS_IDENT_START + '(?:' + JS_IDENT_PART + ')*'


class Dart(RegexLexer):
    """
    For `Dart <http://dart.dev/>`_ source code.

    .. versionadded:: 1.5
    """

    name = 'Dart'
    aliases = ['dart']
    filenames = ['*.dart']
    mimetypes = ['text/x-dart']

    flags = re.MULTILINE | re.DOTALL

    tokens = {
        'root': [
            include('string_literal'),
            (r'#!(.*?)$', Comment.Preproc),
            (r'\b(import|export)\b', Keyword, 'import_decl'),
            (r'\b(library|source|part of|part)\b', Keyword),
            (r'[^\S\n]+', Text),
            (r'//.*?\n', Comment.Single),
            (r'/\*.*?\*/', Comment.Multiline),
            (r'\b(class|extension|mixin)\b(\s+)',
             bygroups(Keyword.Declaration, Text), 'class'),
            (r'\b(as|assert|break|case|catch|const|continue|default|do|else|finally|'
             r'for|if|in|is|new|rethrow|return|super|switch|this|throw|try|while)\b',
             Keyword),
            (r'\b(abstract|async|await|const|covariant|extends|external|factory|final|'
             r'get|implements|late|native|on|operator|required|set|static|sync|typedef|'
             r'var|with|yield)\b', Keyword.Declaration),
            (r'\b(bool|double|dynamic|int|num|Function|Never|Null|Object|String|void)\b',
             Keyword.Type),
            (r'\b(false|null|true)\b', Keyword.Constant),
            (r'[~!%^&*+=|?:<>/-]|as\b', Operator),
            (r'@[a-zA-Z_$]\w*', Name.Decorator),
            (r'[a-zA-Z_$]\w*:', Name.Label),
            (r'[a-zA-Z_$]\w*', Name),
            (r'[(){}\[\],.;]', Punctuation),
            (r'0[xX][0-9a-fA-F]+', Number.Hex),
            # DIGIT+ (‘.’ DIGIT*)? EXPONENT?
            (r'\d+(\.\d*)?([eE][+-]?\d+)?', Number),
            (r'\.\d+([eE][+-]?\d+)?', Number),  # ‘.’ DIGIT+ EXPONENT?
            (r'\n', Text)
            # pseudo-keyword negate intentionally left out
        ],
        'class': [
            (r'[a-zA-Z_$]\w*', Name.Class, '#pop')
        ],
        'import_decl': [
            include('string_literal'),
            (r'\s+', Text),
            (r'\b(as|deferred|show|hide)\b', Keyword),
            (r'[a-zA-Z_$]\w*', Name),
            (r'\,', Punctuation),
            (r'\;', Punctuation, '#pop')
        ],
        'string_literal': [
            # Raw strings.
            (r'r"""([\w\W]*?)"""', String.Double),
            (r"r'''([\w\W]*?)'''", String.Single),
            (r'r"(.*?)"', String.Double),
            (r"r'(.*?)'", String.Single),
            # Normal Strings.
            (r'"""', String.Double, 'string_double_multiline'),
            (r"'''", String.Single, 'string_single_multiline'),
            (r'"', String.Double, 'string_double'),
            (r"'", String.Single, 'string_single')
        ],
        'string_common': [
            (r"\\(x[0-9A-Fa-f]{2}|u[0-9A-Fa-f]{4}|u\{[0-9A-Fa-f]*\}|[a-z'\"$\\])",
             String.Escape),
            (r'(\$)([a-zA-Z_]\w*)', bygroups(String.Interpol, Name)),
            (r'(\$\{)(.*?)(\})',
             bygroups(String.Interpol, using(this), String.Interpol))
        ],
        'string_double': [
            (r'"', String.Double, '#pop'),
            (r'[^"$\\\n]+', String.Double),
            include('string_common'),
            (r'\$+', String.Double)
        ],
        'string_double_multiline': [
            (r'"""', String.Double, '#pop'),
            (r'[^"$\\]+', String.Double),
            include('string_common'),
            (r'(\$|\")+', String.Double)
        ],
        'string_single': [
            (r"'", String.Single, '#pop'),
            (r"[^'$\\\n]+", String.Single),
            include('string_common'),
            (r'\$+', String.Single)
        ],
        'string_single_multiline': [
            (r"'''", String.Single, '#pop'),
            (r'[^\'$\\]+', String.Single),
            include('string_common'),
            (r'(\$|\')+', String.Single)
        ]
    }

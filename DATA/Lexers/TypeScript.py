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


class TypeScript(RegexLexer):
    """
    For `TypeScript <http://typescriptlang.org/>`_ source code.

    .. versionadded:: 1.6
    """

    name = 'TypeScript'
    aliases = ['ts', 'typescript']
    filenames = ['*.ts', '*.tsx']
    mimetypes = ['text/x-typescript']

    flags = re.DOTALL | re.MULTILINE

    # Higher priority than the TypoScriptLexer, as TypeScript is far more
    # common these days
    priority = 0.5

    tokens = {
        'commentsandwhitespace': [
            (r'\s+', Text),
            (r'<!--', Comment),
            (r'//.*?\n', Comment.Single),
            (r'/\*.*?\*/', Comment.Multiline)
        ],
        'slashstartsregex': [
            include('commentsandwhitespace'),
            (r'/(\\.|[^[/\\\n]|\[(\\.|[^\]\\\n])*])+/'
             r'([gimuys]+\b|\B)', String.Regex, '#pop'),
            (r'(?=/)', Text, ('#pop', 'badregex')),
            default('#pop')
        ],
        'badregex': [
            (r'\n', Text, '#pop')
        ],
        'root': [
            (r'^(?=\s|/|<!--)', Text, 'slashstartsregex'),
            include('commentsandwhitespace'),
            (r'\+\+|--|~|&&|\?|:|\|\||\\(?=\n)|'
             r'(<<|>>>?|==?|!=?|[-<>+*%&|^/])=?', Operator, 'slashstartsregex'),
            (r'[{(\[;,]', Punctuation, 'slashstartsregex'),
            (r'[})\].]', Punctuation),
            (r'(for|in|while|do|break|return|continue|switch|case|default|if|else|'
             r'throw|try|catch|finally|new|delete|typeof|instanceof|void|of|'
             r'this|async|await|debugger|yield|abstract|static|import|export|'
             r'implements|super|extends|private|protected|public|readonly)\b',
                Keyword, 'slashstartsregex'),
            (r'(var|let|const|with|function|class|type|enum|interface)\b',
                Keyword.Declaration, 'slashstartsregex'),
            (r'(boolean|byte|char|double|final|float|goto|int|long|native|'
             r'package|short|synchronized|throws|transient|volatile)\b', Keyword.Reserved),
            (r'(true|false|null|NaN|Infinity|undefined)\b', Keyword.Constant),
            (r'(Array|Boolean|Date|Error|Function|Math|'
             r'Number|Object|RegExp|String|decodeURI|'
             r'decodeURIComponent|encodeURI|encodeURIComponent|'
             r'Error|eval|isFinite|isNaN|parseFloat|parseInt|document|this|'
             r'window|globalThis|Symbol|BigInt)\b', Name.Builtin),
            # Match stuff like: module name {...}
            (r'\b(module)(\s*)(\s*[\w?.$][\w?.$]*)(\s*)',
             bygroups(Keyword.Reserved, Text, Name.Other, Text), 'slashstartsregex'),
            # Match variable type keywords
            (r'\b(string|bool|number)\b', Keyword.Type),
            # Match stuff like: constructor
            (r'\b(constructor|declare|interface|as|AS)\b', Keyword.Reserved),
            # Match stuff like: super(argument, list)
            (r'(super)(\s*)(\([\w,?.$\s]+\s*\))',
             bygroups(Keyword.Reserved, Text), 'slashstartsregex'),
            # Match stuff like: function() {...}
            (r'([a-zA-Z_?.$][\w?.$]*)(?=\(\) \{)', Name.Other, 'slashstartsregex'),
            # Match stuff like: (function: return type)
            (r'([\w?.$][\w?.$]*)(\s*:\s*)([\w?.$][\w?.$]*)',
             bygroups(Name.Other, Text, Keyword.Type)),
            (r'[$a-zA-Z_]\w*', Name.Other),
            (r'0[bB][01]+n?', Number.Bin),
            (r'0[oO]?[0-7]+n?', Number.Oct),  # Browsers support "0o7" and "07" (< ES5) notations
            (r'0[xX][0-9a-fA-F]+n?', Number.Hex),
            (r'[0-9]+n', Number.Integer),
            (r'(\.[0-9]+|[0-9]+\.[0-9]*|[0-9]+)([eE][-+]?[0-9]+)?', Number.Float),
            (r'"(\\\\|\\[^\\]|[^"\\])*"', String.Double),
            (r"'(\\\\|\\[^\\]|[^'\\])*'", String.Single),
            (r'`', String.Backtick, 'interp'),
            # Match stuff like: Decorators
            (r'@\w+', Keyword.Declaration),
        ],

        # The 'interp*' rules match those in JavascriptLexer. Changes made
        # there should be reflected here as well.
        'interp': [
            (r'`', String.Backtick, '#pop'),
            (r'\\.', String.Backtick),
            (r'\$\{', String.Interpol, 'interp-inside'),
            (r'\$', String.Backtick),
            (r'[^`\\$]+', String.Backtick),
        ],
        'interp-inside': [
            # TODO: should this include single-line comments and allow nesting strings?
            (r'\}', String.Interpol, '#pop'),
            include('root'),
        ],
    }


import re
from pygments.lexer import RegexLexer,include,words
from pygments.token import *

__all__ = ['HalcmdLexer']

class HalcmdLexer(RegexLexer):
    """
    Lexer for the machinekit halcmd language

    """
    name = 'Halcmd'
    aliases = ['halcmd']
    filenames = ['*.hal']
    tokens = {
        'root': [
            (r'\n', Text),
            (r'\s+', Text),
            (r'[;#].*$', Comment.Single),
            include('keywords'),
            (r'(?s)"(\\\\|\\.|[^"\\])*"', String.Double),
            (r"(?s)'(\\\\|\\.|[^'\\])*'", String.Single),
            (r'(=>|<=|=)', Operator),
            (r'\[.*?\]\w+', Name.Namespace), # ini param substitution
            (r'[a-zA-Z][_\-\.a-zA-Z0-9]*', Name.Variable),  # HAL name
            include('numbers'),
        ],
        'keywords': [
            (words((
                "addf",
                "alias",
                "autoload",
                "delf",
                "delg",
                "delinst"
                "delm",
                "delring",
                "delsig",
                "delthread",
                "exit",
                "getp",
                "gets",
                "help",
                "linkpp",
                "linkps",
                "linksp",
                "list",
                "loadrt",
                "loadusr",
                "lock",
                "log",
                "net",
                "newcomp",
                "newg",
                "newinst",
                "newm",
                "newpin",
                "newring",
                "newsig",
                "newthread",
                "ping",
                "ptype",
                "quit",
                "ready",
                "ringdump",
                "ringread",
                "ringwrite",
                "save",
                "sete",
                "setp",
                "sets",
                "show",
                "shutdown",
                "sleep",
                "source",
                "start",
                "status",
                "stop",
                "stype",
                "unalias",
                "unlinkp",
                "unload",
                "unlock",
                "vtable",
                "waitbound",
                "waitexists",
                "waitunbound",
            ), prefix=r'\b', suffix=r'\s*\b'),
             Keyword),
        ],
        'numbers': [
            (r'(\d+\.\d*|\d*\.\d+)([eE][+-]?[0-9]+)?j?', Number.Float),
            (r'\d+[eE][+-]?[0-9]+j?', Number.Float),
            (r'0[0-7]+j?', Number.Oct),
            (r'0[bB][01]+', Number.Bin),
            (r'0[xX][a-fA-F0-9]+', Number.Hex),
            (r'\d+L', Number.Integer.Long),
            (r'\d+j?', Number.Integer)
        ],
    }



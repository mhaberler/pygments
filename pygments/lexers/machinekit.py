import re
from pygments.lexer import RegexLexer,include,words
from pygments.token import *

__all__ = ['HalcmdLexer', 'RS274Lexer']

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


class RS274Lexer(RegexLexer):
    """
    Lexer for RS274NGC G-Code

    """
    name = 'G-code'
    aliases = ['rs274']
    filenames = ['*.ngc']
    flags = re.IGNORECASE # | re.DOTALL
    tokens = {
        'root': [
            (r'\n', Text),
            (r'\s+', Text),
            (r';.*', Comment.Single),
            (r'%', Name.Attribute), # program begin/end

            (r'\([^\)]*\)', Comment.Single),
            (r'#([0-9]{4})', Name.Variable),    # predefined variable: eg #5420
            (r'#([0-9][0-9]?)', Name.Variable), # function parameter: #1..#30
            (r'#<([^\>]+)>', Name.Variable),    # named variable: #<foo>
            include('builtins'),
            include('owords'),
            include('flowcontrol'),
            (r'([n]([ |\t]*[0-9]){1,5})', Name.Attribute), # line numbers
            (r'(([-/|\=\+\*])|(\])|(\[))', Operator),
            (r'[fs]([\d])+(\.[\d]+)?', Keyword.Type),     # feeds and speeds
            (r'[gmth]([\d]){1,3}(\.\d)?', Keyword),  # G M T H codes
            (r'[xyzabcuvwijkpqrl]', Name.Function),  # Axes
            include('numbers'),
        ],
        'owords': [
            (r'o(([ \t]*[0-9])+|<([a-z_]([a-z0-9_])*>))', Name.Label),
        ],
        'flowcontrol' : [
            (words(('sub', 'endsub', 'while', 'endwhile',
                    'if', 'else', 'endif', 'do', 'call',
                    'break', 'continue', 'return',
                    'repeat', 'endrepeat','elseif'),
                    prefix=r'(?i)\b', suffix=r'\s*'),
                   Keyword.Reserved),
        ],
        'builtins': [
            (words(('cos', 'tan', 'asin', 'sin', 'acos', 'atan', 'exp', 'ln', 'sqrt',
                    'fup', 'fix', 'abs', 'or', 'xor', 'and', 'mod', 'gt', 'lt',
                    'ge', 'le', 'eq', 'ne', 'exists'),
                   prefix=r'(?i)\b', suffix=r'\s*\('), # case insensitive
             Name.Builtin, 'function'),
        ],
        'function': [
            (r'[^\)\(]+', Text),
            (r'\)', Keyword, '#pop'),
        ],
        'numbers': [
            (r'[+-]?([\d]+\.)[\d]*',Number.Float),
            (r'[+-]?([\d]*\.)[\d]+',Number.Float),
            (r'[+-]?[\d]+', Number.Integer),
        ],
    }

# # ngc.lang - RS274 G-Code formatting (EMC flavour)
# #
# #  Michael Haberler 3/2011
# #
# #  originally based on the Highlight-mode file for gedit,
# #  written by Jan Van Gilsen <janvangilsen(at)gmail(dot)com>
# #  Installation instructions can be found at:
# #  http://wiki.linuxcnc.org/cgi-bin/emcinfo.pl?Highlighting_In_Gedit
# #  Version		: 0.3
# #  Last Edit	: 10Th Nov 2007, by Jan Van Gilsen
# #  Comment 	: added probing and rigid tapping G-codes (new in 2.2)


# environment comment delim '\([dD][eE][bB][uU][gG],' ")" begin
# 	variable =  '#([0-9]{4})'
# 	variable =  '#[0-9][0-9]?'
# 	variable =  '#<([^\>]+)>'
# end
# comment delim "(" ")"
# comment start ";"


# # numbered parameters (#5xxx)
# variable =  '#([0-9]{4})'

# # function parameter -  #1 .. #30
# variable =  '#[0-9][0-9]?'

# # named parameters
# variable =  '#<([^\>]+)>'

# # math functions and boolean logic
# function = "cos|tan|asin|acos|atan|exp|ln|sqrt|fup|fix|abs|or",
# 	"xor|and|mod|gt|lt|ge|le|eq|ne|exists"
# 	nonsensitive

# # operators
# function = '(([-/|\=\+\*])|(\])|(\[))'

# # line numbers
# comment = '^[n|N]([ |\t]*[0-9]){1,5}'

# # O-word lines and their keywords
# preproc = '[ \t]*[o|O](([ \t]*[0-9])+|<([[:alpha:]]|_)([[:word:]]|\-)+>)[ \t]*',
# 	'(sub|endsub|while|endwhile|if|else|endif|do|call|break|continue|return|repeat|endrepeat|elseif)'

# # G codes
# vardef GCODE = '[g|G]([ \t]*[0])*[ \t]*'
# keyword = $GCODE + '1[ \t]*[07-9]'
# keyword = $GCODE + '2[ \t]*[018]'
# keyword = $GCODE + '3[ \t]*[03]'
# keyword = $GCODE + '3[ \t]*3[ \t]*.[ \t]*1'
# keyword = $GCODE + '3[ \t]*8[ \t]*.[ \t]*[2-5]'
# keyword = $GCODE + '4[ \t]*[1-3][ \t]*.[ \t]*1'
# keyword = $GCODE + '4[ \t]*[0-39]'
# keyword = $GCODE + '5[ \t]*[3-9]'
# keyword = $GCODE + '6[ \t]*[14]'
# keyword = $GCODE + '6[ \t]*.[ \t]*1'
# keyword = $GCODE + '7[ \t]*6'
# keyword = $GCODE + '8[ \t]*[0-9]'
# keyword = $GCODE + '9[ \t]*[0-489]'
# keyword = $GCODE + '9[ \t]*2[ \t]*.[ \t]*[1-3]'
# keyword = $GCODE + '[0-5]'


# # M-Codes
# vardef MCODE = '[m|M]([ \t]*[0])*[ \t]*'
# keyword = $MCODE + '5[ \t]*[0-3]'
# keyword = $MCODE + '3[ \t]*0'
# keyword = $MCODE + '6[ \t]*0'
# keyword = $MCODE + '6[ \t]*[0-9]'
# keyword = $MCODE + '7[ \t]*[0-3]'
# keyword = $MCODE + '1[ \t]*[0-9][ \t]*[1-9]'
# keyword = $MCODE + '1[ \t]*[1-9][ \t]*0'
# keyword = $MCODE + '[0-9]'

# # Feeds & speeds
# keyword = '[f|F|s|S]([ \t]*[0-9])*[ \t]*[.]?([ \t]*[0-9])*'

# # T, H
# keyword = '[t|T|h|H]([ \t]*[0-9])*'

# # Coordinates & arguments; trailing number/expression/params formatted separately
# atom = '[x|X|y|Y|z|Z|a|A|b|B|c|C|u|U|v|V|w|W|i|I|j|J|k|K|p|P|q|Q|r|R|l|L](\s*)?'


# #    * A number consists of (1) an optional plus or minus sign,
# #	followed by (2) zero to many digits, followed, possibly,
# #	by (3) one decimal point,
# #	followed by (4) zero to many digits - provided that there is at least one digit somewhere in the number.
# #
# #    * There are two kinds of numbers: integers and decimals. An integer does not have a decimal point in it; a decimal does.
# #    * Numbers may have any number of digits, subject to the limitation on line length. Only about seventeen significant figures will be retained, however (enough for all known applications).
# #    * A non-zero number with no sign as the first character is assumed to be positive.
# number = '[+-]?([[:digit:]]*\.)?[[:digit:]]+'

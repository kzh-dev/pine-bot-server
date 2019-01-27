# coding=utf-8
# see https://www.tradingview.com/wiki/Appendix_B._Pine_Script_v2_lexer_grammar

import ply.lex as lex
from ply.lex import TOKEN
from .base import PineError
 
# List of token names.   This is always required
tokens = (
    'COND', 'COND_ELSE',
    'OR', 'AND', 'NOT',
    'EQ', 'NEQ',
    'GT', 'GE', 'LT', 'LE',
    'PLUS', 'MINUS', 'MUL', 'DIV', 'MOD',
    'COMMA',
    'ARROW',
    'LPAR', 'RPAR',
    'LSQBR', 'RSQBR',
    'DEFINE',
    'IF_COND', 'IF_COND_ELSE',
    'ASSIGN',
    'FOR_STMT',
    'FOR_STMT_TO',
    'FOR_STMT_BY',
    'BREAK',
    'CONTINUE',

    'BEGIN', 'END', 'DELIM',

    'INT_LITERAL',
    'FLOAT_LITERAL',
    'BOOL_LITERAL',
    'STR_LITERAL',
    'COLOR_LITERAL',

    'ID', 
    #'ID_EX',
)

def _surround (r):
    return r'(?:' + r + r')'

def Lexer ():

    def r (t):
        t.lexer.last_token = t
        t.lexer.line_breakable = False
        return t
    def b (t):
        t.lexer.last_token = t
        t.lexer.line_breakable = True
        return t

    ### Grammer definitiion

    # Simple tokens
    def t_COND (t):
        r'\?'
        return b(t)
    def t_COND_ELSE (t):
        r':'
        return b(t)
    def t_EQ (t):
        r'=='
        return b(t)
    def t_NEQ (t):
        r'!='
        return b(t)
    def t_GT (t):
        r'>'
        return b(t)
    def t_GE (t):
        r'>='
        return b(t)
    def t_LT (t):
        r'<'
        return b(t)
    def t_LE (t):
        r'<='
        return b(t)
    def t_PLUS (t):
        r'\+'
        return b(t)
    def t_MINUS (t):
        r'-'
        return b(t)
    def t_MUL (t):
        r'\*'
        return b(t)
    def t_DIV (t):
        r'/'
        return b(t)
    def t_MOD (t):
        r'%'
        return b(t)
    def t_COMMA (t):
        r','
        return b(t)
    def t_ARROW (t):
        r'=>'
        return r(t)
    def t_LSQBR (t):
        r'\['
        t.lexer.in_braket += 1
        return r(t)
    def t_RSQBR (t):
        r'\]'
        t.lexer.in_braket -= 1
        return r(t)
    def t_DEFINE (t):
        r'='
        return b(t)
    def t_ASSIGN (t):
        r':='
        return b(t)

    # reserved keywords (Needs to define as a method before hand ID to prevent from being swallowed.
    def t_IF_COND (t):
        r'\bif\b'
        return r(t)
    def t_IF_COND_ELSE (t):
        r'\belse\b'
        return r(t)
    def t_OR (t):
        r'\bor\b'
        return b(t)
    def t_AND (t):
        r'\band\b'
        return b(t)
    def t_NOT (t):
        r'\bnot\b'
        return r(t)
    def t_FOR_STMT (t):
        r'\bfor\b'
        return r(t)
    def t_FOR_STMT_TO (t):
        r'\bto\b'
        return r(t)
    def t_FOR_STMT_BY (t):
        r'\bby\b'
        return r(t)
    def t_BREAK (t):
        r'\bbreak\b'
        return r(t)
    def t_CONTINUE (t):
        r'\bcontinue\b'
        return r(t)

    # Parenthsis
    def t_LPAR (t):
        r'\('
        t.lexer.in_paren += 1
        return r(t)
    def t_RPAR (t):
        r'\)'
        t.lexer.in_paren -= 1
        return r(t)

    # Pseudo tokens
    def t_BEGIN (t):
        r'\|BGN\|'
        if not t.lexer.in_paren and not t.lexer.in_braket and not t.lexer.line_breakable:
            return r(t)
        else:
            t.lexer.dummy_indent += 1
    def t_END (t):
        r'\|END\|'
        if not t.lexer.in_paren and not t.lexer.in_braket:
            if not t.lexer.dummy_indent:
                return r(t)
            t.lexer.dummy_indent -= 1
    def t_DELIM (t):
        r'\|DLM\|'
        if not t.lexer.in_paren and not t.lexer.in_braket and not t.lexer.line_breakable:
            return r(t)

    ## Literals

    # fragment DIGIT : ( '0' .. '9' ) ;
    # fragment DIGITS : ( '0' .. '9' )+ ;
    # fragment HEX_DIGIT : ( '0' .. '9' | 'a' .. 'f' | 'A' .. 'F' ) ;
    # fragment EXP : ( 'e' | 'E' ) ( '+' | '-' )? DIGITS ;
    digit = _surround(r'\d')
    digits = _surround(r'\d+')
    hex_digit = _surround(r'[\dA-Fa-f]')
    exp = _surround(r'[eE][-+]?' + digits)

    # FLOAT_LITERAL : ( '.' DIGITS ( EXP )? | DIGITS ( '.' ( DIGITS ( EXP )? )? | EXP ) );
    float1 = _surround(r'\.' + digits + exp + r'?')
    float2 = _surround(digits + r'\.' + _surround(digits + _surround(exp + r'?')) + r'?')
    float3 = exp
    float_ = _surround(float1 + '|' + float2 + '|' + float3)
    @TOKEN(float_)
    def t_FLOAT_LITERAL (t):
        t.value = float(t.value)
        return r(t)

    @TOKEN(digits)
    def t_INT_LITERAL (t):
        t.value = int(t.value, 10)
        return r(t)

    # BOOL_LITERAL : ( 'true' | 'false' );
    def t_BOOL_LITERAL (t):
        r'true|false'
        t.value = (t.value == 'true')
        return r(t)

    # fragment ESC : '\\' . ;
    # STR_LITERAL : ( '"' ( ESC | ~ ( '\\' | '\n' | '"' ) )* '"' | '\'' ( ESC | ~ ( '\\' | '\n' | '\'' ) )* '\'' );
    esc = r'\\'
    dqbody = _surround(esc + '|' + r'[^\\\n"]') + '*'
    dqstr = r'"' + dqbody + r'"'
    sqbody = _surround(esc + '|' + r"[^\\\n']") + '*'
    sqstr = r"'" + sqbody + r"'"
    str_ = dqstr + '|' + sqstr
    @TOKEN(str_)
    def t_STR_LITERAL (t):
        t.value = t.value[1:-1] 
        return r(t)

    # COLOR_LITERAL : ( '#' HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT | '#' HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT );
    t_COLOR_LITERAL = '\#' + hex_digit + '{6}' + _surround(hex_digit + '{2}') + '?'

    # fragment ID_BODY : ( ID_LETTER | DIGIT )+ ;
    # fragment ID_BODY_EX : ( ID_LETTER_EX | DIGIT )+ ;
    # fragment ID_LETTER : ( 'a' .. 'z' | 'A' .. 'Z' | '_' ) ;
    # fragment ID_LETTER_EX : ( 'a' .. 'z' | 'A' .. 'Z' | '_' | '#' ) ;
    # ID : ( ID_LETTER ) ( ( '\.' )? ( ID_BODY '\.' )* ID_BODY )? ;
    # ID_EX : ( ID_LETTER_EX ) ( ( '\.' )? ( ID_BODY_EX '\.' )* ID_BODY_EX )? ;
    id_letter = r'[A-Za-z_]'
    id_letter_ex = r'[A-Za-z_#]'
    id_body = r'\w+'
    id_body_ex = r'[\w#]+'
    id_ = id_letter + _surround(_surround(r'\.?' + id_body + r'\.') + '*' + id_body) + '?'
    #id_ex_ = id_letter_ex + _surround(_surround(r'\.?' + id_body_ex + r'\.') + '*' + id_body_ex) + '?'
    @TOKEN(id_)
    def t_ID (t):
        return r(t)
    #@TOKEN(id_ex_)
    #def t_ID_EX (t):
    #    return r(t)

    ### Utilities
    t_ignore = ' \t'
    def t_newline(t):
        r'\n+'
        t.lexer.lineno += len(t.value)
    def t_error (t):
        raise PineError("invalid character: {}".format(t.value[0]))
        #t.lexer.skip(1)

    ### Make lexer
    lexer = lex.lex()
    lexer.in_paren = 0
    lexer.in_braket = 0
    lexer.dummy_indent = 0
    lexer.last_token = None
    lexer.line_breakable = False
    return lexer


if __name__ == '__main__':
    import sys
    from .preprocess import preprocess
    with open(sys.argv[1]) as f:
        data = preprocess(f.read())
        lexer = Lexer()
        lexer.input(data)

        # Tokenize
        while True:
            tok = lexer.token()
            if not tok: 
                break      # No more input
            print(tok)

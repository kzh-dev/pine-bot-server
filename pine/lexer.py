# coding=utf-8
# see https://www.tradingview.com/wiki/Appendix_B._Pine_Script_v2_lexer_grammar

import ply.lex as lex
from ply.lex import TOKEN
 
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
    ### Grammer definitiion

    # Simple tokens
    t_COND = r'\?'
    t_COND_ELSE = r':'
    t_EQ = r'=='
    t_NEQ = r'!='
    t_GT = r'>'
    t_GE = r'>='
    t_LT = r'<'
    t_LE = r'<='
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_MUL = r'\*'
    t_DIV = r'/'
    t_MOD = r'%'
    t_COMMA = r','
    t_ARROW = r'=>'
    t_LSQBR = r'\['
    t_RSQBR = r'\]'
    t_DEFINE = r'='
    t_ASSIGN = r':='

    # reserved keywords (Needs to define as a method before hand ID to prevent from being swallowed.
    def t_IF_COND (t):
        r'if'
        return t
    def t_IF_COND_ELSE (t):
        r'else'
        return t
    def t_OR (t):
        r'or'
        return t
    def t_AND (t):
        r'and'
        return t
    def t_NOT (t):
        r'not'
        return t
    def t_FOR_STMT (t):
        r'for'
        return t
    def t_FOR_STMT_TO (t):
        r'to'
        return t
    def t_FOR_STMT_BY (t):
        r'by'
        return t
    def t_BREAK (t):
        r'break'
        return t
    def t_CONTINUE (t):
        r'continue'
        return t

    # Parenthsis
    def t_LPAR (t):
        r'\('
        t.lexer.in_paren += 1
        return t
    def t_RPAR (t):
        r'\)'
        t.lexer.in_paren -= 1
        return t

    # Pseudo tokens
    def t_BEGIN (t):
        r'\|BGN\|'
        if not t.lexer.in_paren:
            return t
        else:
            t.lexer.dummy_indent += 1
    def t_END (t):
        r'\|END\|'
        if not t.lexer.in_paren:
            if not t.lexer.dummy_indent:
                return t
            t.lexer.dummy_indent -= 1
    def t_DELIM (t):
        r'\|DLM\|'
        if not t.lexer.in_paren:
            return t

    ## Literals

    # fragment DIGIT : ( '0' .. '9' ) ;
    # fragment DIGITS : ( '0' .. '9' )+ ;
    # fragment HEX_DIGIT : ( '0' .. '9' | 'a' .. 'f' | 'A' .. 'F' ) ;
    # fragment EXP : ( 'e' | 'E' ) ( '+' | '-' )? DIGITS ;
    digit = _surround(r'\d')
    digits = _surround(r'\d+')
    hex_digit = _surround(r'[\dA-Fa-f]')
    exp = _surround(r'[eE][-+]?' + digits)

    @TOKEN(digits)
    def t_INT_LITERAL (t):
        t.value = int(t.value, 10)
        return t

    # FLOAT_LITERAL : ( '.' DIGITS ( EXP )? | DIGITS ( '.' ( DIGITS ( EXP )? )? | EXP ) );
    float1 = _surround(r'\.' + digits + exp + r'?')
    float2 = _surround(digits + _surround(digits + _surround(exp + r'?')) + r'?')
    float3 = exp
    float_ = _surround(float1 + '|' + float2 + '|' + float3)
    @TOKEN(float_)
    def t_FLOAT_LITERAL (t):
        t.value = float(t.value)
        return t

    # BOOL_LITERAL : ( 'true' | 'false' );
    def t_BOOL_LITERAL (t):
        r'true|false'
        t.value = (t.value == 'true')
        return t

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
        return t

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
        return t
    #@TOKEN(id_ex_)
    #def t_ID_EX (t):
    #    return t

    ### Utilities
    t_ignore = ' \t'
    def t_newline(t):
        r'\n+'
        t.lexer.lineno += len(t.value)
    def t_error (t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    ### Make lexer
    lexer = lex.lex()
    lexer.in_paren = 0
    lexer.dummy_indent = 0
    return lexer


if __name__ == '__main__':
    import sys
    from preprocess import preprocess
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

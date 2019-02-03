# coding=utf-8
# see https://www.tradingview.com/wiki/Appendix_A._Pine_Script_v2_preprocessor

import re

COMMENT_RE = re.compile(r'//.*$', re.MULTILINE)
def remove_comment (string):
    return COMMENT_RE.sub('', string)

INDENT_RE = re.compile(r'[ \t]+')
def complement_block_tokens (string):
    lines = []
    prev = 0
    last = 0
    for line in string.splitlines():
        line = line.rstrip()

        if line:
            mo = INDENT_RE.match(line)
            if mo:
                ws = mo.group().replace("\t", '    ')   # TAB = WS x 4?
                indent = int((len(ws) + 3 ) / 4)
            else:
                indent = 0

            if prev < indent:
                lines[last][1] = '|BGN|' * (indent - prev)
            elif prev > indent:
                lines[last][1] += '|END|' * (prev - indent)

            prev = indent
            delim = '|DLM|'
            last = len(lines)
        else:
            delim = ''

        lines.append([line, delim])

    if prev != 0:
        lines[-1][1] += '|END|' * prev

    return "\n".join([l + d for l,d in lines])

def preprocess (string):
    # 1. remove comment FIXME
    string = remove_comment(string)

    # 2. insert block delimiter tokens
    string = complement_block_tokens(string)
    return string


if __name__ == '__main__':
    import sys
    with open(sys.argv[1]) as f:
        print(preprocess(f.read()))

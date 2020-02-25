def match(tokens, expected):
    if tokens[0] != expected:
        print('Parse error in match. Got {0}, expected {1}'.format(tokens[0], expected))
        return 1, tokens[1:]
    print('Matched {0} with {1}'.format(tokens[0], expected))
    return 0,tokens[1:]

def parseProgram(tokens):
    cumError = 0
    token = tokens[0]
    if token in ['id', 'read','write','$$']:
        error, tokens = parseStmtList(tokens)
        cumError += error 
        error, tokens = match(tokens, '$$')
        cumError += error
    else:
        cumError = 1
        print('Parse error from parseProgram')
    return cumError, tokens

def parseStmtList(tokens):
    token = tokens[0]
    cumError = 0
    if token in ['id', 'read','write']:
        error, tokens = parseStmt(tokens)
        cumError += error
        error, tokens = parseStmtList(tokens)
        cumError += error
    elif token == '$$':
        pass
    else:
        cumError = 1
        print('Parse error from parseStmtList on {0}'.format(token))
    return cumError, tokens

def parseStmt(tokens):
    token = tokens[0]
    cumError = 0
    if token == 'id':
        error, tokens = match(tokens, 'id')
        cumError += error
        error, tokens = match(tokens, 'assign')
        cumError += error
        error, tokens = parseExpr(tokens)
        cumError += error
        return cumError, tokens
    elif token == 'read':
        error, tokens = match(tokens,'read')
        cumError += error
        error, tokens = match(tokens, 'id')
    elif token == 'write':
        error, tokens = match(tokens, 'write')
        cumError += error
        error, tokens = match(tokens, 'id')
    else: 
        cumError = 1
        print('Parse error in parseStmt on {0} in {1}'.format(token, tokens))
    return cumError, tokens

def parseExpr(tokens):
    token = tokens[0]
    cumError = 0
    if token in ['id','num', '(']:
        error, tokens = parseTerm(tokens)
        cumError += error
        error, tokens = parseTermTail(tokens)
        cumError += error
    else:
        cumError = 1
        print('Parse error in parseExpr on {0}'.format(token))
    return cumError, tokens

def parseTermTail(tokens):
    token = tokens[0]
    cumError = 0
    if token in ['+','-']:
        error, tokens = parseAddOp(tokens)
        cumError += error
        error, tokens = parseTerm(tokens)
        cumError += error
        error, tokens = parseTermTail(tokens)
        cumError += error
    elif token in [')','id','read', 'write', '$$']:
        pass
    else:
        cumError = 1
        print('Parse error in parseTermTail on {0}'.format(token))
    return cumError, tokens


def parseTerm(tokens):
    token = tokens[0]
    cumError = 0
    if token in ['id','num', '(']:
        error, tokens = parseFactor(tokens)
        cumError += error
        error, tokens = parseFactorTail(tokens)
        cumError += error
    else:
        cumError = 1
        print('Parse error in parseTerm on {0}'.format(token))
    return cumError, tokens

def parseFactorTail(tokens):
    token = tokens[0]
    cumError = 0
    if token in ['*','div']:
        error, tokens = parseMultOp(tokens)
        cumError += error
        error, tokens = parseFactor(tokens)
        cumError += error
        error, tokens = parseFactorTail(tokens)
        cumError += error
    elif token in ['+','-',')','id', 'read','write', '$$']:
        pass
    else:
        cumError = 1
        print('Parse error in parseFactorTail on {0}'.format(token))
    return cumError, tokens

def parseFactor(tokens):
    token = tokens[0]
    cumError = 0
    if token == 'id':
        error, tokens = match(tokens, token)
        cumError += error
    elif token == 'num':
        error, tokens = match(tokens, token)
        cumError += error
    elif token == '(':
        error, tokens = match(tokens, token)
        cumError += error
        error, tokens = parseExpr(tokens)
        cumError += error
        error, tokens = match(tokens, ')')
        cumError += error
    else:
        cumError = 1
        print('Parse error in parseFactor on {0}'.format(token))
    return cumError, tokens

def parseAddOp(tokens):
    token = tokens[0]
    cumError = 0
    if token == '+':
        error, tokens = match(tokens, token)
        cumError += error
    elif token == '-':
        error, tokens = match(tokens, token)
        cumError += error
    else:
        cumError = 1
        print('Parse error in parseAddOp on {0}'.format(token))
    return cumError, tokens

def parseMultOp(tokens):
    token = tokens[0]
    cumError = 0
    if token == '*':
        error, tokens = match(tokens, token)
        cumError += error
    elif token == 'div':
        error, tokens = match(tokens, token)
        cumError += error
    else:
        cumError = 1
        print('Parse error in parseMultOp on {0}'.format(token))
    return cumError, tokens

def run(tokens):
    errors, tokens = parseProgram(tokens)
    if errors > 0:
        print('Tokens failed to parse. Found {0} errors'.format(errors))
    else:
        print('Tokens successfully parsed')

tokens = []
filename = 'calcTokens'
with open(filename, 'r') as infile:
    for line in infile:
        tokenSet = line.strip().split()
        tokens.extend(tokenSet)

run(tokens)


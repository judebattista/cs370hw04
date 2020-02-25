# Treating := as a single op may cause trouble
operators = ['(',')', '+', '-', '*']
keywords = ['read','write']
whitespace = [' ', '\t', '\n', '\r']
eof = '$$'

def isWhiteSpace(inputStr):
    return inputStr in whitespace

def eatWhiteSpace(inputStr):
    ndx = 0
    while inputStr[ndx] in whitespace and ndx < len(inputStr):
        ndx += 1
    #print(inputStr)
    return inputStr[ndx:]

def eatUntil(inputStr, term):
    ndx = 0
    while inputStr[ndx] != term and ndx < len(inputStr):
        ndx += 1
    print('Ate until: {0}'.format(inputStr))
    return inputStr[ndx+1:]

# scan expects lines to be a list of strings
def scan(lines):
    curChar = ''
    nextChar = ''
    # Get rid of whitespace
    lines = eatWhiteSpace(lines)
    #print(lines)
    curChar = lines[0]
    if len(lines) > 1:
        nextChar = lines[1]
    if curChar == '$':
        if nextChar == '$':
            return '$$', []
        else:
            print('Scanner error on termination symbol: {0}{1}'.format(curChar, nextChar))
    
    if curChar in operators:
        print('Token: {0}'.format(curChar))
        return curChar, lines[1:]
    if curChar == ':':
        if nextChar == '=':
            print('assign')
            return 'assign', lines[2:]
        else:
            print('Scanner error on ":" {0}{1}'.format(curChar, nextChar))
    if curChar == '/':
        # print('Found a slash: {0}{1}'.format(curChar, nextChar))
        # If it is the first character of a /**/ comment
        # read to the end of the comment
        if nextChar == '*':
            print('Found /*')
            while nextChar != '/' and lines:  # potential bound error
                # Ordering is weird to prevent errors in the event eatUntil returns []
                nextChar = lines[0]
                lines = eatUntil(lines[2:], '*')
            return [], lines[2:] 
        # If we have a single line comment
        elif nextChar == '/':
            lines = eatUntil(lines, '\n')
            return [], lines[0:]
        else:
            print('div')
            return 'div', lines[1:]
    # Number with a leading decimal point
    if curChar == '.':
        ndx = 2
        num = curChar
        while nextChar.isdigit() and ndx < len(lines):
            num += nextChar
            nextChar = lines[ndx]
            ndx += 1
        if len(num) > 1:
            print('Numeric value: {0}'.format(num))
            return 'num', lines[ndx-1:]
        else:
            print('Scanner error: malformed numeric value {0}'.format(num))
            return []
    # If we have a number
    if curChar.isdigit():
        ndx = 2
        num = curChar
        while nextChar.isdigit() and ndx < len(lines):
            num += nextChar
            nextChar = lines[ndx]
            ndx += 1
        if ndx < len(lines) and nextChar == '.':
            num += nextChar
            nextChar = lines[ndx]
            ndx += 1
        while nextChar.isdigit() and ndx < len(lines):
            num += nextChar
            nextChar = lines[ndx]
            ndx += 1
        print('Numeric value: {0}'.format(num))
        return 'num', lines[ndx-1:]
    # If we have an alphabetic char
    if str(curChar).isalpha():
        ndx = 2
        string = curChar
        while str(nextChar).isalnum() and ndx < len(lines):
            string += nextChar
            nextChar = lines[ndx]
            ndx += 1
        if string in keywords:
            print(string)
            return string, lines[ndx:]
        else:
            print('id={0}'.format(string))
            return 'id', lines[ndx-1:]
    print('Scanner error on {0}{1}'.format(curChar, nextChar))
    return [],[]
         

def run(lines):
    tokens = []
    #print lines
    while lines:
        token, lines = scan(lines)
        if len(token) > 0:
            tokens.append(token)
    return tokens

# Open the code file
# filename = input('Please enter the filename to scan')
filename = "calcCode"
lines = ""
# Read the lines from the code file into our object
with open(filename, 'r') as infile:
    for line in infile:
        lines += line

lines = eatWhiteSpace(lines)
tokens = run(lines)
print(tokens)

outfilename = 'calcTokens'
with open(outfilename, 'w') as outfile:
    for token in tokens:
        outfile.write(token + ' ')

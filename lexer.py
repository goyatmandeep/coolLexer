import ply.lex as lex

tokens = [                                      #list of all valid tokens, RE defined later.
    'TYPE', 'ID', 'INTEGER', 'STRING', 'BOOL','ACTION',"LPAREN", "RPAREN", "LBRACE", "RBRACE", "COLON", "COMMA", "DOT", "SEMICOLON", "AT",
     "PLUS", "MINUS", "MULTIPLY", "DIVIDE", "EQ", "LT", "LTEQ", "ASSIGN", "INT_COMP", "NOT",] 

keywords = {                                  #keywords defined in this manner to avoid conflicts with the identifier names.
    'class': 'CLASS', 
    'inherits': 'INHERITS',
    'in': 'IN',
    'case': 'CASE',
    'of': 'OF',
    'esac': 'ESAC',
    'new': 'NEW',
    'self': 'SELF',
    'isvoid': 'ISVOID',
    'if': 'IF',
    'in': 'IN',
    'then': 'THEN',
    'else': 'ELSE',
    'fi': 'FI',
    'while': 'WHILE',
    'loop': 'LOOP',
    'pool': 'POOL',
    'let': 'LET', 
}

tokens = tokens + list(keywords.values())

def t_INTEGER(t):                                   #Regular expression with some action code.
    r'[0-9]+'                                       #Function documentation string. Matched according to function definition.
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]
    return t

def t_BOOL(t):
    r'true|false'
    t.value = True if t.value == 'true' else False
    return t

states = (("COMMENT", 'exclusive'),)

def t_start_comment(t):
    r"\(\*"
    t.lexer.push_state("COMMENT")
    t.lexer.comment_count = 0

def t_COMMENT_another(t):
    r"\(\*"
    t.lexer.comment_count += 1

def t_COMMENT_end(t):
    r"\*\)"
    if t.lexer.comment_count == 0:
        t.lexer.pop_state()
    else:
        t.lexer.comment_count -= 1

def t_COMMENT_newline(t):
    r'\n+'
    t.lexer.lineno +=len(t.value)

def t_COMMENT(t):
    r'\-\-[^\n]*'
    pass

def t_COMMENT_error(t):
    t.lexer.skip(1)

def t_NOT(t):
    r'[nN][oO][tT]'
    return t

# Identifiers

def t_TYPE(t):                                                   #Class name starts with capital letter.
    r'[A-Z][A-Za-z0-9_]*'
    return t

def t_ID(t):                                                    #If token does not match with keyword then it is an identifier.
    r'[a-z][A-Za-z0-9_]*'
    t.type = keywords.get(t.value.lower(), 'ID')
    if t.type == 'ID':
        lexer.num_count += 1
    return t


def t_newline(t):                                               #To increase the Line Count
    r'\n+'
    t.lexer.lineno += len(t.value)

                                                               # Must start with t_ to be identified as token.    
t_LPAREN = r'\('                                               #Matched according to the length of the RE string.                               
t_RPAREN = r'\)'        
t_LBRACE = r'\{'        
t_RBRACE = r'\}'        
t_COLON = r'\:'         
t_COMMA = r'\,'         
t_DOT = r'\.'           
t_SEMICOLON = r'\;'     
t_AT = r'\@'            
t_MULTIPLY = r'\*'      
t_DIVIDE = r'\/'        
t_PLUS = r'\+'          
t_MINUS = r'\-'          
t_INT_COMP = r'~'       
t_LT = r'\<'            
t_EQ = r'\='            
t_LTEQ = r'\<\='        
t_ASSIGN = r'\<\-'      
t_ACTION = r'\=\>'       

def t_error(t):                                                     #to skip the illegal character
    print("Illegal character encountered '{}'".format(t.value[0]))
    t.lexer.skip(1)

t_ignore = ' '

if 1:   
    import sys
    if len(sys.argv) != 2:
        print('You need to specify a cool source file to read from.')
        sys.exit(1)
    

    sourcefile = sys.argv[1]

    lexer = lex.lex()                                               #Lexer build.
    lexer.num_count = 0

    try:
        with open(sourcefile, 'r') as source:
            lexer.input(source.read())
    except:
        print("File not found.")
        exit(1)
    
    # Read tokens
    for token in lexer:
        if token is not None:
            print("Token " + "("+str(token.value) + " "+ str(token.type)+")")
    print("Number of identifiers encountered", lexer.num_count)

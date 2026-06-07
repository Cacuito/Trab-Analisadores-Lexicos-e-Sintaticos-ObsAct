import ply.lex as lex

tokens = [
    'NUM',
    'BOOL',
    'MSG',
    'NAMEDEVICE',
    'OBSERVATION',
    'OPLOGIC',
    'AND',
    'PONTO',
    'VIRGULA',
    'ABRE_CHAVE',
    'FECHA_CHAVE',
    'ABRE_PARENTESE',
    'FECHA_PARENTESE',
    'IGUAL'
]

reserved = {
    'dispositivo': 'DISPOSITIVO_KW',
    'set': 'SET',
    'se': 'SE',
    'entao': 'ENTAO',
    'senao': 'SENAO',
    'ligar': 'LIGAR',
    'desligar': 'DESLIGAR',
    'verificar': 'VERIFICAR',
    'enviar alerta': 'ENVIAR_ALERTA',
    'para todos:': 'PARA_TODOS',
}

tokens += list(reserved.values())

t_AND = r'&&'
t_PONTO = r'\.'
t_VIRGULA = r','
t_ABRE_CHAVE = r'\{'
t_FECHA_CHAVE = r'\}'
t_ABRE_PARENTESE = r'\('
t_FECHA_PARENTESE = r'\)'
t_IGUAL = r'='

# Operadores lógicos
def t_OPLOGIC(t):
    r'==|!=|<=|>=|<|>'
    return t

# Booleanos (True/False)
def t_BOOL(t):
    r'True|False|TRUE|FALSE'
    t.value = t.value.upper() == 'TRUE'
    return t

# Mensagens entre aspas, limitadas a 100 caracteres
def t_MSG(t):
    r'"[^"\n]{0,100}"'
    t.value = t.value[1:-1]  # Remove as aspas
    return t

# Números inteiros e não negativos
def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Identificadores complexos
def t_IDENTIFIES(t):
    r'enviar\salerta|para\stodos:|dispositivo:|=[=]?|!=|[a-zA-Z][a-zA-Z0-9]*'

    if t.value in reserved:
        t.type = reserved[t.value]
    elif t.value.isalpha():
        t.type = 'NAMEDEVICE'
    else:
        t.type = 'OBSERVATION'
    return t

# Ignorar espaços em branco
t_ignore = ' \t'

# Controlar quebra de linhas para apontar erros com precisão
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Tratamento de erros léxicos
def t_error(t):
    print(f"Erro Léxico: Caractere inválido '{t.value[0]}' na linha {t.lineno}")
    t.lexer.skip(1)

# Inicializa o lexer
lexer = lex.lex()
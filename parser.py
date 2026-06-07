# parser.py
import ply.yacc as yacc
from lexer import tokens

# Regra Inicial: O programa é composto por dispositivos e comandos
def p_program(p):
    'program : devices cmds'
    p[0] = p[1] + "\n" + p[2]

# Lista de dispositivos (recursiva)
def p_devices_multiple(p):
    'devices : device devices'
    p[0] = p[1] + "\n" + p[2]

def p_devices_single(p):
    'devices : device'
    p[0] = p[1]

# Regra auxiliar para aceitar tanto NAMEDEVICE quanto OBSERVATION como identificadores textuais
def p_id_any(p):
    '''id_any : NAMEDEVICE
              | OBSERVATION'''
    p[0] = p[1]

# Declaração de um dispositivo simples: dispositivo: {namedevice}
def p_device_simple(p):
    'device : DISPOSITIVO_KW ABRE_CHAVE NAMEDEVICE FECHA_CHAVE'
    dispositivo = p[3]
    p[0] = f"if '{dispositivo}' not in globals(): {dispositivo} = {{'status': 0, 'observation': 0}}"

# Declaração de um dispositivo com sensor: dispositivo: {namedevice, observation}
def p_device_complete(p):
    'device : DISPOSITIVO_KW ABRE_CHAVE NAMEDEVICE VIRGULA id_any FECHA_CHAVE'
    dispositivo = p[3]
    sensor = p[5]
    p[0] = f"{sensor} = 0\nif '{dispositivo}' not in globals(): {dispositivo} = {{'status': 0, 'observation': '{sensor}'}}"

# Lista de comandos finalizados por ponto (recursiva)
def p_cmds_multiple(p):
    'cmds : cmd PONTO cmds'
    p[0] = p[1] + "\n" + p[3]

def p_cmds_single(p):
    'cmds : cmd PONTO'
    p[0] = p[1]

# Um comando genérico
def p_cmd(p):
    '''cmd : attrib
           | obsact
           | act'''
    p[0] = p[1]

# Atribuição de variável/sensor simples: set temperatura = 40
def p_attrib_var(p):
    'attrib : SET id_any IGUAL var'
    p[0] = f"{p[2]} = {p[4]}"

# Atribuição vinda do retorno de uma função: set estado = verificar(ventilador)
def p_attrib_execute(p):
    'attrib : SET id_any IGUAL actexecute'
    p[0] = f"{p[2]} = {p[4]}"

# Valores aceitos em variáveis e comparações
def p_var(p):
    '''var : NUM
           | BOOL
           | NAMEDEVICE
           | OBSERVATION'''
    p[0] = str(p[1])

# Condicional Simples: se OBS entao CMDS
def p_obsact_simple(p):
    'obsact : SE obs ENTAO cmds'
    comandos_indentados = "\n".join(["    " + linha for linha in p[4].split("\n")])
    p[0] = f"if {p[2]}:\n{comandos_indentados}"

# Condicional Completa: se OBS entao CMDS senao CMDS
def p_obsact_complete(p):
    'obsact : SE obs ENTAO cmds SENAO cmds'
    comandos_if = "\n".join(["    " + linha for linha in p[4].split("\n")])
    comandos_else = "\n".join(["    " + linha for linha in p[6].split("\n")])
    p[0] = f"if {p[2]}:\n{comandos_if}\nelse:\n{comandos_else}"

# Expressão lógica simples: temperatura > 30
def p_obs_simple(p):
    'obs : id_any OPLOGIC var'
    p[0] = f"{p[1]} {p[2]} {p[3]}"

# Expressão lógica composta: movimento == True && umidade < 40
def p_obs_compound(p):
    'obs : id_any OPLOGIC var AND obs'
    p[0] = f"{p[1]} {p[2]} {p[3]} and {p[5]}"

# Ações físicas em dispositivos (ligar/desligar) ou envio de alertas
def p_act(p):
    '''act : ACTION NAMEDEVICE
           | actalert'''
    if len(p) == 3:
        p[0] = f"{p[1]}('{p[2]}')"
    else:
        p[0] = p[1]

# Comando de checagem/função: verificar(ventilador)
def p_actexecute(p):
    'actexecute : VERIFICAR ABRE_PARENTESE NAMEDEVICE FECHA_PARENTESE'
    p[0] = f"verificar('{p[3]}')"

# Terminais de ação pura
def p_action(p):
    '''ACTION : LIGAR
              | DESLIGAR'''
    p[0] = p[1]

# --- REGRAS DE ALERTA E BROADCAST ---

# Alerta simples para um dispositivo: enviar alerta ("msg") namedevice
def p_actalert_simple(p):
    'actalert : ENVIAR_ALERTA ABRE_PARENTESE MSG FECHA_PARENTESE NAMEDEVICE'
    p[0] = f"alerta_simples('{p[5]}', '{p[3]}')"

# Alerta com concatenação de variável: enviar alerta ("msg", temperatura) namedevice
def p_actalert_var(p):
    'actalert : ENVIAR_ALERTA ABRE_PARENTESE MSG VIRGULA id_any FECHA_PARENTESE NAMEDEVICE'
    p[0] = f"alerta_com_var('{p[7]}', '{p[3]}', {p[5]})"

# 1. Broadcast Simples
def p_actalert_broadcast_simple(p):
    'actalert : ENVIAR_ALERTA ABRE_PARENTESE MSG FECHA_PARENTESE PARA_TODOS devicelist'
    p[0] = f"for dev in {p[6]}: alerta_simples(dev, '{p[3]}')"

# 2. Broadcast com Variável
def p_actalert_broadcast_var(p):
    'actalert : ENVIAR_ALERTA ABRE_PARENTESE MSG VIRGULA id_any FECHA_PARENTESE PARA_TODOS devicelist'
    # p[5] é a variável (ex: temperatura) e p[8] é a devicelist
    p[0] = f"for dev in {p[8]}: alerta_com_var(dev, '{p[3]}', {p[5]})"

# Lista de dispositivos para o Broadcast (recursiva)
def p_devicelist_multiple(p):
    'devicelist : NAMEDEVICE VIRGULA devicelist'
    p[0] = [p[1]] + p[3]

def p_devicelist_single(p):
    'devicelist : NAMEDEVICE'
    p[0] = [p[1]]

# Tratamento de erros sintáticos
def p_error(p):
    if p:
        print(f"Erro Sintático: Token inesperado '{p.value}' na linha {p.lineno}")
    else:
        print("Erro Sintático: Fim de arquivo inesperado")

# Inicializa o parser LALR(1)
parser = yacc.yacc()
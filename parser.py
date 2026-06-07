import ply.yacc as yacc
from lexer import tokens

def p_program(p):
    'program : devices cmds'
    p[0] = p[1] + "\n" + p[2]

def p_devices_multiple(p):
    'devices : device devices'
    p[0] = p[1] + "\n" + p[2]

def p_devices_single(p):
    'devices : device'
    p[0] = p[1]

def p_device_simple(p):
    'device : DISPOSITIVO_KW ABRE_CHAVE NAMEDEVICE FECHA_CHAVE'
    dispositivo = p[3]
    p[0] = f"if '{dispositivo}' not in globals(): {dispositivo} = {{'status': 0, 'observation': 0}}"

def p_device_complete(p):
    'device : DISPOSITIVO_KW ABRE_CHAVE NAMEDEVICE VIRGULA OBSERVATION FECHA_CHAVE'
    dispositivo = p[3]
    sensor = p[5]
    p[0] = f"{sensor} = 0\nif '{dispositivo}' not in globals(): {dispositivo} = {{'status': 0, 'observation': '{sensor}'}}"

def p_cmds_multiple(p):
    'cmds : cmd PONTO cmds'
    p[0] = p[1] + "\n" + p[3]

def p_cmds_single(p):
    'cmds : cmd PONTO'
    p[0] = p[1]

def p_cmd(p):
    '''cmd : attrib
           | obsact
           | act'''
    p[0] = p[1]

def p_attrib_var(p):
    'attrib : SET OBSERVATION IGUAL var'
    p[0] = f"{p[2]} = {p[4]}"

def p_attrib_execute(p):
    'attrib : SET OBSERVATION IGUAL actexecute'
    p[0] = f"{p[2]} = {p[4]}"

def p_var(p):
    '''var : NUM
           | BOOL
           | OBSERVATION'''
    p[0] = str(p[1])

def p_obsact_simple(p):
    'obsact : SE obs ENTAO cmds'
    comandos_indentados = "\n".join(["    " + linha for linha in p[4].split("\n")])
    p[0] = f"if {p[2]}:\n{comandos_indentados}"

def p_obsact_complete(p):
    'obsact : SE obs ENTAO cmds SENAO cmds'
    comandos_if = "\n".join(["    " + linha for linha in p[4].split("\n")])
    comandos_else = "\n".join(["    " + linha for linha in p[6].split("\n")])
    p[0] = f"if {p[2]}:\n{comandos_if}\nelse:\n{comandos_else}"

def p_obs_simple(p):
    'obs : OBSERVATION OPLOGIC var'
    p[0] = f"{p[1]} {p[2]} {p[3]}"

def p_obs_compound(p):
    'obs : OBSERVATION OPLOGIC var AND obs'
    p[0] = f"{p[1]} {p[2]} {p[3]} and {p[5]}"

def p_act_action(p):
    'act : ACTION NAMEDEVICE'
    p[0] = f"{p[1]}('{p[2]}')"

def p_act_alert(p):
    'act : actalert'
    p[0] = p[1]

def p_actexecute(p):
    'actexecute : VERIFICAR ABRE_PARENTESE NAMEDEVICE FECHA_PARENTESE'
    p[0] = f"verificar('{p[3]}')"

def p_action(p):
    '''ACTION : LIGAR
              | DESLIGAR'''
    p[0] = p[1]

def p_actalert_simple(p):
    'actalert : ENVIAR_ALERTA ABRE_PARENTESE MSG FECHA_PARENTESE NAMEDEVICE'
    p[0] = f"alerta_simples('{p[5]}', '{p[3]}')"

def p_actalert_var(p):
    'actalert : ENVIAR_ALERTA ABRE_PARENTESE MSG VIRGULA OBSERVATION FECHA_PARENTESE NAMEDEVICE'
    p[0] = f"alerta_com_var('{p[7]}', '{p[3]}', {p[5]})"

def p_actalert_broadcast(p):
    'actalert : ENVIAR_ALERTA ABRE_PARENTESE MSG FECHA_PARENTESE PARA_TODOS devicelist'
    p[0] = f"for dev in {p[6]}: alerta_simples(dev, '{p[3]}')"

def p_devicelist_multiple(p):
    'devicelist : NAMEDEVICE VIRGULA devicelist'
    p[0] = [p[1]] + p[3]

def p_devicelist_single(p):
    'devicelist : NAMEDEVICE'
    p[0] = [p[1]]

def p_error(p):
    if p:
        print(f"Erro Sintático: Token inesperado '{p.value}' na linha {p.lineno}")
    else:
        print("Erro Sintático: Fim de arquivo inesperado")

parser = yacc.yacc()
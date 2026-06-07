# Trab-Analisadores-Lexicos-e-Sintaticos-ObsAct

PROGRAM -> DEVICES CMDS

DEVICES -> DEVICE DEVICES | DEVICE

DEVICE -> dispositivo: {namedevice}
DEVICE -> dispositivo: {namedevice, observation}

CMDS -> CMD . CMDS | CMD .

CMD -> ATTRIB | OBSACT | ACT

ATTRIB -> set observation = VAR
ATTRIB -> set observation = ACTEXECUTE

OBSACT -> se OBS entao CMDS
OBSACT -> se OBS entao CMDS senao CMDS

OBS -> observation oplogic VAR
OBS -> observation oplogic VAR && OBS

##### Adicionado o observation
VAR -> num | bool | observation

ACT -> ACTION namedevice | ACTALERT

##### ACTION foi substituido por verificar e () adicionados
ACTEXECUTE -> verificar (namedevice)

ACTALERT -> enviar alerta (msg) namedevice
ACTALERT -> enviar alerta (msg, observation) namedevice
##### Regra de enviar alerta para todos adicionado
ACTALERT -> enviar alerta (msg) para todos: DEVICELIST

##### Criado para o alerta para todos funcionar
DEVICELIST -> namedevice, DEVICELIST | namedevice

##### Retirado o verificar
ACTION -> ligar | desligar
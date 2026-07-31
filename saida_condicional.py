from runtime import *

umidade = 0
if 'higrometro' not in globals(): higrometro = {'status': 0, 'observation': 'umidade'}
potencia = 0
if 'umidificador' not in globals(): umidificador = {'status': 0, 'observation': 'potencia'}
umidade = 35
if umidade < 40:
    ligar('umidificador')
    if umidade < 20:
        potencia = 100
    else:
        potencia = 150
else:
    desligar('umidificador')
    potencia = 0
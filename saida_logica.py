from runtime import *

movimento = 0
if 'sensormovimento' not in globals(): sensormovimento = {'status': 0, 'observation': 'movimento'}
luz = 0
if 'sensorluminosidade' not in globals(): sensorluminosidade = {'status': 0, 'observation': 'luz'}
if 'lampada' not in globals(): lampada = {'status': 0, 'observation': 0}
movimento = True
luz = 20
if movimento == True and luz < 50:
    ligar('lampada')
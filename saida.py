from runtime import *

temperatura = 0
if 'Termometro' not in globals(): Termometro = {'status': 0, 'observation': 'temperatura'}
if 'ventilador' not in globals(): ventilador = {'status': 0, 'observation': 0}
if 'celular' not in globals(): celular = {'status': 0, 'observation': 0}
temperatura = 40
if temperatura > 30:
    estado = verificar('ventilador')
    if estado == 1:
        for dev in ['ventilador', 'celular']: alerta_com_var(dev, 'Janela fechada e calor em', temperatura)
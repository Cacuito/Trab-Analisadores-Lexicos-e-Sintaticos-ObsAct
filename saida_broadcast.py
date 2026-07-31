from runtime import *

if 'arcondicionado' not in globals(): arcondicionado = {'status': 0, 'observation': 0}
if 'aquecedor' not in globals(): aquecedor = {'status': 0, 'observation': 0}
if 'painelalerta' not in globals(): painelalerta = {'status': 0, 'observation': 0}
for dev in ['arcondicionado', 'aquecedor', 'painelalerta']: alerta_simples(dev, 'Alerta do sistema: Evacuacao imediata do prédio')
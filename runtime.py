def ligar(namedevice):
    print(f"{namedevice} ligado!")
    return 1

def desligar(namedevice):
    print(f"{namedevice} desligado!")
    return 0

def verificar(namedevice):
    print(f"{namedevice} esta ligado.")
    return 1

def alerta_simples(namedevice, msg):
    print(f"{namedevice} recebeu o alerta:\n")
    print(msg)

def alerta_com_var(namedevice, msg, var):
    print(f"{namedevice} recebeu o alerta:\n")
    print(f"{msg} {var}")
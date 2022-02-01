from settings import Config

def lg(*cadena):
    if Config.DEBUG:
        print(*cadena)

class Partida():
    def __init__(self, _cant_j, _estado):
        self.cant_j = _cant_j
        self.estado = _estado
    def preguntarOtraPartida(self):
        print("¿Desea volver a jugar? Introducza 'y' o 'n'")
        entrada = input()
        if(entrada == 'n' or entrada == 'y'):
            if(entrada == 'n'):
                self.estado = False
        else:
            print("Ingreso una opcion invalida.")
            self.preguntarOtraPartida()

import random

class Partida():
    n_turno = 1
    def __init__(self):
        self.primerJugador = random.randint(0,1)

    def incrementarTurno(self):
        self.n_turno += 1
    def obtenerGanador(self):
        print("fin")

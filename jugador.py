from usuario import *

class Jugador(Usuario):
    def __init__(self):
        self.puntos = 0
        self.estado = True
        self.cartas_obt = []


    def iniciarSesion(self):
        self.nombre_de_usuario = input("Ingrese su nombre de usuario: ")
    def calcularPuntos(self):
        self.puntos = 0
        for n in range(len(self.cartas_obt)):
            self.puntos += self.cartas_obt[n]
        if(self.puntos == 21):
            self.estado = False
        elif(self.puntos > 21):
            for n in range(len(self.cartas_obt)):
                if(self.cartas_obt[n] == 11):
                    self.cartas_obt[n] = 1
                    self.calcularPuntos()
                    return
            self.estado = False
        else:
            pass
    def robarCarta(self, carta, valor, tipo):
        self.cartas_obt.append(valor)
        print(carta, " de ", tipo)
        self.calcularPuntos()

    def seguirJugando(self):
        print("Ingrese 'n' si desea plantarse")
        print("Ingrese 'y' si desea robar otra carta")
        entrada = input()
        if(entrada == 'n' or entrada == 'y'):
            if(entrada == 'n'):
                self.estado = False
        else:
            print("Ingreso una opcion invalida.")
            self.seguirJugando()

from usuario import *

class Jugador(Usuario):
    tipo_de_turno = 0
    puntos = 0
    estado = True

    def iniciarSesion(self):
        self.nombre_de_usuario = input("Ingrese su nombre de usuario: ")
    def robarCarta(self, carta, valor, tipo):
        print(carta, " de ", tipo)
        self.puntos += valor
    def seguirJugando(self):
        print("Ingrese 'n' si desea plantarse")
        print("Ingrese 'y' si desea seguir jugando")
        entrada = input()
        if(entrada == 'n' or entrada == 'y'):
            if(entrada == 'n'):
                self.estado = False
        else:
            print("Ingreso una opcion invalida.")
            self.seguirJugando()

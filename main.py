from partida import *
from jugador import *
from carta import *
import random

def mezclar_cartas(carta):
    list_temporal = []
    for x in range(len(carta)):
        list_temporal.append(carta[x].id)
    for x in range(len(carta)):
        cont_ale = random.randint(0,len(carta)-1)
        temporal = list_temporal[x]
        list_temporal[x] = list_temporal[cont_ale]
        list_temporal[cont_ale] = temporal
    return list_temporal

try:
    print("Iniciando la partida")
    #Mezclamos las cartas
    carta = []
    for x in range(52):
        cont = x//13
        carta.append(Carta(x+1-cont*13, cont, x))
    cartas_mez = mezclar_cartas(carta)
    print(cartas_mez)
    #Creamos la partida y el jugador "casa"
    partida_actual = Partida()
    casa = Jugador()
    casa.nombre_de_usuario = "Casa"
    print("Elija el numero de jugadores en la partida")
    partida_actual.cant_j = int(input())
    jugador = []
    for x in range(partida_actual.cant_j):
        jugador.append(Jugador())
        jugador[x].iniciarSesion()

    print("=================================================================")
    indice = 0
    for x in range(partida_actual.cant_j):
        print(jugador[x].nombre_de_usuario, ":")
        jugador[x].robarCarta(carta[cartas_mez[indice]].numero, carta[cartas_mez[indice]].valor, carta[cartas_mez[indice]].tipo)
        indice += 1
    print(casa.nombre_de_usuario, ":")
    casa.robarCarta(carta[cartas_mez[indice]].numero, carta[cartas_mez[indice]].valor, carta[cartas_mez[indice]].tipo)
    indice += 1
    print("----------------------------------------------------------------")
    for x in range(partida_actual.cant_j):
        print(jugador[x].nombre_de_usuario, ":")
        jugador[x].robarCarta(carta[cartas_mez[indice]].numero, carta[cartas_mez[indice]].valor, carta[cartas_mez[indice]].tipo)
        print("Su puntaje es: ", jugador[x].puntos)
        indice += 1
    print("----------------------------------------------------------------")
    for x in range(partida_actual.cant_j):
        if(jugador[x].estado == True):
            print(jugador[x].nombre_de_usuario, ":")
            while(jugador[x].estado):
                jugador[x].seguirJugando()
                if(jugador[x].estado == False):
                    break
                jugador[x].robarCarta(carta[cartas_mez[indice]].numero, carta[cartas_mez[indice]].valor, carta[cartas_mez[indice]].tipo)
                indice += 1
                print("Su puntaje es: ", jugador[x].puntos)
        print("-------------------------------------------------------------")
    print(casa.nombre_de_usuario, ":")
    while(casa.estado):
        casa.robarCarta(carta[cartas_mez[indice]].numero, carta[cartas_mez[indice]].valor, carta[cartas_mez[indice]].tipo)
        indice += 1
        print("El puntaje de la casa es: ", casa.puntos)
        if(casa.puntos > 16):
            casa.estado = False
    print("-------------------------------------------------------------")
    for x in range(partida_actual.cant_j):
        if(jugador[x].puntos > 21):
            print(jugador[x].nombre_de_usuario, " perdiste.")
        else:
            if(jugador[x].puntos == casa.puntos):
                print(jugador[x].nombre_de_usuario, " empataste.")
            elif(jugador[x].puntos > casa.puntos):
                print(jugador[x].nombre_de_usuario, " ganaste.")
            else:
                print(jugador[x].nombre_de_usuario, " perdiste.")
finally:
    print("finnnnnnnnn")

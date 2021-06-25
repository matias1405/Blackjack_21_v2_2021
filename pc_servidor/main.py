from partida import *
from jugador import *
from carta import *
import random
import socket

#funcion para mezclar las cartas
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

#funcion para recibir datos
#recibe un dato del cliente y lo devuelve decodificado
def recibirDatos():
    dato_recibido = b''
    dato_recibido = connection.recv(128)
    return dato_recibido.decode()

#funcion para enviar datos
#primero espera un msj del cliente solicitando un dato
#se compara y se responde si es el dato esperado o no
#si es la peticion esperada se envia el dato que solicito el cliente
def enviarDatos(dato_esperado, dato_a_enviar):
    dato_a_enviar = str(dato_a_enviar)
    dato = ""
    while (True):
        dato = recibirDatos()
        if(dato == dato_esperado):
            respuesta = "si"
            connection.send(respuesta.encode())
            break
        else:
            respuesta = "no"
            connection.send(respuesta.encode())
    connection.send(dato_a_enviar.encode())

#funcion para jugar una partida
#solo se necesita como parametro el numero de jugadores
def crear_partida(cant_jug_part_actual):
    print("Iniciando la partida")
    #Mezclamos las cartas
    cartas_mez = mezclar_cartas(carta)
    print(cartas_mez)
    #Creamos la partida y el jugador "casa"
    partida_actual = Partida(1, True)
    casa = Jugador()
    casa.nombre_de_usuario = "Casa00"
    casa.nombre = "Casa"
    partida_actual.cant_j = cant_jug_part_actual
    jugador = []
    #creamos el jugador de la pc servidor
    jugador.append(Jugador())
    jugador[0].iniciarSesion()
    #si son dos jugadores pedimos los datos al jugador de la pc cliente
    if(partida_actual.cant_j == 2):
        jugador.append(Jugador())
        jugador[1].nombre_de_usuario = recibirDatos()
        jugador[1].nombre = recibirDatos()
        #se envia el nombre del jugador que juega en la pc servidor
        enviarDatos("nombre0", jugador[0].nombre)

    print("=================================================================")
    #roba primera carta el jugador de la pc servidor
    indice = 0
    print(jugador[0].nombre , ":")
    jugador[0].robarCarta(carta[cartas_mez[indice]].numero, carta[cartas_mez[indice]].valor, carta[cartas_mez[indice]].tipo)
    indice += 1
    #si existe, roba la primera carta el jugador de la pc cliente
    if(partida_actual.cant_j == 2):
        enviarDatos(jugador[0].nombre, cartas_mez[indice-1])
        print(jugador[1].nombre , ":")
        jugador[1].robarCarta(carta[cartas_mez[indice]].numero, carta[cartas_mez[indice]].valor, carta[cartas_mez[indice]].tipo)
        indice += 1
        enviarDatos(jugador[1].nombre, cartas_mez[indice-1])
    #roba la primera carta la casa
    print(casa.nombre, ":")
    casa.robarCarta(carta[cartas_mez[indice]].numero, carta[cartas_mez[indice]].valor, carta[cartas_mez[indice]].tipo)
    indice += 1
    if(partida_actual.cant_j == 2):
        enviarDatos(casa.nombre, cartas_mez[indice-1])
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
                if(casa.puntos > 21):
                    print(jugador[x].nombre, " ganaste")
                else:
                    print(jugador[x].nombre_de_usuario, " perdiste.")
    partida_actual.preguntarOtraPartida()
    if(partida_actual.estado):
        crear_partida(cant_jug_part_actual)

################################################################################
#PROGRAMA PRINCIPAL
################################################################################
# Creacion de un socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#condiciones iniciales para la primera partida
print("Bienvenidos")
#creamos las cartas
carta = []
for x in range(52):
    cont = x//13
    carta.append(Carta(x+1-cont*13, cont, x))
#eleccion de la cantidad de jugadores
cant_jug_part_actual = int(input("Elija el numero de jugadores de la partida \n"))
if(cant_jug_part_actual == 2):
    #obtenemos la iplocal de esta pc
    ip = socket.gethostbyname(socket.gethostname())
    print("Introduzca la siguiente direccion en la otra PC: ", ip)
    ip_cliente = input("Introduzca la direccion ip dada por la otra PC: ")
    # Bind the socket to the port
    server_address = (ip_cliente, 10000)
    print("starting up on ", server_address(0), " port ", server_address(1))
    sock.bind(server_address)
    # Listen for incoming connections
    sock.listen(1)
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    print('connection from', client_address)
    try:
        crear_partida(cant_jug_part_actual)
    finally:
        # cerramos la conexion
        connection.close()
else:
    crear_partida(cant_jug_part_actual)

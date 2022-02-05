from clases import *
import random
import socket


def getIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.connect(('<broadcast>', 0))
    ip = s.getsockname()[0]
    s.close()
    return ip

#===============================================================================

def cantidad_jug():
    #eleccion de la cantidad de jugadores
    cantidad = int(input("Elija el numero de jugadores de la partida \n"))
    if cantidad != 2:
        cantidad = 1
    return cantidad

#===============================================================================

#funcion para recibir datos
#recibe un dato del cliente y lo devuelve decodificado
def recibirDatos():
    dato_recibido = connection.recv(128)
    return dato_recibido.decode()

#===============================================================================

#funcion para enviar datos
def enviarDatos(dato):
    connection.send(dato.encode())

#===============================================================================

#funcion para jugar una partida
#solo se necesita como parametro el numero de jugadores
def crear_partida(cant_jug):
    print("\nIniciando la partida...")
    #Creamos la partida y el jugador "casa"
    partida = Partida(cant_jug, True)
    casa = Jugador()
    casa.nombre_de_usuario = "Casa00"
    casa.nombre = "Casa"
    #Mezclamos las cartas
    random.shuffle(mazo)
    lista_jug = []
    #creamos el jugador de la pc servidor
    lista_jug.append(Jugador())
    lista_jug[0].iniciarSesion()
    #si son dos jugadores pedimos los datos al jugador de la pc cliente
    if(partida.cant_j == 2):
        #se envia el nombre del jugador que juega en la pc servidor
        enviarDatos(f'usuario {lista_jug[0].nombre_de_usuario}')
        enviarDatos(f'nombre {lista_jug[0].nombre}')
        lista_jug.append(Jugador())
        enviarDatos('usuario2')
        lista_jug[1].nombre_de_usuario = recibirDatos()
        enviarDatos('nombre2')
        lista_jug[1].nombre = recibirDatos()
    lista_jug.append(casa)

    #roba primera carta cada jugador y la casa
    ind = 0
    ind = repartir_carta(lista_jug, ind, cant_jug, False)
    #roba la segunda carta cada jugador pero no la casa
    ind = repartir_carta(lista_jug[:-1], ind, cant_jug)
    #continua el juego jugador de la pc servidor
    while(lista_jug[0].estado):
        lista_jug[0].seguirJugando()
        if(lista_jug[0].estado == False):
            break
        ind = repartir_carta(lista_jug[0], ind, cant_jug)
    #juega si existe el jugador de la pc ip_cliente
    if cant_jug == 2:
        while(lista_jug[1].estado):
            enviarDatos('seguirjugando')
            estado_jugador = recibirDatos()
            if estado_jugador == 'n':
                lista_jug[1].estado = False
                break
            ind = repartir_carta(lista_jug[1], ind, cant_jug)
    #juega la casa, la casa se planta de obtener mas de 16
    while(casa.estado):
        ind = repartir_carta(lista_jug[-1], ind, cant_jug)
        if(casa.puntos > 16):
            casa.estado = False

    #mostramos los resultados otenidos
    resultados(lista_jug[:-1], casa)
    partida.preguntarOtraPartida()
    if(partida.estado):
        crear_partida(partida.cant_j)

#===============================================================================

def repartir_carta(lista, ind, cant_jug, mostrar_puntaje = True):
    if type(lista) is not list:
        lista = [lista]
    for jugador in lista:
        print(f'{jugador.nombre} :')
        jugador.robarCarta(mazo[ind].numero, mazo[ind].valor, mazo[ind].tipo)
        if(cant_jug == 2):
            enviarDatos(f'{jugador.nombre_de_usuario} {mazo[ind].id}')
        if mostrar_puntaje:
            print(f'El puntaje de {jugador.nombre} es {jugador.puntos}')
        ind += 1
        print("\n-----------------------------------------------------------\n")
    return ind

#===============================================================================

def resultados(lista_jug, casa):
    print("\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
    for jugador in lista_jug:
        if(jugador.puntos > 21):
            print(jugador.nombre, "perdió.\n")
        elif(jugador == 21):
            print(jugador.nombre, "hizo BLACKJACK.\n")
        elif(jugador.puntos == casa.puntos):
            print(jugador.nombre, "empató.\n")
        elif(jugador.puntos > casa.puntos):
            print(jugador.nombre, "ganó.\n")
        elif(casa.puntos > 21):
            print(jugador.nombre, "ganó.\n")
        else:
            print(jugador.nombre, "perdió.\n")

################################################################################
#PROGRAMA PRINCIPAL
################################################################################

if __name__ == '__main__':
    print("**************************************")
    print("\nBIENVENIDO AL BLACKJACK 21 V2\n")
    print("**************************************\n")
    #creamos las cartas
    mazo = []
    for x in range(52):
        cont = x//13
        mazo.append(Carta(x+1-cont*13, cont, x))

    cant_jugagores = cantidad_jug()

    if(cant_jugagores == 2):
        #obtenemos la iplocal de esta pc
        ip = getIp()
        # Creacion de un socket TCP/IP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
            crear_partida(cant_jugagores)
        finally:
            # cerramos la conexion
            connection.close()
    else:
        crear_partida(cant_jugagores)

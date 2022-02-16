#include <iostream>
#include <sys/types.h>
#include <sys/socket.h>
#include <string>
#include <thread>         // std::this_thread::sleep_for
#include <chrono>         // std::chrono::seconds
#include <vector>
#include <cstring>
#include <netdb.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

using namespace std;

//========================== definicion de clases ==============================

int sockfd;
char buffer_tx[255];
char buffer_rx[255];


class Carta{
public:
    int numero, valor, id;
    string tipo;
    Carta(int n, int t, int i){
        numero = n;
        if(numero >= 10){
            valor = 10;
        }
        else if(numero == 1){
            valor = 11;
        }
        else{
            valor = n;
        }
        if(t == 0){
            tipo = "corazon";
        }
        else if(t == 1){
            tipo = "diamante";
        }
        else if(t == 2){
            tipo = "trebol";
        }
        else{
            tipo = "pica";
        }
        id = i;
    }
};

vector<Carta> mazo;

class Jugador{
public:
    string nombre_de_usuario = "anon";
    string nombre;
    int puntos, cont;
    bool estado;
    int cartas_obt[12];

    void inicio(){
        puntos = 0;
        cont = 0;
        estado = true;
        for(int i=0; i < (sizeof(cartas_obt)/4); i++){
            cartas_obt[i] = 0;
        }
    }
    void iniciarSesion(){
        cout << endl << "---------------------------------------------" << endl;
        cout << "Ingrese su nombre de usuario: ";
        cin >> this->nombre_de_usuario;
        cout << "Ingrese su nombre: ";
        cin >> this->nombre;
        cout << endl << "---------------------------------------------" << endl;
    }

    void robarCarta(int id){
        cartas_obt[cont] = mazo[id].valor;
        cout << mazo[id].numero << " de " << mazo[id].tipo << endl;
        cont += 1;
        this->calcularPuntos();
        if (cartas_obt[1] != 0){
            cout << endl << "El puntaje de " << nombre;
            cout << " es :" << this->puntos << "." << endl;
        }
    }

    void calcularPuntos(){
        this->puntos = 0;
        for(int i = 0; i<(sizeof(cartas_obt)/4); i++){
            this->puntos += cartas_obt[i];
        }
        if(this->puntos == 21){
            estado = false;
        }
        if(this->puntos > 21){
            for(int i=0; i<(sizeof(cartas_obt)/4); i++){
                if (cartas_obt[i] == 11){
                    cartas_obt[i] = 1;
                    this->puntos -= 10;
                    break;
                }
            }
            if(this->puntos >= 21){
                estado = false;
            }
        }
    }

    string seguirjugando(){
        string respuesta;
        if (estado == false){
            return "n";
        }
        cout << endl << nombre << ":" << endl;
        cout << endl << "Ingrese 'n' si desea plantarse" << endl;
        cout << "Ingrese 'y' si desea robar otra carta" << endl;
        cin >> respuesta;
        if(respuesta == "n" || respuesta == "y"){
            if(respuesta == "n"){
                estado = false;
            }
        }
        else{
            cout << "Ingreso una opcion invalida." << endl;
            respuesta = this->seguirjugando();
        }
        cout << endl << "---------------------------------------------" << endl;
        return respuesta;
    }

    string obtenerNomber(){
        return nombre;
    }
};

//======================== definicion de funciones =============================

void Enviar(string estado){
    //this_thread::sleep_for(chrono::milliseconds(500));
    for(int i=0; i < estado.length(); i++){
        buffer_tx[i] = estado[i];
    }
    //cout << estado << endl;
    write(sockfd, buffer_tx, sizeof(buffer_tx));
    memset(buffer_tx, 0, sizeof(buffer_tx));
}


string Recibir(){
    string estado;
    read(sockfd, buffer_rx, sizeof(buffer_rx));
    //cout << "El servidor dice: " << buffer_rx << endl;
    estado = buffer_rx;
    memset(buffer_rx, 0, sizeof(buffer_rx));
    return estado;
}

//============================ programa principal ==============================



int main(){

    //=============creacion y conexion del socket TCP IP========================

    struct sockaddr_in servaddr;
    char ip[] = "192.168.1.9";
    string estado, palabra;
    size_t pos = 0;
    cout<<"Conectando al servidor..."<<endl<<endl;
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    cout << "Ingrese la ip de la PC servidor: " << endl;
    memset(&servaddr, 0, sizeof(servaddr));
    //cin >> ip;
    servaddr.sin_addr.s_addr = inet_addr(ip);
    servaddr.sin_family = AF_INET;
    servaddr.sin_port = htons(10000);
    connect(sockfd, (struct sockaddr*) &servaddr, sizeof(servaddr));
    cout << "Conectado al Servidor!" << endl;

    //================ creacion de objetos cartas y jugadores ==================

    for(int x=0; x < 52; x++){
        int cont = x/13;
        mazo.push_back(Carta(x+1-cont*13, cont, x));
    }
    Jugador jugador_cl = Jugador();
    Jugador jugador_se = Jugador();

    //creacion del jugador casa
    Jugador casa = Jugador();
    casa.nombre_de_usuario = "casa00";
    casa.nombre = "Casa";

    //========================== inicio del juego ==============================

    while(true){
        estado = Recibir();
        if ((pos = estado.find(" ")) == string::npos){
            palabra = estado;
        }
        else{
            palabra = estado.substr(0, pos);
            estado.erase(0, pos+1);
        }
        if (palabra == "inicio"){
            jugador_cl.inicio();
            jugador_cl.iniciarSesion();
            casa.inicio();
            jugador_se.inicio();
            Enviar("ok");
        }
        else if (palabra == "usuario"){
            jugador_se.nombre_de_usuario = estado;
            Enviar("ok");
        }
        else if (palabra == "nombre"){
            jugador_se.nombre = estado;
            cout << endl << "El nombre del otro jugador es: ";
            cout << jugador_se.nombre << endl;
            cout << endl << "---------------------------------------------" << endl;
            Enviar("ok");
        }
        else if (palabra == "usuario2"){
            Enviar(jugador_cl.nombre_de_usuario);
        }
        else if (palabra == "nombre2"){
            Enviar(jugador_cl.nombre);
        }
        else if (palabra == jugador_se.nombre_de_usuario){
            cout << endl << jugador_se.nombre << ":" << endl;
            Enviar("ok");
            estado = Recibir();
            int id = stol(estado);
            jugador_se.robarCarta(id);
            cout << endl << "---------------------------------------------" << endl;
            Enviar("ok");
        }
        else if (palabra == jugador_cl.nombre_de_usuario){
            cout << endl << jugador_cl.nombre << ":" << endl;
            Enviar("ok");
            estado = Recibir();
            int id = stol(estado);
            jugador_cl.robarCarta(id);
            cout << endl << "---------------------------------------------" << endl;
            Enviar("ok");
        }
        else if (palabra == casa.nombre_de_usuario){
            cout << endl << casa.nombre << ":" << endl;
            Enviar("ok");
            estado = Recibir();
            int id = stol(estado);
            casa.robarCarta(id);
            cout << endl << "---------------------------------------------" << endl;
            Enviar("ok");
        }
        else if (palabra == "seguirjugando"){
            Enviar(jugador_cl.seguirjugando());
        }
        else if (palabra == "resultados"){
            cout << endl << "Resultados:" << endl;
            if(jugador_se.puntos > 21){
                cout << endl << jugador_se.nombre << " perdió." << endl;
            }
            else if(jugador_se.puntos == 21){
                cout << endl << jugador_se.nombre << " hizo BLACKJACK." << endl;
            }
            else if(jugador_se.puntos == casa.puntos){
                cout << endl << jugador_se.nombre << " empató." << endl;
            }
            else if(jugador_se.puntos > casa.puntos){
                cout << endl << jugador_se.nombre << " ganó." << endl;
            }
            else if(casa.puntos > 21){
                cout << endl << jugador_se.nombre << " ganó." << endl;
            }
            else{
                cout << endl << jugador_se.nombre << " perdió." << endl;
            }

            //-----------------------------------------------------------------

            if(jugador_cl.puntos > 21){
                cout << endl << jugador_cl.nombre << " perdió." << endl;
            }
            else if(jugador_cl.puntos == 21){
                cout << endl << jugador_cl.nombre << " hizo BLACKJACK." << endl;
            }
            else if(jugador_cl.puntos == casa.puntos){
                cout << endl << jugador_cl.nombre << " empató." << endl;
            }
            else if(jugador_cl.puntos > casa.puntos){
                cout << endl << jugador_cl.nombre << " ganó." << endl;
            }
            else if(casa.puntos > 21){
                cout << endl << jugador_cl.nombre << " ganó." << endl;
            }
            else{
                cout << endl << jugador_cl.nombre << " perdió." << endl;
            }
            cout << endl << "---------------------------------------------" << endl;
            Enviar("ok");
        }
        else if (palabra == "cerrarconexion"){
            cout << endl << "fin del juego" << endl;
            Enviar("ok");
            break;
        }
    }

    //========================= cierre de la conexion ==========================

    close(sockfd);
    cout << "Cerrando conexion" << endl << endl;
    return 0;
}

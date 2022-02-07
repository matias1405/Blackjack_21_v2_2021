#include <iostream>
#include <winsock2.h>
#include <string>
#include <vector>

using namespace std;

//========================== definicion de clases ==============================

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


class Jugador{

};

//======================== definicion de funciones =============================

void Enviar(){
    cout<<"Escribe el mensaje a enviar: ";
    cin>>buffer;
    send(server, buffer, sizeof(buffer), 0);
    memset(buffer, 0, sizeof(buffer));
    cout << "Mensaje enviado!" << endl;
}


string Recibir(){
    string estado;
    recv(server, buffer, sizeof(buffer), 0);
    cout << "El servidor dice: " << buffer << endl;
    estado = buffer;
    memset(buffer, 0, sizeof(buffer));
    return estado;
}

//============================ programa principal ==============================

int main(){

    //=============creacion y conexion del socket TCP IP========================

    SADATA WSAData;
    SOCKET server;
    SOCKADDR_IN addr;
    char buffer[1024];
    char ip[15];
    string estado, palabra;
    size_t pos = 0;
    cout<<"Conectando al servidor..."<<endl<<endl;
    WSAStartup(MAKEWORD(2,0), &WSAData);
    server = socket(AF_INET, SOCK_STREAM, 0);
    cout << "Ingrese la ip de la PC servidor: " << endl;
    cin >> ip;
    addr.sin_addr.s_addr = inet_addr(ip);
    addr.sin_family = AF_INET;
    addr.sin_port = htons(10000);
    connect(server, (SOCKADDR *)&addr, sizeof(addr));
    cout << "Conectado al Servidor!" << endl;

    //================ creacion de objetos cartas y jugadores ==================

    vector<Carta> mazo;
    for(int x=0; x < 52; x++){
        int cont = x/13;
        mazo.push_back(Carta(j+1-cont*13, cont, x));
    }
    Jugador jugador_cl = Jugador();
    Jugador jugador_se = Jugador();

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
        cout << palabra << endl;
        if (palabra == "inicio"){
            cout << "matias" <<endl;
        }
        else if (palabra == "usuario"){
            cout << "alfaro" <<endl;
        }
        else if (palabra == "nombre"){
            cout << "alfaro" <<endl;
        }
        else if (palabra == "usuario2"){
            cout << "hola de nuevo" <<endl;
        }
        else if (palabra == "nombre2"){
            cout << "hola de nuevo" <<endl;
        }
        else if (palabra == jugador1){
            cout << "hola de nuevo" <<endl;
        }
        else if (palabra == jugador2){
            cout << "hola de nuevo" <<endl;
        }
        else if (palabra == "seguirjugando"){
            cout << "hola de nuevo" <<endl;
        }
        else if (palabra == "resultados"){
            cout << "alfaro" <<endl;
        }
        else{
            cout << "intentalo nuevamente" <<endl;
        }
    }

    //========================= cierre de la conexion ==========================

    closesocket(server);
    WSACleanup();
    cout << "Cerrando conexion" << endl << endl;
    return 0
}

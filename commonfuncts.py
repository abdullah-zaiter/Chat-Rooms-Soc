import socket
import sys
import logging

#variaveis globais do programa:
#conexao socket do servidor
s = socket.socket()
#lista de TODOS os usuarios conectados ao servidor
All_Users = list()
#lista de TODAS as salas disponiveis no servidor
Chat_rooms = list()

logging.basicConfig(filename='server.log', filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO)

#funcao que recebe uma string e uma conexao socket, manda a string e espera a resposta do cliente.
#retorna a string enviada pelo cliente
def send_receive_string(msgp, socket_client):
    msg = msgp
    data = ""
    socket_client.send(msg)
    while data == "":
        try:
            data = socket_client.recv(1024)
        except (KeyboardInterrupt, SystemExit):
            s.close()
            sys.exit(0)
        except Exception as x:
            print(x.message)
            break
    return data

#dada uma conexao socket, esta funcao retorna o indice dessa conexao no vetor de usuarios
def from_socket_conn_to_index(socket_client):
    for i in range(len(All_Users)):
        if(socket_client == All_Users[i].Connection):
            return i
    return None

#dado um nome de sala esta funcao retorna a indice dessa sala no vetor de salas
def from_room_name_to_index(name):
    for i in range(len(Chat_rooms)):
        if(name == Chat_rooms[i].Name):
            return i
    return None

#dado uma conexao socket, essa funcao retorna o indice da sala que esse usuario esta conectado
#retorna tambem o indice dele no vetor de usuarios dentro da sala.
def from_socket_conn_to_room_index(socket_client):
    for i in range(len(Chat_rooms)):    
        for j in range(len(Chat_rooms[i].Users)):
            if(socket_client == Chat_rooms[i].Users[j].Connection):
                return i,j
    return None,None

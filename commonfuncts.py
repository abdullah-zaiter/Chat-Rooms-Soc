import socket
import sys

s = socket.socket()
All_Users = list()
Chat_rooms = list()

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

def from_socket_conn_to_index(socket_client):
    for i in range(len(All_Users)):
        if(socket_client == All_Users[i].Connection):
            return i
    return None

def from_room_name_to_index(name):
    for i in range(len(Chat_rooms)):
        if(name == Chat_rooms[i].Name):
            return i
    return None

def from_socket_conn_to_room_index(socket_client):
    for i in range(len(Chat_rooms)):    
        for j in range(len(Chat_rooms[i].Users)):
            if(socket_client == Chat_rooms[i].Users[j].Connection):
                return i,j

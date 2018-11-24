import socket
import threading
import sys
from user import User
from chatroom import ChatRoom

Chat_rooms = list()
All_Users = list()

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

def delete_user(socket_client):
    index = from_socket_conn_to_index(socket_client)
    All_Users[index].close_connection()
    print("User "+ All_Users[index].Username + "signed out.")        
    del All_Users[index]
    socket_client.close()

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

def compare_string_to_existing_names(name):
    for i in range(len(All_Users)):
        if(name == All_Users[i].Username):
            return True
    return False

def signup_client(socket_client):
    msg = "Enter your name: "
    index = from_socket_conn_to_index(socket_client)
    name = send_receive_string(msg, socket_client)
    while(compare_string_to_existing_names(name)):
        msg = "This Username("+name+") is already used, choose another one: "
        name = send_receive_string(msg, socket_client)
    if len(All_Users[index].Username)>=1:
        socket_client.send("Username Updated to " + name)
        print("Username Updated to " + name)
    else:
        socket_client.send("New User Added " + name)        
        print("New User Added " + name)
    All_Users[index].Username = name

def signout_client(socket_client):
    msg = "Are you sure you want to sign out ? (Y/N) "
    answer = send_receive_string(msg, socket_client)
    if(answer == "Y" or answer == "y"):
        delete_user(socket_client)

def check_users(socket_client):
    j = 0
    msg = ""
    for i in range(len(All_Users)):
        if(len(All_Users[i].Username)>=1):
            j += 1
            if(All_Users[i].Connection == socket_client):
                msg += "User "+str(j)+": YOU.\n"
            else:
                msg += "User "+str(j)+": "+All_Users[i].Username+".\n"
    
    if(j==0):
        msg = "No one is connected to server."
    socket_client.send(msg)

def check_chatrooms(socket_client):
    j = 0
    msg = ""
    for i in range(len(Chat_rooms)):
        if(len(Chat_rooms[i].Name)>=1):
            j += 1
            msg += "Chat room "+str(j)+": "+Chat_rooms[i].Name+". \n"    
    if(j==0):
        msg = "No open chat rooms."
    socket_client.send(msg)

def create_chatroom(socket_client):
    msg = "Enter room name: "
    name = send_receive_string(msg, socket_client)
    msg = "Enter room type (normal or private): "
    ttype = send_receive_string(msg, socket_client)
    password = ""
    index = from_socket_conn_to_index(socket_client)
    user = All_Users[index]
    if (ttype == "private" or ttype == "PRIVATE"):
        msg = "Enter room password: "
        password = send_receive_string(msg, socket_client)
    socket_client.send("New room "+name+" created successfully" )        
    print("New room created " + name)
    Chat_rooms.append(ChatRoom(name,ttype,user,password))

def enter_chatroom(socket_client):
    if(len(Chat_rooms)<=0):
        socket_client.send("No open rooms now, open one or wait for someone else to do so.")
    else:
        socket_client.send("Available rooms, choose one:")
        check_chatrooms(socket_client)
        room = send_receive_string("", socket_client)
        index = from_room_name_to_index(room)
        Chat_rooms[index].Users.append(All_Users[from_socket_conn_to_index(socket_client)])
        socket_client.send("Welcome to "+Chat_rooms[index].Name+" room! ")


def broadcast_usr(socket_client):
    #maquina de estados aqui, variavel state
    state = 1
    while True:
        try:
            data = socket_client.recv(1024)
            if state == 1:
                if (data == "A" or data == "a"):
                    signup_client(socket_client)
                    state = 2
                else:
                    socket_client.send("Access denied, Register your username by clicking A.")
            elif (state == 2):
                if (data == "A" or data == "a"):
                    signup_client(socket_client)
                elif (data == "B" or data == "b"):
                    check_users(socket_client)
                elif (data == "C" or data == "c"):
                    check_chatrooms(socket_client)
                elif (data == "D" or data == "d"):
                    enter_chatroom(socket_client)
                elif (data == "E" or data == "E"):
                    create_chatroom(socket_client)
                elif (data == "F" or data == "f"):
                    signout_client(socket_client)
                    return  
            #b_usr(socket_client, data)
        except Exception as x:
            print(x.message)
            break
        except (KeyboardInterrupt, SystemExit):
            print("wtffffff")
            kill_all()


def b_usr(cs_sock, msg):
    for client in CONNECTIONS:
        if client != cs_sock:
            client.send(msg)


if __name__ == "__main__":
    # socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # bind
    HOST = 'localhost'
    PORT = 5023
    s.bind((HOST, PORT))
    # listen
    s.listen(1)
    print('Chat server started on port : ' + str(PORT))
    while True:
        j = 0 
        for i in range(len(All_Users)):
           if(len(All_Users[i].Username)>=1):
                j+=1
                print("User "+str(j)+": "+All_Users[i].Username)
        try:
            socket_client, cli_add = s.accept()
            All_Users.append(User(socket_client))
            thread_client = threading.Thread(
                target=broadcast_usr, args=[socket_client])
            thread_client.start()
        except (KeyboardInterrupt, SystemExit):
            s.close()
            sys.exit(0)


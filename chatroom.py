from commonfuncts import *

class ChatRoom:
    Name = ""
    Type = ""  
    Users = list()
    Password = ""
    def __init__(self, name,ttype, user, password):
        self.Name = name

        self.Type = ttype
        self.Users.append(user)
        if(self.Type== "PRIVATE" or self.Type== "private"):
            self.Password = password     
        else:
            self.Type = "Open"
    def send_to_all_users(self, msg, cs_sock):
        Room_Connections = []
        sender_name = ""
        for i in range(len(self.Users)):
            if (self.Users[i].Connection == cs_sock):
                sender_name = self.Users[i].Username
            Room_Connections.append(self.Users[i].Connection)
        msg = sender_name + " - " + msg
        for client in Room_Connections:
            if client != cs_sock:
                client.send(msg)
    def check_room_users(self, cs_sock):
        j = 0
        msg = ""
        for i in range(len(self.Users)):
            if(len(self.Users[i].Username)>=1):
                j += 1
                if(self.Users[i].Connection == cs_sock):
                    msg += "User "+str(j)+": YOU.\n"
                else:
                    msg += "User "+str(j)+": "+self.Users[i].Username+".\n"
        if(j==0):
            msg = "No one is in the room."
        cs_sock.send(msg)
    def welcoming_message(self, cs_sock):
        self.send_to_all_users("Entered This Chat room!", cs_sock)
        cs_sock.send("Welcome to '"+ self.Name +"' ! feel free to  share your thoughts, not fake news.")
    def exiting_message(self, cs_sock):
        self.send_to_all_users("Signed out!", cs_sock)
    def add_user(self, user):
        self.Users.append(user)
        self.welcoming_message(user.Connection)
    def delete_user(self, user):
        self.exiting_message(user.Connection)
        self.Users.remove(user) 

def check_chatrooms(socket_client):
    j = 0
    msg = ""
    for i in range(len(Chat_rooms)):
        if(len(Chat_rooms[i].Name)>=1):
            j += 1
            msg += "Chat room "+str(j)+": "+Chat_rooms[i].Name+", "+str(len(Chat_rooms[i].Users))+" User(s) connected. \n"    
    if(j==0):
        msg = "No open chat rooms."
    socket_client.send(msg)

def compare_string_to_existing_roomnames(name):
    for i in range(len(Chat_rooms)):
        if(name == Chat_rooms[i].Name):
            return True
    return False

def create_chatroom(socket_client):
    msg = "Enter room name: "
    name = send_receive_string(msg, socket_client)
    while(compare_string_to_existing_roomnames(name)):
        msg = "This room name("+name+") is already used, choose another one: "
        name = send_receive_string(msg, socket_client)
    msg = "Enter room type (open or private): "
    ttype = send_receive_string(msg, socket_client)
    password = ""
    index = from_socket_conn_to_index(socket_client)
    user = All_Users[index]
    if (ttype == "private" or ttype == "PRIVATE"):
        msg = "Enter room password: "
        password = send_receive_string(msg, socket_client)
    print("New room created " + name)
    Chat_rooms.append(ChatRoom(name,ttype,user,password))
    socket_client.send("New "+Chat_rooms[-1].Type+" room '"+name+"' created successfully")        

def enter_chatroom(socket_client):
    if(len(Chat_rooms)<=0):
        socket_client.send("No open rooms now, create one or wait for someone else to do so.")
    else:
        socket_client.send("Available rooms, choose one:\n")
        check_chatrooms(socket_client)
        room = send_receive_string("", socket_client)
        index = from_room_name_to_index(room)
        if(Chat_rooms[index].Type == "PRIVATE" or Chat_rooms[index].Type == "private"):
            msg = "Private room, Enter password: "
            password = send_receive_string(msg, socket_client)
            if(password == Chat_rooms[index].Password):
                Chat_rooms[index].add_user(All_Users[from_socket_conn_to_index(socket_client)])
            else:
                i = 1
                while (i<3 and password != Chat_rooms[index].Password):
                    i += 1
                    msg = "wrong password, try again: "
                    password = send_receive_string(msg, socket_client)
                    if(password == Chat_rooms[index].Password):
                        Chat_rooms[index].add_user(All_Users[from_socket_conn_to_index(socket_client)])
                        break
        else:
            Chat_rooms[index].add_user(All_Users[from_socket_conn_to_index(socket_client)])
                        

def exit_chatroom(socket_client):
    index, j= from_socket_conn_to_room_index(socket_client)
    Chat_rooms[index].delete_user(Chat_rooms[index].Users[j])
    if len(Chat_rooms[index].Users)<=0:
        print("Room '"+Chat_rooms[index].Name+"' is empty now, deleting.")
        del Chat_rooms[index]
        pass

def send_msg_to_current_room(msg, socket_client):
    index,j = from_socket_conn_to_room_index(socket_client)
    Chat_rooms[index].send_to_all_users(msg,socket_client)

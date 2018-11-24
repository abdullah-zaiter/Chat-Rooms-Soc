from commonfuncts import *

class User:
    Connection = socket.socket()
    Username = ""
    def __init__(self, connection):
        self.Connection = connection
    def send_message(self, msg):
        self.Connection.send(msg)
    def close_connection(self):
        self.Connection.close()

def compare_string_to_existing_usernames(name):
    for i in range(len(All_Users)):
        if(name == All_Users[i].Username):
            return True
    return False

def delete_user(socket_client):
    index = from_socket_conn_to_index(socket_client)
    All_Users[index].close_connection()
    print("User "+ All_Users[index].Username + "signed out.")        
    del All_Users[index]
    socket_client.close()
def signup_client(socket_client):
    msg = "Enter your name: "
    index = from_socket_conn_to_index(socket_client)
    name = send_receive_string(msg, socket_client)
    while(compare_string_to_existing_usernames(name)):
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

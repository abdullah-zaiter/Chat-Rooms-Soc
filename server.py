import socket, threading

class Chat_room:
    Name = ""
    Type = ""  
    Users = []
    Password = ""
    def __init__(self, Name,Type, User, Password):
        self.Name = Name
        self.Type = Type
        self.Users.append(User)
        if(Type== "PRIVATE"):
            self.Password = Password   

Chat_room = []
Users = []
CONNECTIONS  = []

def listening_client():
    while True:
        #accept    
        cli_sock, cli_add = ser_sock.accept()
        CONNECTIONS.append(cli_sock)
        thread_client = threading.Thread(target = broadcast_usr, args=[cli_sock])
        thread_client.start()

def signup_client(cli_sock):
    data = ""
    while data == "":
        try:
            data = cli_sock.recv(1024)
            Users.append(data)
            print("New User Added " + data)
        except Exception as x:
            print(x.message)
            break

def broadcast_usr(cli_sock):
    while True:
        try:
            data = cli_sock.recv(1024)
            if (data == "A" or data == "a"):
                signup_client(cli_sock)
               #b_usr(cli_sock, data)
        except Exception as x:
            print(x.message)
            break

def b_usr(cs_sock, msg):
    for client in CONNECTIONS:
        if client != cs_sock:
            client.send(msg)

if __name__ == "__main__":    
    # socket
    ser_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ser_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # bind
    HOST = 'localhost'
    PORT = 5023
    ser_sock.bind((HOST, PORT))

    # listen    
    ser_sock.listen(1)
    print('Chat server started on port : ' + str(PORT))

    thread_ac = threading.Thread(target = listening_client)
    thread_ac.start()
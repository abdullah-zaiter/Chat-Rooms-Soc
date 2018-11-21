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

def accepting_protocol(ID):
    ID.send("What would you like to do ?")

def listening_client():
    while True:
        #accept    
        cli_sock, cli_add = ser_sock.accept()
        accepting_protocol(cli_sock)
        Users.append(cli_sock)
        thread_client = threading.Thread(target = broadcast_usr, args=[cli_sock])
        thread_client.start()

def print_send_available_users(ID)
    ID.send(Users)

def broadcast_usr(cli_sock):
    while True:
        try:
            data = cli_sock.recv(1024)
            if (data == "A" or data == "a"):
                print("acho que ele quer A")
               
               #manda pa geraaaaaaaaaaaaaal
               #b_usr(cli_sock, data)
        except Exception as x:
            print(x.message)
            break

def b_usr(cs_sock, msg):
    for client in Users:
        if client != cs_sock:
            client.send(msg)

if __name__ == "__main__":    
    Users = []

    # socket
    ser_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    # bind
    HOST = 'localhost'
    PORT = 5023
    ser_sock.bind((HOST, PORT))

    # listen    
    ser_sock.listen(1)
    print('Chat server started on port : ' + str(PORT))

    thread_ac = threading.Thread(target = listening_client)
    thread_ac.start()
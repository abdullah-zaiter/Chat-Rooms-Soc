import socket
import threading
import os.path
import time

#opcoes possiveis e como o servidor reconhece
def connection_options():
    print('''A- Register your username
B- Check available Users.
C- Check available chat rooms.
D- Joining a chat room.
E- Create a chat room.
F- Sign out of server.''')

#dada uma mensagem recebida pelo servidor, pega o conteudo e elimina o nome do usuario
#serve para tratar os casos de arquivos
def eliminate_username_from_msg(msg):
    flag = 0
    for i in range(len(msg)):
        if(msg[i]=='-'):
            flag = 1
        elif flag == 1:
            filename = msg[(i-len(msg)+1):]
            break
    return filename

#dado um nome de arquivo, checa se existe e envia caso existir 
def send_file(filename):
    if os.path.isfile(filename):
        socket_client.send(filename)
        time.sleep(.500)
        print("rolando envio")
        f = open(filename, "rb")
        l = f.read(1000)
        while (l):
            socket_client.send(l)
            l = f.read(1000)
    else:
        print("file doesn't exist.")
        socket_client.send("@nameerror")
        socket_client.send("@nameerror")
    socket_client.send("@endfile")

#dado um nome de arquivo, recebe o conteudo e crie ele no diretorio atual
def receive_file(filename):
    print("debug 1")
    f = open(filename, "w+")
    f.close()
    f = open(filename, "rb+")
    l = socket_client.recv(1024)
    l = eliminate_username_from_msg(l)
    while (l != "@endfile" and l != "@nameerror"):
        f.write(l)
        l = socket_client.recv(1024)
        l = eliminate_username_from_msg(l)
    f.close()
    if(l == "@nameerror"):
        os.remove(filename)

#thread que cuida de mandar dados o tempo todo ao servidor
def send():
    while True:
        msg = raw_input()
        msg = str(msg)
        if(msg == "config"):
            connection_options()
        elif(msg == "@file" or msg == "@FILE"):
            socket_client.send(msg)
            msg = raw_input("enter the file's name: ")
            msg = str(msg)
            send_file(msg)
        else:
            socket_client.send(msg)

#thread de receber dados do servidor o tempo todo
def receive():
    while True:
        data = socket_client.recv(1024)
        if (data[-5:] == "@file" or data[-5:] == "@FILE"):
            data = socket_client.recv(1024)
            receive_file(eliminate_username_from_msg(data))
        else:
            print(str(data))


if __name__ == "__main__":
    # socket
    #abre a conexao socket
    socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect
    HOST = 'localhost'
    PORT = 5023
    socket_client.connect((HOST, PORT))
    uname = "foo"
    print('Connected to remote host...')
    #printa opcoes de utilizacao
    connection_options()
    #thread de envio de dados
    thread_send = threading.Thread(target=send)
    thread_send.start()
    #thread de receber dados
    thread_receive = threading.Thread(target=receive)
    thread_receive.start()
    #isso permite envio e recebimento de dados simultaneo

import socket
import threading
import os.path
import time

def connection_options():
    print('''A- Register your username
B- Check available Users.
C- Check available chat rooms.
D- Entering a chat room.
E- Create a chat room.
F- Sign out of server.''')


def send_file(filename):
    if os.path.isfile(filename):
        socket_client.send(filename)
        time.sleep(.300)
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

def eliminate_username_from_msg(msg):
    flag = 0
    for i in range(len(msg)):
        if(msg[i]=='-'):
            flag = 1
        elif flag == 1:
            filename = msg[(i-len(msg)+1):]
            break
    return filename

def receive_file(filename):
    print("debug 1")
    f = open(filename, "w+")
    f.close()
    f = open(filename, "rb+")
    l = socket_client.recv(1024)
    l = eliminate_username_from_msg(l)
    print(l)
    while (l != "@endfile" and l != "@nameerror"):
        print("debug 2"+l)
        f.write(l)
        l = socket_client.recv(1024)
        l = eliminate_username_from_msg(l)
    f.close()
    if(l == "@nameerror"):
        os.remove(filename)


def send(uname):
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
    socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect
    HOST = 'localhost'
    PORT = 5023
    socket_client.connect((HOST, PORT))
    uname = "foo"
    print('Connected to remote host...')
    connection_options()

    thread_send = threading.Thread(target=send, args=[uname])
    thread_send.start()

    thread_receive = threading.Thread(target=receive)
    thread_receive.start()

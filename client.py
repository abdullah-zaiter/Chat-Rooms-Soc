import socket
import threading

def connection_options():
    print('''A- Register your username
B- Check available Users.
C- Check available chat rooms.
D- Entering a chat room.
E- Create a chat room.
F- Sign out of server.''')

def send(uname):
    while True:
        msg = raw_input()
        msg = str(msg)
        if(msg == "config"):
            connection_options()
        elif(msg == "@file" or msg == "@FILE"):
        else:
            socket_client.send(msg)


def receive():
    while True:
        data = socket_client.recv(1024)
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
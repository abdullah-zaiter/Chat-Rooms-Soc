import socket, threading


def send(uname):
    while True:
        msg = raw_input()
        data = str(msg)
        cli_sock.send(data)

def connection_options():
    print('''
    A- Check available Users.
    B- Check available chat rooms.
    C- Register to a chat room.
    D- Create a chat room.
        ''')

def receive():
    while True:
        data = cli_sock.recv(1024)
        if(data == "What would you like to do ?"):
                print(str(data))
                connection_options()


if __name__ == "__main__":   
    # socket
    cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect
    HOST = 'localhost'
    PORT = 5023

    uname = raw_input('Enter your chat username: ')

    cli_sock.connect((HOST, PORT))     
    print('Connected to remote host...')


    thread_send = threading.Thread(target = send,args=[uname])
    thread_send.start()

    thread_receive = threading.Thread(target = receive)
    thread_receive.start()
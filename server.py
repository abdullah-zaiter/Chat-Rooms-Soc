import threading
from user import *
from chatroom import *

#maquina de estados aqui, para cada um cliente tem uma maquina estados dessa rodanddo em paralelo
#para entender as letras dos ifs, aqui a explicacao de cada letra:
#A- Register your username
#B- Check available Users.
#C- Check available chat rooms.
#D- Entering a chat room.
#E- Create a chat room.
#F- Sign out of server.

#@exit eh usado para sair da sala caso ja tiver dentro

def state_machine(socket_client):
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
                    flag = enter_chatroom(socket_client)
                    if ((len(Chat_rooms)>=1) and flag):
                        state = 3
                        pass
                elif (data == "E" or data == "E"):
                    state = 3
                    create_chatroom(socket_client)
                elif (data == "F" or data == "f"):
                    signout_client(socket_client)
                    return 
            elif(state == 3):
                if(data == "@exit" or data == "@EXIT"):
                    exit_chatroom(socket_client)
                    socket_client.send("You exited the room !")
                    state = 2
                else:
                    send_msg_to_current_room(data,socket_client)            
        except (KeyboardInterrupt, SystemExit):
            s.close()
            sys.exit(0)
        except Exception as x:
            print(x.message)
            break

#thread que vai atualizando o arquivo de conexoes a cada conexao nova entrar no servidor
def clients_file_update():
    len_All_Users_aux = 0
    while True:
        if(len(All_Users)!= len_All_Users_aux):
            len_All_Users_aux = len(All_Users)
            j = 0
            clients_names = list() 
            for i in range(len(All_Users)):
                if(len(All_Users[i].Username)>=1):
                    j += 1
                    clients_names.append("User "+str(j)+": "+All_Users[i].Username+", adress "+str(All_Users[i].IP)+":"+str(All_Users[i].Port)+".")
            with open('clients.txt', 'w') as f:
                for item in clients_names:
                    print >> f, item
                f.close()
                del clients_names

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
    thread_file = threading.Thread(target=clients_file_update)
    thread_file.start()
    print('Chat server started on port : ' + str(PORT))
    #loop que checa se uma nova conexao foi feita e se sim cria uma nova thread de machina de estados para tratar este cliente.
    while True:
        j = 0 
        try:
            socket_client, cli_add = s.accept()
            All_Users.append(User(socket_client))
            All_Users[-1].IP = cli_add[0]
            All_Users[-1].Port = cli_add[1]
            thread_client = threading.Thread(target=state_machine, args=[socket_client])
            thread_client.start()
        except (KeyboardInterrupt, SystemExit):
            s.close()
            sys.exit(0)
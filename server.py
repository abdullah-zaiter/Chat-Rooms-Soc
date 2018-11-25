import threading
from chatroom import *

#maquina de estados aqui, para cada um cliente tem uma maquina estados dessa rodanddo em paralelo
#para entender as letras dos ifs, aqui a explicacao de cada letra:
#A- Register your username
#B- Check available Users.
#C- Check available chat rooms.
#D- Joining a chat room.
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
                    logging.info("Connection of "+str(All_Users[from_socket_conn_to_index(socket_client)].IP)+":"+str(All_Users[from_socket_conn_to_index(socket_client)].Port)+" is registered as "+All_Users[from_socket_conn_to_index(socket_client)].Username)                
                    state = 2
                else:
                    msg = "Access denied, Register your username by clicking A."
                    socket_client.send(msg)
                    logging.info("Server sent '"+msg+"' to connection at "+str(All_Users[from_socket_conn_to_index(socket_client)].IP)+":"+str(All_Users[from_socket_conn_to_index(socket_client)].Port))                
            elif (state == 2):
                if (data == "A" or data == "a"):
                    logging.info(All_Users[from_socket_conn_to_index(socket_client)].Username+" updated name to "+data)                
                    signup_client(socket_client)
                elif (data == "B" or data == "b"):
                    logging.info(All_Users[from_socket_conn_to_index(socket_client)].Username+" wanted to know the available users")                
                    check_users(socket_client)
                elif (data == "C" or data == "c"):
                    logging.info(All_Users[from_socket_conn_to_index(socket_client)].Username+" wanted to know the chat rooms")                
                    check_chatrooms(socket_client)
                elif (data == "D" or data == "d"):
                    logging.info(All_Users[from_socket_conn_to_index(socket_client)].Username+" tried to enter chat room")                                    
                    flag = join_chatroom(socket_client)
                    if ((len(Chat_rooms)>=1) and flag):
                        state = 3
                        index,j  = from_socket_conn_to_room_index(socket_client)
                        logging.info(All_Users[from_socket_conn_to_index(socket_client)].Username+" successfully joined chat room "+Chat_rooms[index].Name)                                    
                    else:
                        logging.info(All_Users[from_socket_conn_to_index(socket_client)].Username+" failed joining chat room")
                elif (data == "E" or data == "E"):
                    state = 3
                    create_chatroom(socket_client)
                    logging.info(All_Users[from_socket_conn_to_index(socket_client)].Username+" created chat room "+Chat_rooms[-1].Name)                                      
                elif (data == "F" or data == "f"):
                    name = All_Users[from_socket_conn_to_index(socket_client)].Username
                    signout_client(socket_client)
                    logging.info(name+" signed out the server")
                    return 
            elif(state == 3):
                index, j = from_socket_conn_to_room_index(socket_client)
                if(data == "@exit" or data == "@EXIT"):
                    msg = "You exited the room !"
                    logging.info("Server sent '"+msg+"' to "+ All_Users[from_socket_conn_to_index(socket_client)].Username)
                    logging.info(All_Users[from_socket_conn_to_index(socket_client)].Username+" signed out the chat room "+Chat_rooms[index].Name)
                    exit_chatroom(socket_client)
                    socket_client.send(msg)
                    state = 2
                elif(data == "@whosthere" or data == "@WHOSTHERE"):
                    Chat_rooms[index].check_room_users(socket_client)
                else:
                    logging.info(All_Users[from_socket_conn_to_index(socket_client)].Username+" contacted chat room "+ Chat_rooms[index].Name)                    
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

    logging.info("Server started on port : "+str(PORT))
    print('Chat server started on port : ' + str(PORT))
    #loop que checa se uma nova conexao foi feita e se sim cria uma nova thread de machina de estados para tratar este cliente.
    while True:
        j = 0 
        try:
            socket_client, cli_add = s.accept()
            All_Users.append(User(socket_client))
            All_Users[-1].IP = cli_add[0]
            All_Users[-1].Port = cli_add[1]
            logging.info("Connection of "+str(All_Users[-1].IP)+":"+str(All_Users[-1].Port)+" created")
            thread_client = threading.Thread(target=state_machine, args=[socket_client])
            thread_client.start()
        except (KeyboardInterrupt, SystemExit):
            s.close()
            sys.exit(0)
from commonfuncts import *

#classe que define o usuario dentro do servidor
#tem informacoes necessaarios, como IP, porta, nome de usuario no servidor e a conexao socket
class User:
    Connection = socket.socket()
    Username = ""
    IP = ''
    Port = int
    def __init__(self, connection):
        self.Connection = connection
    def send_message(self, msg):
        self.Connection.send(msg)
    def close_connection(self):
        self.Connection.close()

#dada uma string de nome de usuario, essa funcao retorna verdadeiro se houver algum usuario no servidor com esse username
def compare_string_to_existing_usernames(name):
    for i in range(len(All_Users)):
        if(name == All_Users[i].Username):
            return True
    return False

#dada uma conexao socket, essa funcao acha o usuario no vetor de usuarios e apaga ele e fecha a conexao socket
def delete_user(socket_client):
    index = from_socket_conn_to_index(socket_client)
    All_Users[index].close_connection()
    msg = "User "+ All_Users[index].Username + "signed out successfully."
    print(msg)
    logging.info("Server: "+msg)           
    del All_Users[index]
    socket_client.close()

#dada uma funcao socket, essa funcao faz o cadastro do cliente no servidor, pedindo as informacoes necessarias como username e trata casos de clisoes de username
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
        msg = "New User Added " + name
        print(msg)
        logging.info("Server: "+msg)                   
    All_Users[index].Username = name

#dada uma conexao socket, essa funcao comfirma se o cliente de fato quer sair do servidor e se sim ela retira ele.
def signout_client(socket_client):
    msg = "Are you sure you want to sign out ? (Y/N) "
    answer = send_receive_string(msg, socket_client)
    if(answer == "Y" or answer == "y"):
        delete_user(socket_client)

#essa funcao checa os usuarios atuais cadastrados no servidor e manda pro cliente que demandou a informacao
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

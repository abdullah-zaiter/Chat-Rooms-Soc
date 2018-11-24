class ChatRoom:
    Name = ""
    Type = ""  
    Users = list()
    Password = ""
    def __init__(self, name,ttype, user, password):
        self.Name = name
        self.Type = ttype
        self.Users.append(user)
        if(self.Type== "PRIVATE" or self.Type== "private"):
            self.Password = password     
    def send_to_all_users(self, msg, cs_sock):
        Room_Connections = []
        sender_name = ""
        for i in range(len(self.Users)):
            if (self.Users[i].Connection == cs_sock):
                sender_name = self.Users[i].Username
                pass
            Room_Connections.append(self.Users[i].Connection)
        msg = sender_name + " : " + msg
        for client in Room_Connections:
            if client != cs_sock:
                client.send(msg)
    def check_room_users(self, cs_sock):
        j = 0
        msg = ""
        for i in range(len(self.Users)):
            if(len(self.Users[i].Username)>=1):
                j += 1
                if(self.Users[i].Connection == cs_sock):
                    msg += "User "+str(j)+": YOU.\n"
                else:
                    msg += "User "+str(j)+": "+self.Users[i].Username+".\n"
        
        if(j==0):
            msg = "No one is in the room."
        cs_sock.send(msg)

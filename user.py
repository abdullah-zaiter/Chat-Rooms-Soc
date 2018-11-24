import socket
class User:
    Connection = socket.socket()
    Username = ""
    def __init__(self, connection):
        self.Connection = connection
    def send_message(self, msg):
        self.Connection.send(msg)
    def close_connection(self):
        self.Connection.close()

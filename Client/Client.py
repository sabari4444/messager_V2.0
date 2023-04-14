import socket
import json


class Connect_Init:
    def __init__(self):
        self.sock = None
        self.host_ip = "localhost"
        self.port = 7080
        self.connect()

    def connect(self):
        print("connecting to server...")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host_ip, self.port))
        print("connected to server")

    def recv_msg(self):
        data = self.sock.recv(1024)
        if data:
            return data

    def send_msg(self, msg):
        json_file = json.dumps(msg).encode()
        self.sock.send(json_file)

    def Frame_POST(self, USER_ID, USERNAME, CHATROOM, MESSAGE):
        data = {'PROTOCOL': "POST",
                'USER_ID': int(USER_ID),
                'USERNAME': USERNAME,
                'CHATROOM': CHATROOM,
                "MESSAGE": MESSAGE}
        print(data)
        self.send_msg(data)

    def Frame_GET(self,  USER_ID, USERNAME, CHATROOM, L_RECORD=0):
        data = {'PROTOCOL': "POST",
                'USER_ID': int(USER_ID),
                'USERNAME': USERNAME,
                'CHATROOM': CHATROOM,
                "L_RECORD": L_RECORD}
        self.send_msg(data)

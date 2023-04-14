import json
import socket
import threading
import msg_protocals as protocol


class Server_Init:
    def __init__(self):
        self.sock = None
        self.ip = "localhost"
        self.port = 7080
        self.clients_ = {}
        self.startup_sequence()

    def startup_sequence(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.ip, self.port))
        print(f'server up @{self.ip}:{self.port}')

        self.sock.listen()
        # Waiting for connections
        while True:
            conn, addr = self.sock.accept()
            self.clients_[addr] = conn
            print(f'total {self.clients_}')
            threading.Thread(target=self.listen_msg, args=(conn, addr)).start()

    @staticmethod
    def welcome_msg(conn, addr):
        conn.send("welcome".encode())
        print(f'{addr} has connected and welcome msg is sent')

    def listen_msg(self, conn, addr):
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    print(f"Client {addr} disconnected")
                    del self.clients_[addr]
                    print(f'\n {self.clients_}')
                    break
                data1 = json.loads(data.decode())
                print(f"Received from {addr}: {data1}")
                if data1['PROTOCOL'] == "POST":
                    protocol.Protocols.post_protocol(data1)
                elif data1['PROTOCOL'] == "GET":
                    message_data = protocol.Protocols.get_protocol(data1)
                    json_file = json.dumps(message_data).encode()
                    conn.send(json_file)
                else:
                    print('Error in file~format')

                for i in self.clients_:
                    self.clients_[i].send(data)

            except socket.error as e:
                print("Client disconnected with error:", e)
                del self.clients_[addr]
                print(f'\n {self.clients_}')
                break


Server_Init()

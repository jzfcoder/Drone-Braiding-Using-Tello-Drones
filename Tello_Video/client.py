import sys
import socket


class Client:

    def __init__(self, ip, port, id, controller):
        print("initializing client to ip {}, port {}, id {}".format(ip, port, id))

        self.controller = controller
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

        self.socket_list = [sys.stdin, self.connection]

    def update(self):
        print("updating client")

        for sock in self.socket_list:
            if sock == self.connection:
                data = sock.recv(4096)
                if not data:
                    return
                else:
                    print('received new command')
                    self.controller.send_command(data)

    def send_data(self, data):
        print("sending data: {}".format(data))
        self.connection.send(data.json)

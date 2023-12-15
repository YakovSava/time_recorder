import socket

from telnetlib import Telnet

def write(filename, msg):
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(msg+'\n')

class SimpleSyslogServer:

    def __init__(self, filename:str=None, ip:str=None):
        if not (filename and ip):
            raise
        self._ip = ip
        self._port = 514
        self._filename = filename

    def test_listen(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind((self._ip, self._port))
        while True:
            data, address = server_socket.recvfrom(4096)
            message = data.decode('utf-8')
            print(message)

    def start(self) -> None:
        print("Listem SYSLOG server!")
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind((self._ip, self._port))
        while True:
            data, address = server_socket.recvfrom(4096)
            message = data.decode('utf-8')
            write(self._filename, message)


class TelnetInfo:

    def __init__(self, client=Telnet):
        self._client = client('192.168.1.0', 23)


    def _authorize(self):
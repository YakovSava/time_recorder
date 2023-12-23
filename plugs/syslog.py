import socket

from time import sleep
from telnetlib import Telnet
from paramiko import SSHClient, AutoAddPolicy

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


# Please, do not use!
# This class will no longer be used
class TelnetInfo:

    def __init__(self, client=Telnet):
        self._client = client('192.168.1.1', 23)
        #self._client.set_window_size(65535, 1000)
        self._is_authorize = False

    def write(self, command:str) -> None:
        self._client.write(f'{command}\n'.encode())

    def read_until(self, until:str) -> bytes:
        return self._client.read_until(until.encode())

    def _authorize(self):
        self.read_until('Login')
        self.write('admin')
        self.read_until('Password')
        self.write('admin')
        self.read_until('>')
        self._is_authorize = True

    def get_log(self) -> str:
        if self._is_authorize:
            self.write('show log')
            sleep(15)
            return self._client.read_very_eager().decode('utf-8')
        else:
            self._authorize()
            return self.get_log()

    def save_log(self):
        with open('systemlog.log', 'a', encoding='utf-8') as file:
            file.write(self.get_log()[4:-1])
            #raise


class SSHLogger:

    def __init__(self, host:str='192.168.1.1', user:str='admin', password:str='admin'):
        self._client = SSHClient()
        self._client.set_missing_host_key_policy(AutoAddPolicy())
        self._client.connect(
            hostname=host,
            username=user,
            password=password,
            port=22
        )

    def get_log(self) -> str:
        stdin, stdout, stderr = self._client.exec_command('show log')
        return (stdout.read() + stderr.read()).decode('utf-8')

    def save_log(self):
        with open('systemlog.log', 'a', encoding='utf-8') as file:
            file.write(self.get_log()[4:-1])
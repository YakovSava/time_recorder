import socket

from multiprocessing import Process

class SimpleSyslogServer:

    def __init__(self, ip:str=None, save_to_file:bool=False):
        if ip is not None:
            self._ip = ip
        else:
            raise Exception('ip not found!')
        self._port = 514
        if save_to_file:
            self._file = 'syslog.log'
            self._size = 1048576
        else:
            self._file = 'syslog.log'
            self._size = 0
        self._filesave = save_to_file
        self._run = False
        self._event_log = []
        self._procs:list[Process] = []

    def _clear_event_log(self) -> None:
        self._event_log.clear()

    def _run_listen(self) -> None:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind((self._ip, self._port))
        while True:
            data, address = server_socket.recvfrom(4096)
            message = data.decode('utf-8')
            self._event_log.append(message)

    def start(self) -> None:
        self._procs.append(Process(target=self._run_listen))
        self._procs = list(map(lambda x: x.start(), self._procs))

    def stop(self) -> None:
        self._procs = list(map(lambda x: x.terminate(), self._procs))

    def listen(self):
        for item in self._event_log:
            yield item
        self._clear_event_log()
        return

    def _listen_to_file(self) -> None:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind((self._ip, self._port))
        with open(self._file, 'w', encoding='utf-8') as file:
            while True:
                data, address = server_socket.recvfrom(4096)  # Получаем данные из сокета
                message = data.decode('utf-8')
                file.write(message)

    def filelisten(self, filename:str=None) -> None:
        if not self._filesave:
            raise

        if filename is not None:
            self._file = filename
        self._procs.append(Process(target=self._listen_to_file))
        self._procs = list(map(lambda x: x.start(), self._procs))
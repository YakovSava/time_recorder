### Write function

```
def write(filename, msg)
```

Writes the message `msg` to the file `filename'. The file opens in append mode (`a") with UTF-8 encoding. Each message is written in a new line.

Arguments:
- `filename' (string): the path to the file to write the message to.
- `msg' (string): the message to be written to the file.

### SimpleSyslogServer class

#### Init method

```
def init(self, filename:str=None, ip:str=None)
```

Initializes an instance of the SimpleSyslogServer class. Sets the values of the `_ip`, `_port` and `_filename` attributes.

Arguments:
- `filename' (string, by default `None'): the path to the file to which messages will be written. If omitted, an exception will be thrown.
- `ip` (string, default is `None'): the IP address where the server will listen to messages. If omitted, an exception will be thrown.

#### test_listen method

```
def test_listen(self)
```

Listens to SYSLOG messages at the specified IP address and port `_ip` and `_port'. When a message is received, it decodes it into UTF-8 and prints it. The function works in an infinite loop.

#### Start method

```
def start(self) -> None
```

Starts the SYSLOG server. Prints the message "Listen SYSLOG server!". Creates a server socket and binds it to the IP address `_ip` and the port `_port'. Then calls the `test_listen()` method to start listening for SYSLOG messages.

Return value: None (`None`).
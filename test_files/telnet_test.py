from telnetlib import Telnet

with Telnet('localhost', 23) as client:
    # client.interact()
    us = client.read_until(b'Username')
    print(us.decode())
    print('-'*30)
    client.write(b'qwe\n')
    pswd = client.read_until(b'Password')
    print(pswd.decode())
    print('-' * 30)
    client.write(b'qwe\n')
    cnsl = client.read_until(b'>')
    print(cnsl.decode())
    print('-' * 30)
    client.write(b'dir /b\n')
    cnsl = client.read_until(b'>')
    print(cnsl.decode())
    print('-' * 30)
    client.close()
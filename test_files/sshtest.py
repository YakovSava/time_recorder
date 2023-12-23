from time import sleep
from paramiko import SSHClient, AutoAddPolicy

host = input('Host: ')
user = input('User: ')
passw = input('Password: ')

client = SSHClient()
client.set_missing_host_key_policy(AutoAddPolicy())
client.connect(
    hostname=host,
    username=user,
    password=passw,
    port=22
)

while True:
    try:
        cmd = input('< ')
        stdin, stdout, stderr = client.exec_command(cmd)
        if 'sudo' in cmd:
            stdin.write(passw + '\n')
            stdin.flush()
            sleep(1)
        data = stdout.read() + stderr.read()
        print(data)
    except BaseException:
        break

client.close()

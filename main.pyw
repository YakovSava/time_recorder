from time import sleep
from threading import Thread
from plugs import Converter, Book, Getter,\
    SimpleSyslogServer, GDrive

convert = Converter()
config = convert.load_conf()

# timer = Timer(gap=60*60*24)
syslog = SimpleSyslogServer(filename=config['log_name'], ip=config['ip'])
gdr = GDrive()
exc = Book(filename=config['excel_file'])
get = Getter(filename=config['log_name'])

def get_log(filelog:str) -> str:
    with open(filelog, 'r', encoding='utf-8') as file:
        return file.read()

def load_every_day() -> None:
    global config
    print('Loader func started!')
    while True:
        parsed_ln = get.parse_file()
        calculated_info = get.calculate_times(parsed_ln)

        filename = exc.save_xlsx(calculated_info)
        if config['file_id']:
            file_id = gdr.load_exc_file(filename=filename)
            config['file_id'] = file_id
            convert.update_conf(config)
        else:
            gdr.update_loaded_file(file_id=config['file_id'], filename=filename)

        # timer.wait()
        sleep(config['gap'])

if __name__ == '__main__':
    pr = Thread(target=syslog.start)
    pr.start()
    pr = Thread(target=load_every_day)
    pr.start()
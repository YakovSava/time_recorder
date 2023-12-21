from string import ascii_uppercase as asup
from time import sleep
from threading import Thread
from plugs import Converter, Book, Getter, \
    SimpleSyslogServer, GDrive, TelnetInfo
from plugs.google_connector import GDriveTest

convert = Converter()
config = convert.load_conf()

syslog = SimpleSyslogServer(filename=config['log_name'], ip=config['ip'])
gdr = GDrive()
# gdr = GDriveTest()
exc = Book(filename=config['excel_file'], cmp=convert)
get = Getter(filename=config['log_name'])
tel = TelnetInfo()


def _repl_normal(txt: str) -> str:
    for word in asup:
        txt = txt.replace(f'{word} ', '<14>').replace(f'[{word}] ', '<14>')
    t = txt.replace('[', '').replace(']', '').replace('                    ', '')
    return t if t.endswith('\n') else t + '\n'


def get_log(filelog: str) -> str:
    with open(filelog, 'r', encoding='utf-8') as file:
        return file.read()


def reformat_log(filelog: str) -> None:
    loglines = get_log(filelog).splitlines()
    loglines = list(map(
        _repl_normal, loglines
    ))
    with open(filelog, 'w', encoding='utf-8') as file:
        file.write("".join(loglines))


def load() -> None:
    global config
    print('Loader func started!')
    while True:
        config = convert.load_conf()
        reformat_log(config['log_name'])
        parsed_ln = get.parse_file()
        # with open('test_files/test_log.txt', 'r', encoding='utf-8') as file:
        #    parsed_ln = get.parse_string(file.read())
        calculated_info = get.calculate_times(parsed_ln)

        filename = exc.save_xlsx(calculated_info)
        if not config['file_id']:
            file_id = gdr.load_exc_file(filename=filename)
            config['file_id'] = file_id
            convert.update_conf(config)

            config = convert.load_conf()
        else:
            res = gdr.update_loaded_file(file_id=config['file_id'], filename=filename)
            print("File upload - ", res)
            if not res:
                result = gdr.repair(file_id=config['file_id'], filename=filename)
                if result:
                    file_id = gdr.load_exc_file(filename=filename)
                    config['file_id'] = file_id
                    convert.update_conf(config)

                    config = convert.load_conf()
        # gdr.test_check_trash()
        tel.save_log()

        sleep(config['gap'])


if __name__ == '__main__':
    pr = Thread(target=syslog.start)
    pr.start()
    pr = Thread(target=load)
    pr.start()

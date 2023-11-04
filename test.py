from time import sleep
from plugs import Getter, GDrive, Book,\
    Timer, SimpleSyslogServer


def func(*args, **kwargs):
    sleep(5)
    if not ((args == ()) and (kwargs == {})):
        print(args, kwargs)
    else:
        print('Hello world!')

def check_book():
    try:
        book = Book(filename='tables/test.xlsx')
        get = Getter(filename='test_files/test_log.txt', tested=True)

        parsed_ln = get.parse_file()
        calculated_info = get.calculate_times(parsed_ln)
        print(calculated_info)

        book.save_xlsx(calculated_info)
    except Exception as ex:
        raise ex
    else:
        return 'Test pass'


def check_syslog():
    try:
        logserv = SimpleSyslogServer(ip='192.168.1.146')
        logserv.start()
        c = 0
        for info in logserv.listen():
            print(info)
            if c > 50:
                break
        logserv.filelisten(filename='test.log')

        del logserv

        filelogserv = SimpleSyslogServer(ip='192.168.1.146', save_to_file=True)
        filelogserv.filelisten(filename='test.log')

        with open('test.log', 'r', encoding='utf-8') as file:
            print(file.read())

        filelogserv.stop()
        with open('test.log', 'r', encoding='utf-8') as file:
            print(file.read())
    except Exception as ex:
        raise ex
    else:
        return 'Test pass'

def check_gdrive():
    try:
        gd = GDrive()
        gd.send_exc_file(filename='test_files/test_log.txt')
    except Exception as ex:
        raise ex
    else:
        return 'Test pass'

def check_timer():
    try:
        timer = Timer(gap=0, queue=[])
        for _ in range(5):
            timer.add_to_queue(func)
        timer.start_job()

        coro = timer.coro(func, 'Hello', world=True)
        print(coro)
        coro()
    except Exception as ex:
        raise ex
    else:
        return 'Test pass'

if __name__ == '__main__':
    print(check_book())
    # print(check_syslog())
    # print(check_gdrive())
    # print(check_timer())
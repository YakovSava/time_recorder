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
        book = Book(filename='../tables/test.xlsx')
        get = Getter(filename='test_log.txt', tested=False)

        parsed_ln = get.parse_file()
        calculated_info = get.calculate_times(parsed_ln)

        book.save_xlsx(calculated_info)
    except Exception as ex:
        raise ex
    else:
        return 'Test pass'

def check_syslog():
    try:
        filelogserv = SimpleSyslogServer(ip='192.168.1.146', filename='test.log')

        filelogserv.test_listen()
    except Exception as ex:
        raise ex
    else:
        return 'Test pass'

def check_filesyslog():
    try:
        filelogserv = SimpleSyslogServer(ip='192.168.1.146', filename='test.log')

        filelogserv.start()
    except Exception as ex:
        raise ex
    else:
        return 'Test pass'

def check_gdrive():
    try:
        gd = GDrive()
        gd.send_exc_file(filename='test_log.txt')
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
    # print(check_filesyslog())
    # print(check_gdrive())
    # print(check_timer())
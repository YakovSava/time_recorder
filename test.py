from plugs import Getter, GDrive, Book,\
    Timer, SimpleSyslogServer

def check_book():
    try:
        book = Book(filename='tables/test.xlsx')
        get = Getter(filename='test_files/test_log.txt', tested=True)

        parsed_ln = get.parse_file()
        calculated_info = get.calculate_times(parsed_ln)

        book.save_xlsx(calculated_info)
    except Exception as ex:
        return ex
    else:
        return


def check_syslog(self):
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
        return ex
    else:
        return
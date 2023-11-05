from plugs import Converter, Book, Getter,\
    Timer, SimpleSyslogServer, GDrive

convert = Converter()
config = convert.load_conf()

timer = Timer(gap=60*60*2)
syslog = SimpleSyslogServer(filename=config['log_name'], ip=config['ip'])
gdr = GDrive()
exc = Book(filename=config['excel_file'])
get = Getter(filename=config['log_name'])

def get_log(filelog:str) -> str:
    with open(filelog, 'r', encoding='utf-8') as file:
        return file.read()

def load_every_day() -> None:
    print('Loader func started!')
    while True:
        parsed_ln = get.parse_file()
        calculated_info = get.calculate_times(parsed_ln)

        filename = exc.save_xlsx(calculated_info)
        gdr.send_exc_file(filename=filename)

        timer.wait()

if __name__ == '__main__':
    timer.add_to_queue(syslog.start)
    timer.add_to_queue(load_every_day)
    timer.start_job()
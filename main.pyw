from time import sleep
#from threading import Thread
from plugs import Converter, Book, Getter,\
    SimpleSyslogServer, GDrive, SSHLogger,\
    Logger
from plugs.google_connector import GDriveTest

asup = 'EWI'

convert = Converter()
config = convert.load_conf()

log = Logger(filename=config['s_log_name'], debug=True)
log.write('Конфиг загружен')
log.write('Дескриптор логгера запущен')


#syslog = SimpleSyslogServer(filename=config['log_name'], ip=config['ip']) # Not used!
log.write('Запуск дескриптора Google Drive')
#gdr = GDrive()
gdr = GDriveTest()
log.write('Запуск дескриптора Excel')
exc = Book(filename=config['excel_file'], cmp=convert)
log.write('Запуск дескриптора получения логов')
get = Getter(filename=config['log_name'])
log.write('Запуск SSH дескриптора')
#ssh = SSHLogger()

def _repl_log(conf):
    log.write('Запуск функции преобразования логов')
    with open(conf['log_name'], 'r', encoding='utf-8') as file:
        parts = file.read().splitlines()
    fixed = []

    for part in parts:
        if part.startswith('<14>') or not fixed:
            fixed.append(part)
        else:
            fixed[-1] += ' '+part
    with open(conf['log_name'], 'w', encoding='utf-8') as file:
        file.write('\n'.join(fixed))
    log.write('Функция преобразования завершила работу')


def _repl_normal(txt: str) -> str:
    # log.write('Запуск функции преобразования строки')
    for word in asup:
        txt = txt.replace(f'{word} ', '<14>').replace(f'[{word}] ', '<14>')
    t = txt.replace('[', '').replace(']', '').replace(
        '                    ', '')
    # log.write('Функция преобразования строки завершила работу')
    return t if t.endswith('\n') else t + '\n'


def get_log(filelog: str) -> str:
    log.write('Получение лога')
    with open(filelog, 'r', encoding='utf-8') as file:
        return file.read()


def reformat_log(filelog: str) -> None:
    log.write('Запуск реформатирования лога')
    loglines = get_log(filelog).splitlines()
    loglines =  list(map(
        _repl_normal, loglines
    ))
    with open(filelog, 'w', encoding='utf-8') as file:
        file.write("".join(loglines))
    log.write('Реформатирование лога завершено')


def load() -> None:
    log.write('Запуск загрузчика\n')
    global config
    print('Loader func started!')
    while True:
        log.write('Цикл начат')
        config = convert.load_conf()
        reformat_log(config['log_name'])
        _repl_log(config)
        parsed_ln = get.parse_file()
        calculated_info = get.calculate_times(parsed_ln)
        log.write('Завершено первичное преобразование')

        filename = exc.save_xlsx(calculated_info)
        if not config['file_id']:
            log.write('ID файла не найдено. Начинается загрузка excel файла')

            file_id = gdr.load_file(filename=filename)
            config['file_id'] = str(file_id)
            convert.update_conf(config)
            log.write('Excel файл загружен')

            config = convert.load_conf()
            log.write('Перезагрузка конфига')

        else:
            log.write('ID файла найден. Начато обновление')

            res = gdr.update_loaded_file(
                file_id=config['file_id'], filename=filename)
            log.write('Перепроверка обноваления файла')

            if not res:
                result = gdr.repair(
                    file_id=config['file_id'], filename=filename)
                log.write('Попытка исправить ситуацию автоматически')

                if result:
                    log.write('Исправление успешно применено')

                    file_id = gdr.load_file(filename=filename)
                    config['file_id'] = str(file_id)
                    convert.update_conf(config)

                    config = convert.load_conf()
                else:
                    log.write('Ошибка! Исправление требует вмешательство!')
        log.write("Загрузка excel файла завершена")

        if not config['log_file_id']:
            log.write('ID лог файла не найдено. Начата загрузка')

            file_id = gdr.load_file(filename="logged.log")
            config['log_file_id'] = str(file_id)
            convert.update_conf(config)
            log.write('Загрузка завершена')

            config = convert.load_conf()
            log.write('Перезагрузка конфига')

        else:
            log.write('ID файла найден. Начинается обновление файла')

            res = gdr.update_loaded_file(
                file_id=config['log_file_id'], filename="logged.log")
            log.write('Файл обновлён')

            if not res:
                result = gdr.repair(
                    file_id=config['log_file_id'], filename="logged.log")
                log.write('Файл не обновлён. Попытка автоматического исправления')

                if result:
                    log.write('Исправление применено')

                    file_id = gdr.load_file(filename="logged.log")
                    config['log_file_id'] = str(file_id)
                    convert.update_conf(config)

                    config = convert.load_conf()
                else:
                    log.write('Неизвестная ошибка! Требуется вмешательство человека')
        log.write("Загрузка лога событий завершена")

        if not config['router_log_file_id']:
            log.write('ID лог файла не найдено. Начата загрузка')

            file_id = gdr.load_file(filename="systemlog.log")
            config['router_log_file_id'] = str(file_id)
            convert.update_conf(config)
            log.write('Загрузка завершена')

            config = convert.load_conf()
            log.write('Перезагрузка конфига')

        else:
            log.write('ID файла найден. Начинается обновление файла')

            res = gdr.update_loaded_file(
                file_id=config['router_log_file_id'], filename="systemlog.log")
            log.write('Файл обновлён')

            if not res:
                result = gdr.repair(
                    file_id=config['router_log_file_id'], filename="systemlog.log")
                log.write('Файл не обновлён. Попытка автоматического исправления')

                if result:
                    log.write('Исправление применено')

                    file_id = gdr.load_file(filename="systemlog.log")
                    config['router_log_file_id'] = str(file_id)
                    convert.update_conf(config)

                    config = convert.load_conf()
                else:
                    log.write('Неизвестная ошибка! Требуется вмешательство человека')
        log.write("Загрузка лога роутера")

        log.write('Сохранение лога с SSH сервера')
        #ssh.save_log()

        log.write('Цикл был завершён. Ожидание...\n')
        sleep(config['gap'])


if __name__ == '__main__':
    log.write("Старт программы!")
    load()

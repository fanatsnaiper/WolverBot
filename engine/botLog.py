import logging
from logging import FileHandler,Formatter
import os.path

LOG_INST = [ # пример регистраторов
    'sql',
    'handler',
    'extra'
]
LOGGER_PROGRAM = 'botLog.py'
LOG_COMMAND = "python botLog.py -r {reg} -f {filename} -l {lvl} -m {msg}"
ERROR,WARNING,INFO,DEBUG = 40,30,20,10
MIN_LVL = DEBUG # Минимальный уровень записи в журнал

class ParamsError(Exception):
    pass


if __name__ == '__main__':
    # Получение параметров
    from sys import argv
    initial = False
    script = None
    target_reg = None
    target_file = None
    target_lvl = None
    target_msg = None
    if argv.__len__() == 1:
        pass
    else:
        # Обработка переданных параметров
        for i,arg in enumerate(argv):
            if i==0:
                script = arg
            if arg =='-r':
                target_reg = argv[i+1]
            if arg == '-f':
                target_file = argv[i + 1]
            if arg =='-l':
                target_lvl = argv[i+1]
            if arg =='-m':
                target_msg = argv[i+1]
            if arg =='-i':
                initial = True

    # Проверка корректности переданных параметров
    err_msg = "Params error. Add {need_param}. Value {call_param} is uncorrect"
    if target_reg == None or target_reg.replace(' ','')=='':
        err_msg = err_msg.format(need_param='target_reg',call_param=target_reg)
        raise ParamsError(err_msg)
    if target_file == None or target_file.replace(' ','')=='':
        err_msg = err_msg.format(need_param='target_file', call_param=target_file)
        raise ParamsError(err_msg)
    if target_lvl == None:
        err_msg = err_msg.format(need_param='target_lvl', call_param=target_lvl)
        raise ParamsError(err_msg)
    if target_msg == None or target_msg.replace(' ','') =='':
        err_msg = err_msg.format(need_param='target_msg', call_param=target_msg)
        raise ParamsError(err_msg)

    if argv.__len__() > 15:
        raise ParamsError("Params error. Too many arguments")

    # Проверка правильности уровня записи
    if str(target_lvl).upper() =='ERROR':
        target_lvl = ERROR
    elif str(target_lvl).upper() =='WARNING':
        target_lvl = WARNING
    elif str(target_lvl).upper() =='INFO':
        target_lvl = INFO
    elif str(target_lvl).upper() =='DEBUG':
        target_lvl = DEBUG
    else:
        try:
            target_lvl = int(target_lvl)
            if target_lvl not in [ERROR,WARNING,INFO,DEBUG]:
                raise ParamsError("Log lvl error")
        except ValueError:
            raise ParamsError("Log lvl error")

    # Проставление дефолтных значений параметров
    # if not target_reg or target_reg == '':
    #     target_reg = 'sql' # -r
    # if not target_file or target_file == '':
    #     target_file = 'testlog.txt' # -f
    # if not target_lvl or target_lvl == '':
    #     target_lvl = INFO # -l
    # if not target_msg or target_msg == '':
    #     target_msg = 'test' # -m

    # Получение журнала
    log = logging.getLogger(target_reg)
    log.setLevel(MIN_LVL)

    # Выбор целевого журнала
    mode = 'a'
    if not os.path.exists(target_file):
        mode = 'w'
    l_handler = FileHandler(filename=target_file,
                                  mode=mode)

    # Форматирование записи в журнал
    l_handler.setFormatter(Formatter(fmt='[%(levelname)s] %(asctime)s: %(message)s'))
    log.addHandler(l_handler)

    # Запись в журнал
    if target_lvl == DEBUG:
        log.debug(target_msg)
    if target_lvl == INFO:
        log.info(target_msg)
    if target_lvl == WARNING:
        log.warning(target_msg)
    if target_lvl == ERROR:
        log.error(target_msg)

from abc import abstractmethod,ABC

class DbError(Exception,ABC):
    @abstractmethod
    def process(self):
        pass

class BotError(Exception,ABC):
    @abstractmethod
    def process(self):
        pass

class BotValueError(BotError):
    @classmethod
    def process(cls):
        error_message="Неверный тип данных"
        return(error_message)

class BotConnError(BotError):
    @classmethod
    def process(cls):
        print("Нет доступа к базе данных")

class DBdataError(DbError):
    @classmethod
    def process(cls):
        error_message="Данные отсутствуют"
        return error_message

class ParamsError(Exception):
    @classmethod
    def process(cls):
        error_message="Неверно заданы параметры"
        return error_message
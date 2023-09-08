from abc import abstractmethod,ABC

class DbError(ABC):
    @abstractmethod
    def process(self):
        pass

class BotError(ABC):
    @abstractmethod
    def process(self):
        pass

class BotValueError(BotError):
    @staticmethod
    def process():
        error_message="Ожидалось число"
        return(error_message)

class BotConnError(BotError):
    @staticmethod
    def process():
        print("Нет доступа к данным")

class DBdataError(DbError):
    @staticmethod
    def process():
        error_message="Данные отсутствуют"
        return error_message
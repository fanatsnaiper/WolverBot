from abc import abstractmethod, ABC
class Validator(ABC):
    @abstractmethod
    def validateValue(self, value):
        pass # todo добавить проверку по метаданным бд или другим параметрам

class TextValidator(Validator):
    @staticmethod
    def validateValue(value):
        try:
            value=str(value)
            return True
        except ValueError:
            return False
        
    @staticmethod
    def validatePlayerName(value):
        if TextValidator.validateValue(value) == False:
            return False
        value = str(value)
        for i in range(0,10,1):
            if str(i) in value:
                return False
        if value.split(' ').__len__() != 2:
            return False
        return True


class IntValidator(Validator):
    @staticmethod
    def validateValue(value):
        try:
            int(value)
            return True
        except ValueError:
            return False

